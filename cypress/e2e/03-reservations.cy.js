describe('Reservations', () => {
  beforeEach(() => {
    // Login before each test
    cy.visit('/auth/login')
    cy.get('input[name="email"]').type(Cypress.env('testMemberEmail'))
    cy.get('input[name="password"]').type(Cypress.env('testMemberPassword'))
    cy.get('button[type="submit"]').click()
    cy.url().should('eq', Cypress.config().baseUrl + '/')
  })

  it('should open booking modal when clicking available slot', () => {
    // Wait for grid to load
    cy.get('#grid-body').should('not.contain', 'Lade Verfügbarkeit')
    
    // Click on an available (green) slot
    cy.get('.bg-green-500').first().click()
    
    // Modal should be visible
    cy.get('#booking-modal').should('not.have.class', 'hidden')
    cy.contains('Buchung erstellen')
    cy.get('#booking-date').should('be.visible')
    cy.get('#booking-court').should('be.visible')
    cy.get('#booking-time').should('be.visible')
    cy.get('#booking-for').should('be.visible')
  })

  it('should close booking modal when clicking cancel', () => {
    // Open modal
    cy.get('.bg-green-500').first().click()
    cy.get('#booking-modal').should('not.have.class', 'hidden')
    
    // Click cancel
    cy.contains('button', 'Abbrechen').click()
    
    // Modal should be hidden
    cy.get('#booking-modal').should('have.class', 'hidden')
  })

  it('should create a reservation', () => {
    // Wait for grid to load
    cy.get('#grid-body').should('not.contain', 'Lade Verfügbarkeit')
    
    // Click on an available slot
    cy.get('.bg-green-500').first().click()
    
    // Fill form and submit
    cy.get('#booking-for').select(0) // Select first option (self)
    cy.contains('button', 'Buchung bestätigen').click()
    
    // Should show success message
    cy.contains('Buchung erfolgreich erstellt', { timeout: 10000 })
    
    // Modal should close
    cy.get('#booking-modal').should('have.class', 'hidden')
  })

  it('should display reservations list', () => {
    cy.visit('/reservations/')
    cy.contains('Meine Buchungen')
  })

  it('should navigate to reservations page from dashboard', () => {
    cy.contains('a', 'Meine Buchungen').click()
    cy.url().should('include', '/reservations')
  })
})
