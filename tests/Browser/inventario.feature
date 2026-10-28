# language: es
Característica: Inventario verificable de StockFácil
  Los escenarios describen aceptación y se vinculan a las pruebas reales.
  Este archivo es especificación BDD; no se ejecuta mediante Cucumber.

  @CP-01 @CP-02
  Escenario: Autenticar al administrador y proteger las rutas privadas
    Dado un administrador SQA y una ruta privada
    Cuando introduce credenciales válidas y después cierra sesión
    Entonces accede al resumen y debe autenticarse para volver al catálogo

  @CP-03 @CP-04
  Escenario: Registrar un producto sin duplicar su SKU
    Dado un administrador autenticado y categorías existentes
    Cuando registra un producto con SKU CY-ALTA e intenta repetirlo en minúsculas
    Entonces el primer producto conserva diez unidades y el segundo registro es rechazado

  @CP-05 @CP-06 @CP-07
  Escenario: Mantener el saldo y alertar en el mínimo
    Dado un producto con diez unidades y mínimo de tres
    Cuando entra cinco unidades y sale doce unidades
    Entonces el saldo es tres y aparece Stock bajo con historial trazable
    Y una salida superior al saldo es rechazada sin cambiar stock ni historial
