# Casos funcionales ejecutados

Los IDs siguientes pertenecen al catálogo SQA de esta actividad. Los casos de navegador usan una instancia con SQLite temporal, producto SQA-001 y administrador de demostración. Las pruebas PHPUnit crean sus propios datos en SQLite en memoria; sus variantes no comparten el estado secuencial del navegador.

Para probar errores del servidor se activó noValidate en los formularios de pruebas negativas. No se alteró el formulario de la aplicación. El navegador seguía enviando peticiones reales con sesión y token CSRF.

## SQA/CP-01: Registrar producto válido

| Campo | Contenido |
| --- | --- |
| Historia | HU-01 |
| Objetivo | Registrar producto válido |
| Precondiciones | Sesión de administrador, categoría Bebidas y SKU SQA-001 libre. |
| Datos de entrada | Nombre Producto SQA - HU01; SKU SQA-001; precio 8,50; inicial 10; mínimo 3. |
| Pasos | Abrir Nuevo producto; completar campos; pulsar Registrar producto. |
| Resultado esperado | Confirmación, persistencia del producto y entrada inicial 0 a 10. |
| Resultado obtenido | Producto registrado. El stock inicial quedó en el historial. |
| Estado | Aprobado |
| Evidencia | [hu01-registro-exitoso.png](evidencias/hu01-registro-exitoso.png); [resultados-navegador.json](evidencias/resultados-navegador.json); [phpunit-junit.xml](evidencias/phpunit-junit.xml) |
| Prueba automática relacionada | test_valid_product_appears_in_listing_with_traceable_initial_stock |

## SQA/CP-02: Rechazar producto sin nombre

| Campo | Contenido |
| --- | --- |
| Historia | HU-01 |
| Objetivo | Rechazar producto sin nombre |
| Precondiciones | Sesión iniciada y formulario disponible. |
| Datos de entrada | Nombre vacío; SKU SQA-INVALID; precio 8,50; inicial 10; mínimo 3. |
| Pasos | Enviar el formulario con nombre vacío, omitiendo solo la validación nativa del navegador. |
| Resultado esperado | Mensaje de nombre obligatorio; sin nuevo producto. |
| Resultado obtenido | El campo nombre es obligatorio. |
| Estado | Aprobado |
| Evidencia | [hu01-error-nombre.png](evidencias/hu01-error-nombre.png); [resultados-navegador.json](evidencias/resultados-navegador.json); [phpunit-junit.xml](evidencias/phpunit-junit.xml) |
| Prueba automática relacionada | test_invalid_product_is_rejected; test_invalid_product_is_rejected with data set #0 |

## SQA/CP-03: Rechazar SKU duplicado

| Campo | Contenido |
| --- | --- |
| Historia | HU-01 |
| Objetivo | Rechazar SKU duplicado |
| Precondiciones | CP-01 creó SQA-001. |
| Datos de entrada | SKU SQA-001; otros campos válidos. |
| Pasos | Abrir Nuevo producto e intentar guardar el SKU existente. |
| Resultado esperado | Mensaje de SKU duplicado; sin duplicación en SQLite. |
| Resultado obtenido | El SKU ya está registrado. Usa otro valor. |
| Estado | Aprobado |
| Evidencia | [hu01-error-sku.png](evidencias/hu01-error-sku.png); [resultados-navegador.json](evidencias/resultados-navegador.json); [phpunit-junit.xml](evidencias/phpunit-junit.xml) |
| Prueba automática relacionada | test_duplicate_sku_is_rejected_even_with_lowercase |

## SQA/CP-04: Rechazar precio negativo

| Campo | Contenido |
| --- | --- |
| Historia | HU-01 |
| Objetivo | Rechazar precio negativo |
| Precondiciones | Sesión iniciada, categoría válida. |
| Datos de entrada | Precio -1; SKU SQA-INVALID; otros campos válidos. |
| Pasos | Enviar el formulario omitiendo validación HTML5 para ejercitar el servidor. |
| Resultado esperado | Mensaje de precio no negativo; producto no persistido. |
| Resultado obtenido | El precio debe ser mayor o igual a 0. |
| Estado | Aprobado |
| Evidencia | [hu01-error-precio.png](evidencias/hu01-error-precio.png); [resultados-navegador.json](evidencias/resultados-navegador.json); [phpunit-junit.xml](evidencias/phpunit-junit.xml) |
| Prueba automática relacionada | test_invalid_product_is_rejected with data set #3 |

## SQA/CP-05: Rechazar stock inicial negativo

| Campo | Contenido |
| --- | --- |
| Historia | HU-01 |
| Objetivo | Rechazar stock inicial negativo |
| Precondiciones | Sesión iniciada, categoría válida. |
| Datos de entrada | Stock inicial -1; SKU SQA-INVALID; otros campos válidos. |
| Pasos | Enviar el formulario omitiendo validación HTML5 para ejercitar el servidor. |
| Resultado esperado | Mensaje de stock inicial no negativo; sin producto ni movimiento. |
| Resultado obtenido | El stock inicial debe ser mayor o igual a 0. |
| Estado | Aprobado |
| Evidencia | [hu01-error-stock-inicial.png](evidencias/hu01-error-stock-inicial.png); [resultados-navegador.json](evidencias/resultados-navegador.json); [phpunit-junit.xml](evidencias/phpunit-junit.xml) |
| Prueba automática relacionada | test_invalid_product_is_rejected with data set #6 |

