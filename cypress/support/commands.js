// Custom Cypress commands for Tennis Club Reservation System

/**
 * Login command
 * @example cy.login('admin@tennisclub.de', 'admin123')
 */
Cypress.Commands.add('login', (email, password) => {
  cy.visit('/auth/login')
  cy.get('input[name="email"]').type(email)
  cy.get('input[name="password"]').type(password)
  cy.get('button[type="submit"]').click()
  cy.url().should('eq', Cypress.config().baseUrl + '/')
})

/**
 * Login as admin
 * @example cy.loginAsAdmin()
 */
Cypress.Commands.add('loginAsAdmin', () => {
  cy.login(Cypress.env('adminEmail'), Cypress.env('adminPassword'))
})

/**
 * Login as test member
 * @example cy.loginAsMember()
 */
Cypress.Commands.add('loginAsMember', () => {
  cy.login(Cypress.env('testMemberEmail'), Cypress.env('testMemberPassword'))
})

/**
 * Wait for grid to load
 * @example cy.waitForGrid()
 */
Cypress.Commands.add('waitForGrid', () => {
  cy.get('#grid-body').should('not.contain', 'Lade Verfügbarkeit')
  cy.get('#grid-body tr').should('have.length.gt', 0)
})

/**
 * Select a date on the dashboard
 * @example cy.selectDate('2025-12-05')
 */
Cypress.Commands.add('selectDate', (dateString) => {
  cy.get('#date-selector').clear().type(dateString)
  cy.waitForGrid()
})

/**
 * Navigate days forward or backward
 * @example cy.navigateDays(1) // next day
 * @example cy.navigateDays(-1) // previous day
 */
Cypress.Commands.add('navigateDays', (offset) => {
  const button = offset > 0 ? '→' : '←'
  const times = Math.abs(offset)
  
  for (let i = 0; i < times; i++) {
    cy.contains('button', button).click()
    cy.wait(500) // Wait for grid to update
  }
})

/**
 * Go to today
 * @example cy.goToToday()
 */
Cypress.Commands.add('goToToday', () => {
  cy.contains('button', 'Heute').click()
  cy.waitForGrid()
})
