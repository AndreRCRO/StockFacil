# Historias de usuario

Estas historias corresponden al administrador de StockFácil. Las pruebas automatizadas utilizan SQLite aislado del inventario de desarrollo.

## HU-01: Registro de productos

Como administrador, quiero registrar productos para mantener actualizado el inventario de mi negocio.

| Criterio | Comportamiento implementado | Artefactos y pruebas |
| --- | --- | --- |
| CA-01 | El nombre es obligatorio. | `ProductRequest`; `ProductTest::test_invalid_product_is_rejected`, conjunto `name`. |
| CA-02 | El SKU no se repite, incluso al ingresar minúsculas. | Normalización en `ProductRequest`, índice único de SQLite; `test_duplicate_sku_is_rejected_even_with_lowercase`. |
| CA-03 | El precio es numérico y no negativo, con hasta dos decimales. | `ProductRequest`; conjuntos `price` de `test_invalid_product_is_rejected`. |
| CA-04 | El stock inicial es entero y no negativo. | `ProductRequest`, `InventoryService`; conjuntos `initial_stock` y prueba de cantidad cero. |
| CA-05 | El producto guardado aparece en el listado. | `ProductController`, `products/index.blade.php`; `test_valid_product_appears_in_listing_with_traceable_initial_stock`. |
| CA-06 | Los datos inválidos generan mensajes visibles en español. | `lang/es/validation.php`, componentes `flash` y `field`; pruebas inválidas que siguen la redirección y comprueban el mensaje. |

### Reglas complementarias

- El precio se expresa en bolivianos (Bs).
- El SKU se guarda en mayúsculas y conserva su unicidad también durante la edición.
- Una cantidad inicial positiva crea una entrada dentro de la misma transacción que crea el producto.
- Con stock inicial cero no se crea un movimiento de cantidad cero.
- Editar el catálogo no modifica existencias; el servidor rechaza los campos `stock` e `initial_stock` en la edición.
- Desactivar un producto conserva su registro y sus movimientos. No existe eliminación física en la interfaz.

Artefactos principales: `app/Models/Product.php`, `app/Models/Category.php`, `app/Http/Requests/ProductRequest.php`, `app/Http/Controllers/ProductController.php`, `app/Services/InventoryService.php`, migración de inventario y vistas `resources/views/products/`.

## HU-02: Control de existencias

Como administrador, quiero registrar entradas y salidas para conocer el stock disponible.

| Criterio | Comportamiento implementado | Artefactos y pruebas |
| --- | --- | --- |
| CA-01 | Una entrada incrementa el stock. | `InventoryService::record`; `InventoryTest::test_entry_increases_stock_and_records_history`. |
| CA-02 | Una salida disminuye el stock. | `InventoryService::record`; `test_exit_decreases_stock_and_alert_appears_at_exact_minimum`. |
| CA-03 | Una salida mayor al saldo se rechaza sin modificar el inventario. | `test_insufficient_stock_preserves_balance_and_history`; `ConcurrencyTest`. |
| CA-04 | Se rechazan cantidades cero, negativas, fraccionarias o no numéricas. | `MovementRequest`, `InventoryService`; conjuntos de `test_invalid_movement_is_rejected`. |
| CA-05 | Cada movimiento conserva producto, tipo, cantidad, saldos, responsable, fecha y observación. | `Movement`, `MovementController`, vistas `movements`; pruebas de historial, filtros, paginación y rollback. |
| CA-06 | Se muestra una alerta cuando el stock es igual o inferior al mínimo. | `Product::scopeLowStock`, `stock_status`, dashboard y `low-stock.blade.php`; pruebas del mínimo exacto, agotamiento y reposición. |

### Reglas complementarias

- No se admiten movimientos en productos inactivos.
- Actualizar stock y crear el historial constituyen una sola transacción.
- El servicio vuelve a consultar el saldo real; no confía en el stock de un modelo cargado anteriormente.
- SQLite serializa escrituras; el servicio adquiere el bloqueo antes de leer el saldo. La actualización incluye el saldo anterior como condición.
- No hay rutas para editar ni borrar movimientos históricos.
- La vista previa de JavaScript ayuda al administrador; el servidor siempre valida nuevamente al guardar.

Artefactos principales: `app/Models/Movement.php`, `app/Http/Requests/MovementRequest.php`, `app/Http/Controllers/MovementController.php`, `app/Services/InventoryService.php`, vistas `resources/views/movements/` y pruebas `InventoryTest` y `ConcurrencyTest`.

## Actividades SQA posteriores

Los criterios y los casos planificados sirven como base para revisión, inspección y auditoría. Este documento no contiene resultados de esas actividades. Las ejecuciones técnicas reales se documentan por separado.
