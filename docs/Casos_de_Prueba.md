# Casos de prueba de StockFácil

Fecha 27 de octubre de 2026. Ocho casos funcionales críticos automatizados y una exploración manual pendiente. Cada caso agrupa comprobaciones relacionadas; no equivale a una prueba individual de PHPUnit. Los resultados corresponden a la ejecución final, conservando fallos intermedios de automatización.

| ID | Funcionalidad | Estado técnico | Prioridad | Tarea |
| --- | --- | --- | --- | --- |
| CP-01 | Autenticación | Aprobado | Crítica | K-02 |
| CP-02 | Autenticación | Aprobado | Crítica | K-02 |
| CP-03 | Catálogo | Aprobado | Crítica | K-03 |
| CP-04 | Catálogo | Aprobado | Alta | K-03 |
| CP-05 | Movimientos | Aprobado | Crítica | K-04 |
| CP-06 | Movimientos | Aprobado | Crítica | K-04 |
| CP-07 | Movimientos y alertas | Aprobado | Alta | K-04 |
| CP-08 | Movimientos | Aprobado | Crítica | K-04 |

## CP-01

**Funcionalidad:** Autenticación

**Historia o requisito:** HU-03 Acceder al inventario

**Objetivo:** Iniciar y cerrar sesión de forma verificable.

**Precondiciones:** Servidor SQA aislado; cuenta sqa@example.test disponible; sesión cerrada.

**Datos de entrada:** Correo sqa@example.test y contraseña de fixture SqaDemo2026!.

**Pasos:** Abrir login, completar credenciales, enviar, comprobar dashboard, cerrar sesión e intentar abrir /products.

**Resultado esperado:** Login redirige a dashboard; logout redirige a login y bloquea /products.

**Resultado obtenido:** Selenium comprobó ambas redirecciones y el encabezado del dashboard.

**Estado:** Aprobado automatizado. **Prioridad:** Crítica. **Tarea preparada:** K-02.

**Evidencia:** docs/evidencias/selenium-resultados.json; selenium/CP-01-dashboard.png; AuthenticationTest::test_login_and_logout.


## CP-02

**Funcionalidad:** Autenticación

**Historia o requisito:** HU-03 Proteger rutas y rechazar credenciales incorrectas

**Objetivo:** Evitar acceso sin autenticación.

**Precondiciones:** Mismo entorno; cuenta existente; sesión cerrada.

**Datos de entrada:** GET /dashboard; correo SQA y contraseña incorrecta.

**Pasos:** Abrir /dashboard sin sesión; comprobar /login; enviar contraseña incorrecta y leer error.

**Resultado esperado:** La ruta privada exige login y la contraseña incorrecta no autentica.

**Resultado obtenido:** Selenium observó /login y el mensaje de credenciales incorrectas; PHPUnit comprobó rutas privadas.

**Estado:** Aprobado automatizado. **Prioridad:** Crítica. **Tarea preparada:** K-02.

**Evidencia:** docs/evidencias/selenium-resultados.json; selenium/CP-02-acceso-rechazado.png; AuthenticationTest::test_internal_routes_require_authentication.


## CP-03

**Funcionalidad:** Catálogo

**Historia o requisito:** HU-01 Registrar productos CA-01 a CA-05

**Objetivo:** Crear un producto con stock inicial trazable.

**Precondiciones:** Administrador autenticado; categoría Bebidas; SKU CY-ALTA inexistente.

**Datos de entrada:** Nombre Producto CY-ALTA; SKU CY-ALTA; precio 8.50; stock 10; mínimo 3.

**Pasos:** Completar /products/create, enviar y filtrar /products?q=CY-ALTA; verificar fila. PHPUnit consulta producto y movimiento.

**Resultado esperado:** Un producto con diez unidades, precio 8.50 y movimiento inicial de 0 a 10 del responsable.

**Resultado obtenido:** Cypress verificó la fila; PHPUnit verificó stock, precio, saldo inicial, saldo final y responsable.

**Estado:** Aprobado automatizado. **Prioridad:** Crítica. **Tarea preparada:** K-03.

**Evidencia:** docs/evidencias/cypress/inventario.cy.js/CP-03-producto-creado.png; phpunit-final.xml; ProductTest::test_valid_product_appears_in_listing_with_traceable_initial_stock.


## CP-04

**Funcionalidad:** Catálogo

**Historia o requisito:** HU-01 SKU único CA-02

**Objetivo:** Rechazar duplicación tras normalizar mayúsculas.

**Precondiciones:** CP-03 creó CY-ALTA en la misma ejecución; administrador autenticado.

**Datos de entrada:** Nuevo nombre, SKU cy-alta, categoría Bebidas y precio 8.50.

**Pasos:** Enviar segundo formulario y comprobar #sku-error; filtrar CY-ALTA y contar filas.

**Resultado esperado:** Error de SKU; solo un producto con ese código.

**Resultado obtenido:** Cypress comprobó el error y una sola fila; PHPUnit comprobó un solo registro persistido.

**Estado:** Aprobado automatizado. **Prioridad:** Alta. **Tarea preparada:** K-03.

**Evidencia:** docs/evidencias/cypress/inventario.cy.js/CP-04-sku-duplicado.png; ProductTest::test_duplicate_sku_is_rejected_even_with_lowercase.


## CP-05

**Funcionalidad:** Movimientos

**Historia o requisito:** HU-02 Entradas CA-01 y trazabilidad CA-05

**Objetivo:** Incrementar existencias y registrar historial.

**Precondiciones:** Producto CY-MOV con stock 10; mínimo 3; administrador autenticado.

