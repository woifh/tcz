describe('Dashboard', () => {
  beforeEach(() => {
    // Login before each test
    cy.visit('/auth/login')
    cy.get('input[name="email"]').type(Cypress.env('testMemberEmail'))
    cy.get('input[name="password"]').type(Cypress.env('testMemberPassword'))
    cy.get('button[type="submit"]').click()
    cy.url().should('eq', Cypress.config().baseUrl + '/')
  })

  it('should display dashboard with court grid', () => {
    cy.contains('Platzübersicht')
    cy.get('#availability-grid').should('be.visible')
    cy.contains('Platz 1')
    cy.contains('Platz 6')
  })

  it('should display time slots from 06:00 to 21:00', () => {
    cy.contains('06:00')
    cy.contains('21:00')
  })

  it('should display legend', () => {
    cy.contains('Verfügbar')
    cy.contains('Gebucht')
    cy.contains('Gesperrt')
  })

  it('should display date selector with navigation arrows', () => {
    cy.get('#date-selector').should('be.visible')
    cy.contains('button', '←').should('be.visible')
    cy.contains('button', '→').should('be.visible')
    cy.contains('button', 'Heute').should('be.visible')
  })

  it('should navigate to next day', () => {
    const today = new Date().toISOString().split('T')[0]
    cy.get('#date-selector').should('have.value', today)
    
    cy.contains('button', '→').click()
    
    const tomorrow = new Date()
    tomorrow.setDate(tomorrow.getDate() + 1)
    const tomorrowStr = tomorrow.toISOString().split('T')[0]
    cy.get('#date-selector').should('have.value', tomorrowStr)
  })

  it('should navigate to previous day', () => {
    const today = new Date().toISOString().split('T')[0]
    cy.get('#date-selector').should('have.value', today)
    
    cy.contains('button', '←').click()
    
    const yesterday = new Date()
    yesterday.setDate(yesterday.getDate() - 1)
    const yesterdayStr = yesterday.toISOString().split('T')[0]
    cy.get('#date-selector').should('have.value', yesterdayStr)
  })

  it('should return to today when clicking Heute button', () => {
    // Navigate away from today
    cy.contains('button', '→').click()
    
    // Click Heute button
    cy.contains('button', 'Heute').click()
    
    const today = new Date().toISOString().split('T')[0]
    cy.get('#date-selector').should('have.value', today)
  })

  it('should display user reservations section', () => {
    cy.contains('Meine kommenden Buchungen')
    cy.contains('Alle anzeigen')
  })
})
