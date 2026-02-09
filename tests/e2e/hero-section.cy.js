// hero-section.cy.js
// End-to-end tests for the hero section responsive behavior

describe('Hero Section Responsive Behavior', () => {
  beforeEach(() => {
    // Visit the page containing the hero section
    cy.visit('/'); // Adjust path as needed
  });

  it('maintains proper centering on mobile screens', () => {
    // Test mobile viewport
    cy.viewport('iphone-6');
    cy.get('[data-testid="hero-section"]').should('be.visible');
    
    // Check that input elements are centered
    cy.get('[data-testid="input-container"]')
      .should('have.css', 'display', 'flex')
      .and('have.css', 'justify-content', 'center');
  });

  it('maintains proper centering on tablet screens', () => {
    // Test tablet viewport
    cy.viewport('ipad-2');
    cy.get('[data-testid="hero-section"]').should('be.visible');
    
    // Check that input elements are centered
    cy.get('[data-testid="input-container"]')
      .should('have.css', 'display', 'flex')
      .and('have.css', 'justify-content', 'center');
  });

  it('maintains proper centering on desktop screens', () => {
    // Test desktop viewport
    cy.viewport('macbook-13');
    cy.get('[data-testid="hero-section"]').should('be.visible');
    
    // Check that input elements are centered
    cy.get('[data-testid="input-container"]')
      .should('have.css', 'display', 'flex')
      .and('have.css', 'justify-content', 'center');
  });

  it('validates input properly', () => {
    cy.get('input[type="text"]').type('ab'); // Valid input
    cy.get('button[type="submit"]').click();
    
    // Should not show error
    cy.get('.validation-error').should('not.exist');
    
    cy.get('input[type="text"]').clear().type('x'); // Invalid input
    cy.get('button[type="submit"]').click();
    
    // Should show error
    cy.get('.validation-error').should('be.visible');
  });

  it('loads images efficiently', () => {
    // Test that images load without errors
    cy.get('img').should('have.prop', 'naturalWidth').should('be.greaterThan', 0);
  });
});