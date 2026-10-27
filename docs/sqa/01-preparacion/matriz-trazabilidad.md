# Matriz de trazabilidad

| Historia | CA | Archivo/módulo (ref.) | Caso | Resultado técnico | Evidencia real |
| --- | --- | --- | --- | --- | --- |
| HU-01 | CA-01 | P1, P5 | SQA/CP-02 | Cumple | [CP-02 captura](../04-pruebas/evidencias/hu01-error-nombre.png) |
| HU-01 | CA-02 | P1, P7 | SQA/CP-03 | Cumple | [CP-03 captura](../04-pruebas/evidencias/hu01-error-sku.png) |
| HU-01 | CA-03 | P1, P7 | SQA/CP-04 | Cumple | [CP-04 captura](../04-pruebas/evidencias/hu01-error-precio.png) |
| HU-01 | CA-04 | P1, P4 | SQA/CP-05 | Cumple | [CP-05 captura](../04-pruebas/evidencias/hu01-error-stock-inicial.png) |
| HU-01 | CA-05 | P2, P3, P6 | SQA/CP-01, SQA/CP-06 | Cumple | [CP-01 captura](../04-pruebas/evidencias/hu01-registro-exitoso.png), [CP-06 captura](../04-pruebas/evidencias/hu01-producto-listado.png) |
| HU-01 | CA-06 | C1, C2, C3, C4 | SQA/CP-02, SQA/CP-07 | Cumple | [CP-02 captura](../04-pruebas/evidencias/hu01-error-nombre.png), [CP-07 captura](../04-pruebas/evidencias/hu01-mensajes-validacion.png) |
| HU-02 | CA-01 | M2, M3 | SQA/CP-08 | Cumple | [CP-08 captura](../04-pruebas/evidencias/hu02-entrada-exitosa.png) |
| HU-02 | CA-02 | M2, M3 | SQA/CP-09 | Cumple | [CP-09 captura](../04-pruebas/evidencias/hu02-salida-exitosa.png) |
| HU-02 | CA-03 | M2 | SQA/CP-10 | Cumple | [CP-10 captura](../04-pruebas/evidencias/hu02-error-insuficiente.png) |
| HU-02 | CA-04 | M1, M2, M10 | SQA/CP-11, SQA/CP-12 | Cumple | [CP-11 captura](../04-pruebas/evidencias/hu02-error-cero.png), [CP-12 captura](../04-pruebas/evidencias/hu02-error-negativo.png) |
| HU-02 | CA-05 | M2, M4, M5, M7 | SQA/CP-08, SQA/CP-09, SQA/CP-13 | Cumple | [CP-08 captura](../04-pruebas/evidencias/hu02-entrada-exitosa.png), [CP-09 captura](../04-pruebas/evidencias/hu02-salida-exitosa.png), [CP-13 captura](../04-pruebas/evidencias/hu02-historial.png) |
| HU-02 | CA-06 | M8, M9 | SQA/CP-14 | Cumple | [CP-14 captura](../04-pruebas/evidencias/hu02-alerta-minimo.png) |

## Correspondencia de referencias

| Ref. | Archivo y línea verificados | Clase, método o artefacto |
| --- | --- | --- |
| P1 | `app/Http/Requests/ProductRequest.php:23` | ProductRequest::rules |
| P2 | `app/Http/Controllers/ProductController.php:37` | ProductController::store |
| P3 | `app/Http/Controllers/ProductController.php:16` | ProductController::index |
| P4 | `app/Services/InventoryService.php:13` | InventoryService::createProduct |
| P5 | `resources/views/products/form.blade.php:3` | Formulario Blade de creación y edición |
| P6 | `resources/views/products/index.blade.php:11` | Listado Blade paginado |
| P7 | `database/migrations/2026_10_13_000001_create_inventory_tables.php:17` | Migración: productos y restricciones SQLite |
| P8 | `app/Models/Product.php:17` | Product::category / movements / casts |
| C1 | `resources/views/components/field.blade.php:6` | Componente: etiqueta, ayuda y error del campo |
| C2 | `resources/views/components/flash.blade.php:4` | Componente: resumen de errores y confirmación |
| C3 | `lang/es/validation.php:4` | Mensajes de validación en español |
| C4 | `bootstrap/app.php:19` | Respuesta de validación: recuperación segura de campos escalares |
| A1 | `routes/web.php:14` | Grupo de rutas protegido por auth |
| B1 | `config/database.php:6` | Conexión SQLite, WAL y espera de escritura |
| T1 | `tests/Feature/ProductTest.php:34` | ProductTest: registro válido, invalidaciones y listado |
| T4 | `tests/Feature/AuthenticationTest.php:14` | AuthenticationTest: rutas internas protegidas |
| T5 | `phpunit.xml:24` | SQLite de pruebas en memoria |

| Ref. | Archivo y línea verificados | Clase, método o artefacto |
| --- | --- | --- |
| M1 | `app/Http/Requests/MovementRequest.php:17` | MovementRequest::rules |
| M2 | `app/Services/InventoryService.php:31` | InventoryService::record |
| M3 | `app/Http/Controllers/MovementController.php:34` | MovementController::store |
| M4 | `app/Http/Controllers/MovementController.php:16` | MovementController::index |
| M5 | `app/Models/Movement.php:16` | Movement: atributos, casts y relaciones |
| M6 | `resources/views/movements/form.blade.php:4` | Formulario Blade de movimientos |
| M7 | `resources/views/movements/index.blade.php:4` | Historial Blade |
| M8 | `app/Models/Product.php:37` | Product::scopeLowStock / getStockStatusAttribute |
| M9 | `resources/views/products/low-stock.blade.php:4` | Listado Blade de alertas |
| M10 | `app/Http/Requests/MovementRequest.php:32` | MovementRequest::messages, corrección HR-04 |
| P7 | `database/migrations/2026_10_13_000001_create_inventory_tables.php:17` | Migración: productos y restricciones SQLite |
| P8 | `app/Models/Product.php:17` | Product::category / movements / casts |
| C1 | `resources/views/components/field.blade.php:6` | Componente: etiqueta, ayuda y error del campo |
| C2 | `resources/views/components/flash.blade.php:4` | Componente: resumen de errores y confirmación |
| A1 | `routes/web.php:14` | Grupo de rutas protegido por auth |
| B1 | `config/database.php:6` | Conexión SQLite, WAL y espera de escritura |
| T2 | `tests/Feature/InventoryTest.php:39` | InventoryTest: entradas, salidas, alertas y rollback |
| T3 | `tests/Feature/ConcurrencyTest.php:14` | ConcurrencyTest: dos procesos sobre SQLite temporal |
| T4 | `tests/Feature/AuthenticationTest.php:14` | AuthenticationTest: rutas internas protegidas |
| T5 | `phpunit.xml:24` | SQLite de pruebas en memoria |

Los métodos de prueba concretos y resultados JUnit se detallan en 04-pruebas/casos-prueba.md. Revisión y auditoría independientes permanecen pendientes.
