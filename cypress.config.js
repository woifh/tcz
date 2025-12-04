const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://127.0.0.1:5000',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false,
    screenshotOnRunFailure: true,
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
  env: {
    adminEmail: 'admin@tennisclub.de',
    adminPassword: 'admin123',
    testMemberEmail: 'anna.schmidt@tennisclub.de',
    testMemberPassword: 'member123',
  },
})
