const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const base = process.env.SQA_URL || 'http://127.0.0.1:8003';
    const results = [];
    try {
        await page.goto(base + '/login');
        await page.locator('#email').fill(process.env.SQA_ADMIN_EMAIL || 'admin@stockfacil.test');
        await page.locator('#password').fill(process.env.SQA_ADMIN_PASSWORD || 'StockFacil2026!');
        await page.getByRole('button', { name: 'Iniciar sesión' }).click();
        await page.waitForURL('**/dashboard');
        await page.goto(base + '/products?q=SQA-001');
        const href = await page.getByRole('link', { name: 'Editar Producto SQA - HU01' }).getAttribute('href');
        const id = href.match(/products\/(\d+)\/edit/)[1];
        for (const [cp, quantity, file, expected] of [
            ['CP-11', 0, 'hu02-error-cero.png', 'La cantidad debe ser mayor o igual a 1.'],
            ['CP-12', -1, 'hu02-error-negativo.png', 'La cantidad debe ser mayor o igual a 1.'],
            ['REG-MAX', 2147483648, 'hu02-error-maximo.png', 'La cantidad no debe superar 2147483647.'],
        ]) {
            await page.goto(`${base}/movements/create?type=salida&product_id=${id}`);
            await page.locator('#quantity').fill(String(quantity));
            await page.locator('form[data-submit-form]').evaluate(form => { form.noValidate = true; });
            await page.getByRole('button', { name: 'Registrar movimiento', exact: true }).click();
            await page.waitForLoadState('networkidle');
            const message = await page.locator('#quantity-error').innerText();
            assert.equal(message, expected);
            assert.equal(await page.locator('[data-current-stock]').innerText(), '3');
            await page.locator('main').screenshot({ path: path.join(__dirname, file) });
            results.push({ id: cp, status: 'aprobado', quantity, message, stock: 3, evidence: file, recorded_at: new Date().toISOString() });
        }
        await page.goto(base + '/movements?product_id=' + id);
        assert.equal(await page.locator('tbody tr').count(), 3);
        const initial = JSON.parse(fs.readFileSync(path.join(__dirname, 'resultados-navegador-antes.json'), 'utf8'));
        for (const cp of initial.cases) {
            const update = results.find(item => item.id === cp.id);
            if (update) { cp.obtained = update.message + ' Saldo conservado: 3.'; cp.recorded_at = update.recorded_at; }
        }
        initial.correction = 'HR-04: CP-11 y CP-12 reejecutados; REG-MAX adicional. Historial permanece en tres movimientos.';
        fs.writeFileSync(path.join(__dirname, 'resultados-navegador.json'), JSON.stringify(initial, null, 2));
        fs.writeFileSync(path.join(__dirname, 'revalidacion-correccion.json'), JSON.stringify({ finding: 'HR-04', cases: results, history_count: 3 }, null, 2));
        console.log('PASS: CP-11, CP-12 y REG-MAX. Mensajes corregidos; saldo 3; historial 3.');
    } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
