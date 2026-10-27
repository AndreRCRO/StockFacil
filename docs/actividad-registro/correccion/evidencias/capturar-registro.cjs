const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'C:/Users/andre/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const base = process.env.REGISTRO_URL || 'http://127.0.0.1:8005';
const phase = process.env.REGISTRO_FASE || 'inicial';
const out = __dirname;
const email = phase === 'inicial' ? 'ana.sqa@example.test' : 'beatriz.sqa@example.test';
const password = 'abc12345';
const results = [];
(async () => {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({ viewport: { width: 1366, height: 960 } });
    await context.tracing.start({ screenshots: true, snapshots: true });
    const page = await context.newPage();
    const jsErrors = [];
    page.on('pageerror', error => jsErrors.push(error.message));
    async function capture(id) {
        await page.evaluate(() => document.fonts.ready);
        const file = `${phase}-${id}.png`;
        await page.screenshot({ path: path.join(out, file), fullPage: true });
        return file;
    }
    async function run(id, expected, fn) {
        const at = new Date().toISOString();
        try {
            const observed = await fn();
            results.push({ id, expected, observed, status: 'aprobado', at, url: page.url(), image: await capture(id) });
        } catch (error) {
            results.push({ id, expected, observed: error.message, status: 'fallido', at, url: page.url(), image: await capture(id) });
        }
        console.log(`${id} ${results.at(-1).status}: ${results.at(-1).observed}`);
    }
    async function form(overrides = {}) {
        await page.goto(base + '/register');
        const data = { name: 'Ana SQA', email, password, password_confirmation: password, ...overrides };
        for (const [field, value] of Object.entries(data)) await page.locator('#' + field).fill(value);
        await page.locator('form').evaluate(form => { form.noValidate = true; });
    }
    async function submit() {
        await page.getByRole('button', { name: 'Crear cuenta', exact: true }).click();
        await page.waitForLoadState('networkidle');
    }
    try {
        await page.goto(base + '/register');
        await capture('formulario');
        await run('REG-01', 'Crear cuenta válida y mostrar confirmación en login', async () => {
            await form(); await submit();
            assert(page.url().endsWith('/login'));
            const message = await page.locator('.flash-success').innerText();
            assert(message.includes('Cuenta creada correctamente'));
            return message;
        });
        await run('REG-02', 'Rechazar correo duplicado incluso con mayúsculas y espacios', async () => {
            await form({ email: ' ' + email.toUpperCase() + ' ' }); await submit();
            const message = await page.locator('#email-error').innerText();
            assert(message.includes('ya está registrado'));
            assert.equal(await page.locator('#password').inputValue(), '');
            return message + ' Contraseña no recuperada en formulario.';
        });
        for (const [id, field, value, expected] of [
            ['REG-03', 'email', 'invalido', 'Rechazar formato de correo inválido'],
            ['REG-04', 'password', '1234567', 'Rechazar contraseña de 7 caracteres'],
            ['REG-05', 'password_confirmation', 'diferente', 'Rechazar confirmación distinta'],
            ['REG-06', 'name', '', 'Rechazar nombre vacío'],
            ['REG-07', 'password', 'á'.repeat(40), 'Rechazar contraseña superior a 72 bytes']
        ]) await run(id, expected, async () => {
            const data = { email: 'sin-crear@example.test', [field]: value };
            if (field === 'password') data.password_confirmation = value;
            await form(data); await submit();
            const errorField = field === 'password_confirmation' ? 'password' : field;
            const message = await page.locator('#' + errorField + '-error').innerText();
            assert(message.length > 0);
            assert(page.url().endsWith('/register'));
            return message;
        });
        await run('REG-08', 'Rechazar POST sin token CSRF con HTTP 419', async () => {
            const response = await page.request.post(base + '/register', { form: { name: 'Sin token', email: 'sin-token@example.test', password, password_confirmation: password } });
            assert.equal(response.status(), 419);
            await page.goto(base + '/register');
            return `POST real sin token: HTTP ${response.status()}; ningún registro aceptado.`;
        });
        await run('REG-09', 'Iniciar sesión con el correo registrado en mayúsculas', async () => {
            await page.goto(base + '/login');
            await page.locator('#email').fill(email.toUpperCase());
            await page.locator('#password').fill(password);
            await page.getByRole('button', { name: 'Iniciar sesión' }).click();
            await page.waitForLoadState('networkidle');
            if (!page.url().endsWith('/dashboard')) throw new Error('No accedió al dashboard: ' + await page.locator('.flash-error').innerText());
            return 'Dashboard accesible con el correo en mayúsculas.';
        });
        if (page.url().endsWith('/dashboard')) await page.getByRole('button', { name: 'Cerrar sesión' }).click();
        await run('REG-10', 'Formulario móvil sin desbordamiento horizontal', async () => {
            await page.setViewportSize({ width: 390, height: 844 });
            await page.goto(base + '/register');
            assert(await page.getByRole('button', { name: 'Crear cuenta', exact: true }).isVisible());
            assert(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
            return 'Formulario legible a 390 px; sin desbordamiento horizontal.';
        });
        await page.setViewportSize({ width: 1366, height: 960 });
        await run('REG-11', 'Login normal y bloqueo de registro para usuario autenticado', async () => {
            await page.goto(base + '/login');
            await page.locator('#email').fill(email);
            await page.locator('#password').fill(password);
            await page.getByRole('button', { name: 'Iniciar sesión' }).click();
            await page.waitForURL('**/dashboard');
            await page.goto(base + '/register');
            assert(page.url().endsWith('/dashboard'));
            return 'Usuario autenticado redirigido al dashboard; no puede registrar otra cuenta.';
        });
    } finally {
        fs.writeFileSync(path.join(out, `navegador-${phase}.json`), JSON.stringify({ base, phase, email, jsErrors, results }, null, 2));
        await context.tracing.stop({ path: path.join(out, `trace-${phase}.zip`) });
        await browser.close();
    }
    if (results.some(r => r.status !== 'aprobado')) process.exitCode = 1;
})().catch(error => { console.error(error); process.exitCode = 2; });
