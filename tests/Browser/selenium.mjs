import assert from 'node:assert/strict';
import { Builder, By, until } from 'selenium-webdriver';
import chrome from 'selenium-webdriver/chrome.js';
import edge from 'selenium-webdriver/edge.js';
import { mkdirSync, writeFileSync } from 'node:fs';

const browser = process.env.SQA_BROWSER || (process.platform === 'win32' ? 'MicrosoftEdge' : 'chrome');
const options = browser === 'MicrosoftEdge' ? new edge.Options() : new chrome.Options();
options.addArguments('--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--window-size=1366,900');
const builder = new Builder().forBrowser(browser);
if (browser === 'MicrosoftEdge') builder.setEdgeOptions(options);
else builder.setChromeOptions(options);
const results = [];
mkdirSync('docs/evidencias/selenium', { recursive: true });
let driver;
async function capture(file) {
    writeFileSync(`docs/evidencias/selenium/${file}.png`, await driver.takeScreenshot(), 'base64');
}
async function run(id, action) {
    const started = new Date().toISOString();
    try {
        const obtained = await action();
        results.push({ id, status: 'aprobado', obtained, started, finished: new Date().toISOString() });
        console.log(`${id}: aprobado - ${obtained}`);
    } catch (error) {
        results.push({ id, status: 'fallido', obtained: error.message, started, finished: new Date().toISOString() });
        if (driver) await capture(`${id}-fallo`);
        throw error;
    }
}
try {
    driver = await builder.build();
    await driver.manage().setTimeouts({ implicit: 0, pageLoad: 30000 });
    await run('CP-02', async () => {
        await driver.get(`${process.env.SQA_BASE_URL}/dashboard`);
        await driver.wait(until.urlContains('/login'), 10000);
        await driver.findElement(By.id('email')).sendKeys('sqa@example.test');
        await driver.findElement(By.id('password')).sendKeys('incorrecta');
        await driver.findElement(By.css('button[type=submit]')).click();
        const error = await driver.wait(until.elementLocated(By.id('email-error')), 10000);
        assert.match(await error.getText(), /no son correctos/);
        assert.match(await driver.getCurrentUrl(), /\/login$/);
        await capture('CP-02-acceso-rechazado');
        return 'Ruta privada redirige a login y las credenciales inválidas muestran error sin abrir sesión.';
    });
    await run('CP-01', async () => {
        const password = await driver.findElement(By.id('password'));
        await password.clear();
        await password.sendKeys('SqaDemo2026!');
        await driver.findElement(By.css('button[type=submit]')).click();
        await driver.wait(until.urlContains('/dashboard'), 10000);
        assert.match(await driver.findElement(By.css('h1')).getText(), /Tu inventario/);
        await capture('CP-01-dashboard');
        await driver.findElement(By.css('form[action$="/logout"] button')).click();
        await driver.wait(until.urlContains('/login'), 10000);
        await driver.get(`${process.env.SQA_BASE_URL}/products`);
        await driver.wait(until.urlContains('/login'), 10000);
        return 'Login válido abre el dashboard; logout impide volver al catálogo sin autenticarse.';
    });
} finally {
    writeFileSync('docs/evidencias/selenium-resultados.json', JSON.stringify({
        tool: 'Selenium WebDriver', browser, automated: true, results,
    }, null, 2));
    if (driver) await driver.quit();
}
