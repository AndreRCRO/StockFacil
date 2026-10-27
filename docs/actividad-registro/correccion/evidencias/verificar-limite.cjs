const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'C:/Users/andre/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage({ viewport: { width: 1280, height: 850 } });
    const results = { at: new Date().toISOString(), base: 'http://127.0.0.1:8006', cache: 'file', requests: [] };
    try {
        await page.goto(results.base + '/register');
        const token = await page.locator('input[name="_token"]').inputValue();
        for (let attempt = 1; attempt <= 11; attempt++) {
            const response = await page.request.post(results.base + '/register', { maxRedirects: 0, form: { _token: token, name: '', email: 'limite@example.test', password: 'abc12345', password_confirmation: 'abc12345' } });
            results.requests.push({ attempt, status: response.status() });
            if (response.status() === 429) break;
            assert.equal(response.status(), 302);
        }
        assert.equal(results.requests.at(-1).status, 429);
        await page.locator('form').evaluate(form => { form.noValidate = true; });
        await page.getByRole('button', { name: 'Crear cuenta', exact: true }).click();
        await page.waitForLoadState('networkidle');
        assert((await page.locator('body').innerText()).toLowerCase().includes('too many requests'));
        await page.screenshot({ path: path.join(__dirname, 'limite-429.png'), fullPage: true });
        results.status = 'aprobado';
        results.observed = 'HTTP 429 en solicitudes separadas con caché file; no se crearon cuentas.';
    } catch (error) {
        results.status = 'fallido'; results.observed = error.message; process.exitCode = 1;
    } finally {
        fs.writeFileSync(path.join(__dirname, 'limite-persistente.json'), JSON.stringify(results, null, 2));
        await browser.close();
    }
    console.log(JSON.stringify(results, null, 2));
})();