**Datos de entrada:** Entrada de 5; observación ENTRADA-CY-5.

**Pasos:** Seleccionar producto, enviar entrada y verificar fila del historial. PHPUnit comprueba base y responsable.

**Resultado esperado:** Saldo 15, movimiento entrada 10 a 15 y responsable del registro.

**Resultado obtenido:** Cypress observó 15 en la fila; PHPUnit verificó tipo, cantidad, saldos y usuario.

**Estado:** Aprobado automatizado. **Prioridad:** Crítica. **Tarea preparada:** K-04.

**Evidencia:** docs/evidencias/cypress/inventario.cy.js/CP-05-entrada.png; InventoryTest::test_entry_increases_stock_and_records_history.


## CP-06

**Funcionalidad:** Movimientos

**Historia o requisito:** HU-02 Evitar saldo negativo CA-03

**Objetivo:** Rechazar una salida superior al saldo sin efectos parciales.

**Precondiciones:** Producto CY-SALDO creado con stock 10 y un movimiento inicial.

**Datos de entrada:** Salida de 11; observación INTENTO-RECHAZADO-CY.

**Pasos:** Enviar salida; comprobar error; consultar historial filtrado y catálogo filtrado.

**Resultado esperado:** Stock insuficiente, saldo 10 e historial con una sola entrada inicial.

**Resultado obtenido:** Cypress verificó error, stock 10, historial de una fila y ausencia de la observación rechazada; PHPUnit verificó saldo y cantidad de movimientos.

**Estado:** Aprobado automatizado. **Prioridad:** Crítica. **Tarea preparada:** K-04.

**Evidencia:** docs/evidencias/cypress/inventario.cy.js/CP-06-stock-insuficiente.png; InventoryTest::test_insufficient_stock_preserves_balance_and_history.


## CP-07

**Funcionalidad:** Movimientos y alertas

**Historia o requisito:** HU-02 Salidas CA-02 y alertas CA-06

**Objetivo:** Alertar cuando el saldo llega al mínimo exacto.

**Precondiciones:** Producto CY-MOV con saldo 15 tras CP-05 y mínimo 3.

**Datos de entrada:** Salida de 12; observación SALIDA-CY-12.

**Pasos:** Enviar salida, verificar fila con saldos 15 y 3 y abrir /stock-bajo.

**Resultado esperado:** Saldo 3, movimiento persistido y estado Stock bajo.

**Resultado obtenido:** Cypress verificó saldos e inclusión en alertas; PHPUnit y cuatro datos unitarios verificaron los límites del estado.

**Estado:** Aprobado automatizado. **Prioridad:** Alta. **Tarea preparada:** K-04.

**Evidencia:** docs/evidencias/cypress/inventario.cy.js/CP-07-alerta-minimo.png; InventoryTest::test_exit_decreases_stock_and_alert_appears_at_exact_minimum; ProductStockStatusTest.


## CP-08

**Funcionalidad:** Movimientos

**Historia o requisito:** HU-02 Validar cantidades CA-04

**Objetivo:** Rechazar valores no enteros positivos en el servidor.

**Precondiciones:** Prueba PHPUnit con SQLite en memoria; producto con stock 10 y una entrada inicial.

**Datos de entrada:** Cantidad 0, -1, 1.5, abc y null, mediante proveedor invalidMovements.

**Pasos:** Ejecutar InventoryTest::test_invalid_movement_is_rejected; enviar cada dato; verificar errores, stock e historial.

**Resultado esperado:** Error de quantity, saldo 10 y un solo movimiento inicial para cada variante.

**Resultado obtenido:** Todas las variantes aprobaron en phpunit-final.xml; se comprobaron errores, stock e historial.

**Estado:** Aprobado automatizado. **Prioridad:** Crítica. **Tarea preparada:** K-04.

**Evidencia:** docs/evidencias/phpunit-final.xml; InventoryTest::test_invalid_movement_is_rejected.

## MAN-01 Exploración y aceptación humana

**Objetivo:** comprobar comprensión, navegación y respuesta visual en escritorio y móvil. **Responsable propuesto:** Santiago, con revisión de Andre. **Prioridad:** alta. **Estado:** no ejecutado; requiere interacción y valoración humana real.

**Precondiciones y datos:** usar instalación local o base de demostración desechable; nunca alterar inventario real para practicar. Cuenta de demo, producto nuevo con SKU MAN-01, stock 10 y mínimo 3.

**Pasos:** 1. Abrir login en escritorio y tamaño móvil de 390 píxeles. 2. Navegar con Tab y verificar foco visible y etiquetas. 3. Acceder y abrir/cerrar menú móvil. 4. Crear producto, provocar un campo requerido y revisar mensajes. 5. Registrar entrada y salida y comprobar historial. 6. Cerrar sesión y verificar protección de rutas. 7. Registrar fecha real, navegador, observaciones y captura propia.

**Esperado:** navegación usable, sin superposición, errores comprensibles y saldos coherentes. **Obtenido:** sin ejecución humana registrada. **Evidencia:** pendiente; no se reutiliza una captura automatizada como sesión manual. **Tarea:** K-11.

## Reproducir la automatización

Desde la raíz: `php vendor/phpunit/phpunit/phpunit --colors=never`, `npm run build`, `npm run test:selenium` y `npm run test:cypress`. El ejecutor de navegador crea SQLite nuevo, migra, carga fixtures, arranca PHP en puerto libre y lo detiene al acabar. El correo y contraseña anteriores son datos sintéticos de prueba, no credenciales de la cuenta GitHub.
