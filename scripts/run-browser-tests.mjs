import { spawn, spawnSync } from 'node:child_process';
import { randomBytes } from 'node:crypto';
import { createServer } from 'node:net';
import { mkdirSync, openSync, closeSync, createWriteStream } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const tool = process.argv[2];
if (!['cypress', 'selenium'].includes(tool)) throw new Error('Usa cypress o selenium.');
const evidence = path.join(root, 'docs/evidencias');
const temporary = path.join(root, 'tmp/sqa-e2e');
mkdirSync(evidence, { recursive: true });
mkdirSync(temporary, { recursive: true });
const database = path.join(temporary, `${tool}-${Date.now()}-${randomBytes(4).toString('hex')}.sqlite`);
closeSync(openSync(database, 'wx'));
const port = await new Promise((resolve, reject) => {
    const socket = createServer();
    socket.on('error', reject);
    socket.listen(0, '127.0.0.1', () => {
        const address = socket.address();
        socket.close(() => resolve(address.port));
    });
});
const baseUrl = `http://127.0.0.1:${port}`;
const env = {
    ...process.env, APP_ENV: 'sqa', APP_DEBUG: 'false', APP_URL: baseUrl,
    APP_KEY: `base64:${randomBytes(32).toString('base64')}`,
    APP_CONFIG_CACHE: path.join(temporary, 'no-config-cache.php'),
    DB_CONNECTION: 'sqlite', DB_DATABASE: database, DB_URL: '',
    SESSION_DRIVER: 'database', SESSION_DOMAIN: '', CACHE_STORE: 'database',
    QUEUE_CONNECTION: 'sync', MAIL_MAILER: 'array', BCRYPT_ROUNDS: '4',
    LOG_CHANNEL: 'stderr', ADMIN_EMAIL: 'sqa@example.test',
    ADMIN_NAME: 'Administrador SQA', ADMIN_PASSWORD: 'SqaDemo2026!',
    SQA_BASE_URL: baseUrl, CYPRESS_BASE_URL: baseUrl,
};
const preparation = spawnSync('php', ['artisan', 'migrate', '--seed', '--force', '--no-interaction'], {
    cwd: root, env, encoding: 'utf8',
});
process.stdout.write(preparation.stdout || '');
process.stderr.write(preparation.stderr || '');
if (preparation.status !== 0) process.exit(preparation.status || 1);
const serverLog = createWriteStream(path.join(evidence, `${tool}-servidor.txt`));
const server = spawn('php', ['-S', `127.0.0.1:${port}`,
    path.join(root, 'vendor/laravel/framework/src/Illuminate/Foundation/resources/server.php')], {
    cwd: path.join(root, 'public'), env, stdio: ['ignore', 'pipe', 'pipe'],
});
server.stdout.pipe(serverLog);
server.stderr.pipe(serverLog);
server.on('error', error => console.error(error.message));
let ready = false;
try {
    for (let attempt = 0; attempt < 60; attempt++) {
        try {
            const response = await fetch(`${baseUrl}/login`, { signal: AbortSignal.timeout(1000) });
            if (response.ok) { ready = true; break; }
        } catch { /* El servidor todavía está iniciando. */ }
        await new Promise(resolve => setTimeout(resolve, 250));
    }
    if (!ready) throw new Error(`El servidor aislado no respondió: ${baseUrl}/login`);
    const args = tool === 'cypress'
        ? [path.join(root, 'node_modules/cypress/bin/cypress'), 'run', '--browser', process.env.SQA_CYPRESS_BROWSER || 'electron']
        : [path.join(root, 'tests/Browser/selenium.mjs')];
    const test = spawn(process.execPath, args, { cwd: root, env, stdio: 'inherit' });
    process.exitCode = await new Promise((resolve, reject) => {
        test.on('error', reject);
        test.on('exit', code => resolve(code ?? 1));
    });
} finally {
    server.kill();
    await new Promise(resolve => server.exitCode !== null ? resolve() : server.once('exit', resolve));
    serverLog.end();
}