## SQA/CP-06: Localizar producto guardado

| Campo | Contenido |
| --- | --- |
| Historia | HU-01 |
| Objetivo | Localizar producto guardado |
| Precondiciones | CP-01 aprobado; errores previos no añadieron productos. |
| Datos de entrada | Filtro de búsqueda SQA-001. |
| Pasos | Abrir Productos, buscar el SKU y comprobar la fila. |
| Resultado esperado | Una fila con nombre, SKU, precio y stock 10. |
| Resultado obtenido | Producto SQA-001 visible en el listado filtrado, Bs 8,50 y stock 10. |
| Estado | Aprobado |
| Evidencia | [hu01-producto-listado.png](evidencias/hu01-producto-listado.png); [resultados-navegador.json](evidencias/resultados-navegador.json); [phpunit-junit.xml](evidencias/phpunit-junit.xml) |
| Prueba automática relacionada | test_valid_product_appears_in_listing_with_traceable_initial_stock |

## SQA/CP-07: Visualizar errores de validación

| Campo | Contenido |
| --- | --- |
| Historia | HU-01 |
| Objetivo | Visualizar errores de validación |
| Precondiciones | Sesión iniciada y formulario disponible. |
| Datos de entrada | Nombre vacío; SKU SQA-ERROR; otros campos válidos. |
| Pasos | Enviar, comprobar resumen de errores, mensaje junto al nombre, aria-invalid y conservación del SKU. |
| Resultado esperado | Errores visibles y entrada válida recuperada. |
| Resultado obtenido | Resumen y mensaje junto al nombre visibles; SKU conservado y aria-invalid=true. |
| Estado | Aprobado |
| Evidencia | [hu01-mensajes-validacion.png](evidencias/hu01-mensajes-validacion.png); [resultados-navegador.json](evidencias/resultados-navegador.json); [phpunit-junit.xml](evidencias/phpunit-junit.xml) |
| Prueba automática relacionada | test_invalid_product_is_rejected |

## SQA/CP-08: Registrar entrada válida

| Campo | Contenido |
| --- | --- |
| Historia | HU-02 |
| Objetivo | Registrar entrada válida |
| Precondiciones | Producto SQA-001 activo con stock 10. |
| Datos de entrada | Entrada 5; observación Entrada SQA CP-08. |
| Pasos | Abrir movimiento del producto; verificar preview 15; guardar. |
| Resultado esperado | Stock 15 y movimiento de 10 a 15. |
| Resultado obtenido | Entrada de 5 aceptada; historial muestra stock 10 a 15. |
| Estado | Aprobado |
| Evidencia | [hu02-entrada-exitosa.png](evidencias/hu02-entrada-exitosa.png); [resultados-navegador.json](evidencias/resultados-navegador.json); [phpunit-junit.xml](evidencias/phpunit-junit.xml) |
| Prueba automática relacionada | test_entry_increases_stock_and_records_history; test_exit_decreases_stock_and_alert_appears_at_exact_minimum |

## SQA/CP-09: Registrar salida válida

| Campo | Contenido |
| --- | --- |
| Historia | HU-02 |
| Objetivo | Registrar salida válida |
| Precondiciones | CP-08 aprobado; stock 15. |
| Datos de entrada | Salida 12; observación Salida SQA CP-09. |
| Pasos | Verificar preview 3 y guardar salida. |
| Resultado esperado | Stock 3 y movimiento de 15 a 3. |
| Resultado obtenido | Salida de 12 aceptada; historial muestra stock 15 a 3. |
| Estado | Aprobado |
| Evidencia | [hu02-salida-exitosa.png](evidencias/hu02-salida-exitosa.png); [resultados-navegador.json](evidencias/resultados-navegador.json); [phpunit-junit.xml](evidencias/phpunit-junit.xml) |
| Prueba automática relacionada | test_entry_increases_stock_and_records_history; test_exit_decreases_stock_and_alert_appears_at_exact_minimum |

## SQA/CP-10: Rechazar salida superior al saldo

| Campo | Contenido |
| --- | --- |
| Historia | HU-02 |
| Objetivo | Rechazar salida superior al saldo |
| Precondiciones | CP-09 aprobado; stock 3. |
| Datos de entrada | Salida 4. |
| Pasos | Enviar y comprobar mensaje; volver a consultar el saldo. |
| Resultado esperado | Stock insuficiente; saldo 3 e historial sin cambios. |
| Resultado obtenido | Stock insuficiente. Solo hay 3 unidades disponibles. Saldo conservado: 3. |
| Estado | Aprobado |
| Evidencia | [hu02-error-insuficiente.png](evidencias/hu02-error-insuficiente.png); [resultados-navegador.json](evidencias/resultados-navegador.json); [phpunit-junit.xml](evidencias/phpunit-junit.xml) |
| Prueba automática relacionada | test_insufficient_stock_preserves_balance_and_history |

