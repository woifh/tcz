// Import commands
import './commands'

// Disable uncaught exception handling for cleaner test output
Cypress.on('uncaught:exception', (err, runnable) => {
  // returning false here prevents Cypress from failing the test
  return false
})
