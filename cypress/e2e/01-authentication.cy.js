describe('Authentication', () => {
  beforeEach(() => {
    cy.visit('/auth/login')
  })

  it('should display login page', () => {
    cy.contains('Anmelden')
    cy.get('input[name="email"]').should('be.visible')
    cy.get('input[name="password"]').should('be.visible')
  })

  it('should login with valid admin credentials', () => {
    cy.get('input[name="email"]').type(Cypress.env('adminEmail'))
    cy.get('input[name="password"]').type(Cypress.env('adminPassword'))
    cy.get('button[type="submit"]').click()
    
    cy.url().should('eq', Cypress.config().baseUrl + '/')
    cy.contains('Platzübersicht')
  })

  it('should login with valid member credentials', () => {
    cy.get('input[name="email"]').type(Cypress.env('testMemberEmail'))
    cy.get('input[name="password"]').type(Cypress.env('testMemberPassword'))
    cy.get('button[type="submit"]').click()
    
    cy.url().should('eq', Cypress.config().baseUrl + '/')
    cy.contains('Platzübersicht')
  })

  it('should show error with invalid credentials', () => {
    cy.get('input[name="email"]').type('invalid@test.com')
    cy.get('input[name="password"]').type('wrongpassword')
    cy.get('button[type="submit"]').click()
    
    cy.url().should('include', '/auth/login')
  })

  it('should logout successfully', () => {
    // Login first
    cy.get('input[name="email"]').type(Cypress.env('adminEmail'))
    cy.get('input[name="password"]').type(Cypress.env('adminPassword'))
    cy.get('button[type="submit"]').click()
    
    // Then logout
    cy.contains('Abmelden').click()
    cy.url().should('include', '/auth/login')
  })
})