## SQA/CP-11: Rechazar cantidad cero

| Campo | Contenido |
| --- | --- |
| Historia | HU-02 |
| Objetivo | Rechazar cantidad cero |
| Precondiciones | Producto activo con stock 3. |
| Datos de entrada | Salida 0. |
| Pasos | Enviar sin validación HTML5; leer error y saldo. Repetir después de HR-04. |
| Resultado esperado | Rechazo por cantidad mínima; saldo 3. |
| Resultado obtenido | La cantidad debe ser mayor o igual a 1. Saldo conservado: 3. |
| Estado | Aprobado |
| Evidencia | [hu02-error-cero.png](evidencias/hu02-error-cero.png); [resultados-navegador.json](evidencias/resultados-navegador.json); [phpunit-junit.xml](evidencias/phpunit-junit.xml) |
| Prueba automática relacionada | test_invalid_movement_is_rejected with data set #0; test_invalid_movement_is_rejected with data set #1 |

## SQA/CP-12: Rechazar cantidad negativa

| Campo | Contenido |
| --- | --- |
| Historia | HU-02 |
| Objetivo | Rechazar cantidad negativa |
| Precondiciones | Producto activo con stock 3. |
| Datos de entrada | Salida -1. |
| Pasos | Enviar sin validación HTML5; leer error y saldo. Repetir después de HR-04. |
| Resultado esperado | Rechazo por cantidad mínima; saldo 3. |
| Resultado obtenido | La cantidad debe ser mayor o igual a 1. Saldo conservado: 3. |
| Estado | Aprobado |
| Evidencia | [hu02-error-negativo.png](evidencias/hu02-error-negativo.png); [resultados-navegador.json](evidencias/resultados-navegador.json); [phpunit-junit.xml](evidencias/phpunit-junit.xml) |
| Prueba automática relacionada | test_invalid_movement_is_rejected with data set #0; test_invalid_movement_is_rejected with data set #1 |

## SQA/CP-13: Comprobar historial persistido

| Campo | Contenido |
| --- | --- |
| Historia | HU-02 |
| Objetivo | Comprobar historial persistido |
| Precondiciones | CP-01, CP-08 y CP-09 aprobados; intentos inválidos rechazados. |
| Datos de entrada | Filtro por ID del producto SQA-001. |
| Pasos | Abrir historial filtrado; contar filas y comprobar tipos, saldos, responsable, fechas y notas; contrastar SQLite. |
| Resultado esperado | Tres eventos consecutivos 0 a 10, 10 a 15 y 15 a 3. |
| Resultado obtenido | Tres movimientos: entrada inicial 0 a 10, entrada 10 a 15 y salida 15 a 3; responsable, fecha y observaciones visibles. |
| Estado | Aprobado |
| Evidencia | [hu02-historial.png](evidencias/hu02-historial.png); [resultados-navegador.json](evidencias/resultados-navegador.json); [phpunit-junit.xml](evidencias/phpunit-junit.xml) |
| Prueba automática relacionada | test_entry_increases_stock_and_records_history; test_exit_decreases_stock_and_alert_appears_at_exact_minimum |

## SQA/CP-14: Comprobar alerta en mínimo exacto

| Campo | Contenido |
| --- | --- |
| Historia | HU-02 |
| Objetivo | Comprobar alerta en mínimo exacto |
| Precondiciones | SQA-001 activo, stock 3 y mínimo 3. |
| Datos de entrada | Filtro de alertas SQA-001. |
| Pasos | Abrir Stock bajo, buscar producto y leer estado/stock/mínimo. |
| Resultado esperado | Estado Stock bajo al cumplirse stock igual al mínimo. |
| Resultado obtenido | Alerta Stock bajo visible con stock 3 y mínimo 3. |
| Estado | Aprobado |
| Evidencia | [hu02-alerta-minimo.png](evidencias/hu02-alerta-minimo.png); [resultados-navegador.json](evidencias/resultados-navegador.json); [phpunit-junit.xml](evidencias/phpunit-junit.xml) |
| Prueba automática relacionada | test_exit_decreases_stock_and_alert_appears_at_exact_minimum |

## Cobertura adicional ejecutada

La suite también verifica hash y sesiones, protección de rutas, ausencia de registro público, SKU en minúsculas, valores fraccionarios, stock inicial cero, rollback del producto, edición sin modificación de stock, conservación de inactivos, paginación, modelo con saldo obsoleto, rollback del movimiento, restricción SQLite, dos salidas concurrentes y seeder repetible. REG-MAX comprueba la cantidad 2147483648 y el mensaje de límite superior.

La prueba HTTP de salida válida usa 10 - 7 = 3; el navegador, en su secuencia, usa 15 - 12 = 3. Ambas son variantes documentadas de CA-02. No se presentan como una única ejecución con datos iguales.
