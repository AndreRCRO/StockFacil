const login = () => {
    cy.visit('/login');
    cy.get('#email').type('sqa@example.test');
    cy.get('#password').type('SqaDemo2026!', { log: false });
    cy.get('form[data-submit-form] button[type=submit]').click();
    cy.location('pathname').should('eq', '/dashboard');
};
const product = (sku, stock = '10') => {
    cy.visit('/products/create');
    cy.get('#name').type(`Producto ${sku}`);
    cy.get('#sku').type(sku);
    cy.get('#category_id').select('Bebidas');
    cy.get('#price').clear().type('8.50');
    cy.get('#minimum_stock').clear().type('3');
    cy.get('#initial_stock').clear().type(stock);
    cy.get('form[data-submit-form] button[type=submit]').click();
    cy.location('pathname').should('eq', '/products');
    cy.visit(`/products?q=${sku}`);
};

describe('Aceptación de inventario StockFácil', () => {
    beforeEach(login);

    it('CP-03 y CP-04 crea producto con stock y rechaza SKU duplicado', () => {
        product('CY-ALTA');
        cy.contains('tr', 'CY-ALTA').should('contain.text', 'Producto CY-ALTA').and('contain.text', '10');
        cy.screenshot('CP-03-producto-creado');
        cy.visit('/products/create');
        cy.get('#name').type('Producto duplicado');
        cy.get('#sku').type('cy-alta');
        cy.get('#category_id').select('Bebidas');
        cy.get('#price').type('8.50');
        cy.get('form[data-submit-form] button[type=submit]').click();
        cy.get('#sku-error').should('be.visible').and('contain.text', 'SKU');
        cy.screenshot('CP-04-sku-duplicado');
        cy.visit('/products?q=CY-ALTA');
        cy.get('tbody tr').should('have.length', 1);
    });

    it('CP-06 rechaza salida superior al saldo y conserva stock e historial', () => {
        product('CY-SALDO');
        cy.visit('/movements/create');
        cy.get('#product_id option').contains('CY-SALDO').then(option => {
            const id = option.val();
            cy.get('#product_id').select(id);
            cy.get('input[value=salida]').check();
            cy.get('#quantity').type('11');
            cy.get('#note').type('INTENTO-RECHAZADO-CY');
            cy.get('form[data-submit-form] button[type=submit]').click();
            cy.get('#quantity-error').should('contain.text', 'Stock insuficiente');
            cy.screenshot('CP-06-stock-insuficiente');
            cy.visit(`/movements?product_id=${id}`);
            cy.get('tbody tr').should('have.length', 1).and('contain.text', 'Stock inicial');
            cy.contains('INTENTO-RECHAZADO-CY').should('not.exist');
        });
        cy.visit('/products?q=CY-SALDO');
        cy.contains('tr', 'CY-SALDO').find('td').eq(3).find('strong').should('have.text', '10');
    });

    it('CP-05 registra entrada y CP-07 salida al mínimo con alerta e historial', () => {
        product('CY-MOV');
        cy.visit('/movements/create');
        cy.get('#product_id option').contains('CY-MOV').then(option => {
            const id = option.val();
            cy.get('#product_id').select(id);
            cy.get('#quantity').type('5');
            cy.get('#note').type('ENTRADA-CY-5');
            cy.get('form[data-submit-form] button[type=submit]').click();
            cy.location('pathname').should('eq', '/movements');
            cy.contains('tr', 'ENTRADA-CY-5').should('contain.text', '15');
            cy.screenshot('CP-05-entrada');
            cy.visit(`/movements/create?product_id=${id}&type=salida`);
            cy.get('#quantity').type('12');
            cy.get('#note').type('SALIDA-CY-12');
            cy.get('form[data-submit-form] button[type=submit]').click();
            cy.contains('tr', 'SALIDA-CY-12').should('contain.text', '15').and('contain.text', '3');
            cy.visit('/stock-bajo');
            cy.contains('tr', 'CY-MOV').should('contain.text', 'Stock bajo');
            cy.screenshot('CP-07-alerta-minimo');
        });
    });
});

