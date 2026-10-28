import { defineConfig } from 'cypress';

export default defineConfig({
    video: false,
    screenshotOnRunFailure: true,
    screenshotsFolder: 'docs/evidencias/cypress',
    reporter: 'junit',
    reporterOptions: { mochaFile: 'docs/evidencias/cypress-[hash].xml', toConsole: true },
    viewportWidth: 1366,
    viewportHeight: 900,
    e2e: {
        baseUrl: 'http://127.0.0.1:8015',
        specPattern: 'cypress/e2e/**/*.cy.js',
        supportFile: false,
    },
});
