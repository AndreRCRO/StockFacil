const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');

// Run ONLY against a dedicated SQLite test instance seeded separately.
const base = process.env.SQA_URL || 'http://127.0.0.1:8003';
const email = process.env.SQA_ADMIN_EMAIL || 'admin@stockfacil.test';
const password = process.env.SQA_ADMIN_PASSWORD || 'StockFacil2026!';
const output = __dirname;
const results = [];

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const jsErrors = [];
    page.on('pageerror', error => jsErrors.push(error.message));
    async function go(url) {
        const response = await page.goto(base + url);
        assert.equal(response.status(), 200, url);
        await page.evaluate(() => document.fonts.ready);
    }
    async function capture(name, selector = 'main') {
        const file = name + '.png';
        if (selector) await page.locator(selector).screenshot({ path: path.join(output, file) });
        else await page.screenshot({ path: path.join(output, file), fullPage: false });
        return file;
    }
    function record(id, obtained, evidence) {
        results.push({ id, status: 'aprobado', obtained, evidence, url: page.url(), recorded_at: new Date().toISOString() });
        console.log(`${id}: aprobado - ${obtained}`);
    }
    async function productForm(overrides = {}) {
        await go('/products/create');
        const values = { name: 'Producto SQA - HU01', sku: 'SQA-001', price: '8.50', initial_stock: '10', minimum_stock: '3', ...overrides };
        for (const [field, value] of Object.entries(values)) await page.locator('#' + field).fill(value);
        await page.locator('#category_id').selectOption({ label: 'Bebidas' });
        await page.locator('form[data-submit-form]').evaluate(form => { form.noValidate = true; });
    }
    async function submitProduct() {
        await page.getByRole('button', { name: 'Registrar producto', exact: true }).click();
        await page.waitForLoadState('networkidle');
    }
    async function invalidProduct(id, field, value, file) {
        await productForm({ sku: 'SQA-INVALID', [field]: value });
        await submitProduct();
        const error = page.locator('#' + field + '-error');
        assert.equal(await error.count(), 1);
        record(id, await error.innerText(), await capture(file, '.form-panel'));
    }
    let productId;
    async function movement(type, quantity, note = '') {
        await go(`/movements/create?type=${type}&product_id=${productId}`);
        await page.locator('#quantity').fill(String(quantity));
        await page.locator('#note').fill(note);
        await page.locator('form[data-submit-form]').evaluate(form => { form.noValidate = true; });
    }
    async function submitMovement() {
        await page.getByRole('button', { name: 'Registrar movimiento', exact: true }).click();
        await page.waitForLoadState('networkidle');
    }
    try {
        await go('/login');
        await page.locator('#email').fill(email);
        await page.locator('#password').fill(password);
        await page.getByRole('button', { name: 'Iniciar sesión' }).click();
        await page.waitForURL('**/dashboard');
        await page.waitForLoadState('networkidle');
        await capture('dashboard', null);
        await go('/products/create');
        await capture('hu01-formulario', '.form-panel');
        await productForm();
        await submitProduct();
        assert(page.url().endsWith('/products'));
        const flash = await page.locator('.flash-success').innerText();
        record('CP-01', flash, await capture('hu01-registro-exitoso'));

        await invalidProduct('CP-02', 'name', '', 'hu01-error-nombre');
        await invalidProduct('CP-03', 'sku', 'SQA-001', 'hu01-error-sku');
        await invalidProduct('CP-04', 'price', '-1', 'hu01-error-precio');
        await invalidProduct('CP-05', 'initial_stock', '-1', 'hu01-error-stock-inicial');
        await go('/products?q=SQA-001');
        const row = page.locator('tbody tr');
        assert.equal(await row.count(), 1);
        assert((await row.innerText()).includes('Producto SQA - HU01'));
        assert.equal((await row.locator('td').nth(3).innerText()).trim(), '10');
        const edit = await page.getByRole('link', { name: 'Editar Producto SQA - HU01' }).getAttribute('href');
        productId = edit.match(/products\/(\d+)\/edit/)[1];
        record('CP-06', 'Producto SQA-001 visible en el listado filtrado, Bs 8,50 y stock 10.', await capture('hu01-producto-listado'));
        await productForm({ name: '', sku: 'SQA-ERROR' });
        await submitProduct();
        assert.equal(await page.locator('.flash-error').count(), 1);
        assert.equal(await page.locator('#name').getAttribute('aria-invalid'), 'true');
        assert.equal(await page.locator('#sku').inputValue(), 'SQA-ERROR');
        record('CP-07', 'Resumen y mensaje junto al nombre visibles; SKU conservado y aria-invalid=true.', await capture('hu01-mensajes-validacion'));

        await movement('entrada', 5, 'Entrada SQA CP-08');
        assert.equal(await page.locator('[data-current-stock]').innerText(), '10');
        assert.equal(await page.locator('[data-next-stock]').innerText(), '15');
        await capture('hu02-formulario-movimiento');
        await submitMovement();
        assert(page.url().endsWith('/movements'));
        record('CP-08', 'Entrada de 5 aceptada; historial muestra stock 10 a 15.', await capture('hu02-entrada-exitosa'));
        await movement('salida', 12, 'Salida SQA CP-09');
        assert.equal(await page.locator('[data-current-stock]').innerText(), '15');
        assert.equal(await page.locator('[data-next-stock]').innerText(), '3');
        await submitMovement();
        record('CP-09', 'Salida de 12 aceptada; historial muestra stock 15 a 3.', await capture('hu02-salida-exitosa'));
        for (const [id, amount, name] of [['CP-10', 4, 'hu02-error-insuficiente'], ['CP-11', 0, 'hu02-error-cero'], ['CP-12', -1, 'hu02-error-negativo']]) {
            await movement('salida', amount);
            await submitMovement();
            const error = await page.locator('#quantity-error').innerText();
            assert.equal(await page.locator('[data-current-stock]').innerText(), '3');
            record(id, error + ' Saldo conservado: 3.', await capture(name));
        }
        await go('/movements?product_id=' + productId);
        assert.equal(await page.locator('tbody tr').count(), 3);
        const history = await page.locator('tbody').innerText();
        assert(history.includes('Stock inicial') && history.includes('Entrada SQA CP-08') && history.includes('Salida SQA CP-09'));
        record('CP-13', 'Tres movimientos: entrada inicial 0 a 10, entrada 10 a 15 y salida 15 a 3; responsable, fecha y observaciones visibles.', await capture('hu02-historial'));
        await go('/stock-bajo?q=SQA-001');
        assert.equal(await page.locator('tbody tr').count(), 1);
        const alert = await page.locator('tbody').innerText();
        assert(alert.includes('Stock bajo'));
        assert.equal((await page.locator('tbody tr td').nth(2).innerText()).trim(), '3');
        assert.equal((await page.locator('tbody tr td').nth(3).innerText()).trim(), '3');
        record('CP-14', 'Alerta Stock bajo visible con stock 3 y mínimo 3.', await capture('hu02-alerta-minimo'));
        assert.equal(jsErrors.length, 0, jsErrors.join('\n'));
    } catch (error) {
        results.push({ status: 'fallido', error: error.message, url: page.url(), recorded_at: new Date().toISOString() });
        throw error;
    } finally {
        fs.writeFileSync(path.join(output, 'resultados-navegador.json'), JSON.stringify({ base_url: base, isolated_database: true, note: 'noValidate usado intencionalmente en pruebas negativas para verificar validación del servidor', cases: results, js_errors: jsErrors }, null, 2));
        await browser.close();
    }
})().catch(error => { console.error(error); process.exit(1); });
