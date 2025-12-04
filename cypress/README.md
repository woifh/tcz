# Cypress E2E Tests - Tennis Club Reservation System

## Overview

This directory contains end-to-end tests for the Tennis Club Reservation System using Cypress.

## Setup

### Install Dependencies

```bash
npm install
```

This will install Cypress and other required dependencies.

### Configuration

Test configuration is in `cypress.config.js`. Default settings:
- Base URL: `http://127.0.0.1:5000`
- Viewport: 1280x720
- Video recording: Disabled
- Screenshots on failure: Enabled

### Environment Variables

Test credentials are configured in `cypress.config.js`:
- Admin: `admin@tennisclub.de` / `admin123`
- Test Member: `anna.schmidt@tennisclub.de` / `member123`

## Running Tests

### Prerequisites

Make sure the Flask application is running:

```bash
python3 -m flask run
```

### Interactive Mode (Cypress Test Runner)

```bash
npm run cypress:open
```

This opens the Cypress Test Runner where you can:
- Select and run individual tests
- Watch tests run in real-time
- Debug test failures
- See detailed logs and network requests

### Headless Mode (CI/CD)

```bash
npm run cypress:run
```

Runs all tests in headless mode, suitable for CI/CD pipelines.

### Headed Mode (See Browser)

```bash
npm run test:e2e:headed
```

Runs tests in headed mode so you can see the browser.

## Test Structure

### Test Files

Tests are organized in `cypress/e2e/`:

1. **01-authentication.cy.js**
   - Login with valid credentials
   - Login with invalid credentials
   - Logout functionality
   - Error handling

2. **02-dashboard.cy.js**
   - Dashboard display
   - Court grid rendering
   - Date navigation (arrows, today button)
   - Time slots display
   - User reservations section

3. **03-reservations.cy.js**
   - Opening booking modal
   - Creating reservations
   - Viewing reservations list
   - Navigation between pages

4. **04-favourites.cy.js**
   - Favourites page navigation
   - Adding favourites
   - Removing favourites
   - Dropdown filtering

### Custom Commands

Custom commands are defined in `cypress/support/commands.js`:

- `cy.login(email, password)` - Login with credentials
- `cy.loginAsAdmin()` - Quick admin login
- `cy.loginAsMember()` - Quick member login
- `cy.waitForGrid()` - Wait for availability grid to load
- `cy.selectDate(dateString)` - Select a specific date
- `cy.navigateDays(offset)` - Navigate forward/backward by days
- `cy.goToToday()` - Return to today's date

### Example Usage

```javascript
describe('My Test', () => {
  beforeEach(() => {
    cy.loginAsMember()
  })

  it('should book a court', () => {
    cy.waitForGrid()
    cy.get('.bg-green-500').first().click()
    cy.contains('button', 'Buchung bestätigen').click()
    cy.contains('Buchung erfolgreich erstellt')
  })
})
```

## Test Coverage

### Authentication
- ✅ Login/Logout
- ✅ Invalid credentials
- ✅ Session management

### Dashboard
- ✅ Grid display
- ✅ Date navigation
- ✅ Time slots (06:00-21:00)
- ✅ Legend display
- ✅ User reservations section

### Reservations
- ✅ Booking modal
- ✅ Creating reservations
- ✅ Viewing reservations
- ✅ Navigation

### Favourites
- ✅ Page navigation
- ✅ List display
- ✅ Add/remove functionality
- ✅ Dropdown filtering

## Best Practices

1. **Use Custom Commands**: Leverage custom commands for common actions
2. **Wait for Elements**: Use `cy.waitForGrid()` before interacting with the grid
3. **Descriptive Tests**: Write clear test descriptions
4. **Independent Tests**: Each test should be independent
5. **Clean State**: Use `beforeEach` to set up clean state

## Debugging

### Interactive Debugging

1. Open Cypress Test Runner: `npm run cypress:open`
2. Click on a test file
3. Use the time-travel feature to see each step
4. Inspect DOM, network requests, and console logs

### Screenshots

Failed tests automatically capture screenshots in `cypress/screenshots/`

### Videos

Enable video recording in `cypress.config.js` if needed:

```javascript
video: true
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  cypress:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - uses: actions/setup-python@v4
      
      - name: Install dependencies
        run: |
          npm install
          pip install -r requirements.txt
      
      - name: Start Flask app
        run: python3 -m flask run &
        
      - name: Wait for app
        run: npx wait-on http://127.0.0.1:5000
        
      - name: Run Cypress tests
        run: npm run cypress:run
```

## Troubleshooting

### App Not Running

Make sure Flask is running on port 5000:
```bash
python3 -m flask run
```

### Database Issues

Ensure the database is initialized:
```bash
flask db upgrade
flask init-courts
```

### Port Conflicts

If port 5000 is in use, update `baseUrl` in `cypress.config.js`

## Contributing

When adding new features:
1. Write corresponding Cypress tests
2. Follow existing test structure
3. Use custom commands where appropriate
4. Ensure tests pass before committing

## Resources

- [Cypress Documentation](https://docs.cypress.io/)
- [Best Practices](https://docs.cypress.io/guides/references/best-practices)
- [Custom Commands](https://docs.cypress.io/api/cypress-api/custom-commands)
