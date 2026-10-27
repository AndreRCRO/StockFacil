# Casos de prueba planificados

Estos casos permiten verificar HU-01 y HU-02. La tabla describe resultados **esperados**, no resultados de inspección ni auditoría. Para ejecutar la automatización, usa `php artisan test`.

## Preparación

- Pruebas HTTP con SQLite `:memory:` y `RefreshDatabase`.
- Un usuario administrador y una categoría creados por cada prueba.
- Para HU-02: producto con 10 unidades y mínimo de 3, creado por el servicio.
- La prueba concurrente utiliza un archivo SQLite temporal independiente y lo elimina al finalizar.
- Para pruebas manuales, usa una copia de la base local o los datos de demostración; no uses inventario real.

## HU-01

| ID | Criterio | Entrada o pasos | Resultado esperado | Automatización |
| --- | --- | --- | --- | --- |
| CP-01 | CA-01 a CA-05 | Registrar nombre, SKU, categoría, Bs 3,50, stock 10, mínimo 3. | Producto en listado; stock 10; entrada inicial de 10; responsable registrado. | `ProductTest::test_valid_product_appears_in_listing_with_traceable_initial_stock` |
| CP-02 | CA-01, CA-06 | Enviar nombre vacío. | Error en español; no se guarda producto ni movimiento. | `test_invalid_product_is_rejected` |
| CP-03 | CA-02, CA-06 | Registrar SKU existente también en minúsculas. | Rechazo del duplicado; un solo producto. | `test_duplicate_sku_is_rejected_even_with_lowercase` |
| CP-04 | CA-03, CA-06 | Precio −1, texto o tres decimales. | Rechazo y mensaje; base sin cambios. | Conjuntos `price` de `test_invalid_product_is_rejected` |
| CP-05 | CA-04, CA-06 | Stock inicial −1 o 1,5. | Rechazo; no se crea producto. | Conjuntos `initial_stock` |
| CP-06 | CA-02, CA-06 | SKU vacío, categoría inexistente o mínimo negativo. | Mensaje del campo correspondiente. | Conjuntos `sku`, `category_id`, `minimum_stock` |
| CP-07 | CA-03, CA-04 | Precio y stock inicial cero. | Se guarda el producto; no se registra movimiento cero. | `test_zero_initial_stock_and_zero_price_are_valid_without_zero_movement` |
| CP-08 | Complementario | Editar nombre y precio manteniendo el mismo SKU. Después enviar `stock` o `initial_stock`. | Edición válida; intento de alterar stock rechazado. | `test_edit_updates_information_but_cannot_modify_stock` |
| CP-09 | Complementario | Desactivar producto con historial. | Se excluye del catálogo activo, aparece en inactivos y conserva historial. | `test_deactivation_preserves_history_and_hides_from_active_listing` |
| CP-10 | Complementario | Buscar nombre o SKU y aplicar otra categoría. | Solo aparecen coincidencias dentro de los filtros. | `test_search_and_category_filter_work_together` |

## HU-02

| ID | Criterio | Entrada o pasos | Resultado esperado | Automatización |
| --- | --- | --- | --- | --- |
| CP-11 | CA-01, CA-05 | Entrada de 5 sobre stock 10. | Stock 15; movimiento de 10 a 15 con fecha y responsable. | `InventoryTest::test_entry_increases_stock_and_records_history` |
| CP-12 | CA-02, CA-05, CA-06 | Salida de 7 sobre stock 10. | Stock 3; salida registrada; alerta en el mínimo exacto. | `test_exit_decreases_stock_and_alert_appears_at_exact_minimum` |
| CP-13 | CA-03 | Salida de 11 sobre stock 10. | Error de insuficiencia; stock e historial intactos. | `test_insufficient_stock_preserves_balance_and_history` |
| CP-14 | CA-04 | Cantidad 0, −1, 1,5, texto o vacía. | Error de cantidad; sin cambios en SQLite. | `test_invalid_movement_is_rejected` |
| CP-15 | CA-02, CA-06 | Salida de exactamente 10 unidades. | Stock 0; estado Agotado; indicador actualizado. | `test_exact_stock_exit_is_allowed_and_marks_product_out_of_stock` |
| CP-16 | CA-06 | Llevar stock a 2 y registrar entrada de 5. | Alerta antes; disponible y sin alerta después. | `test_replenishment_removes_alert_and_inactive_products_are_excluded` |
| CP-17 | Complementario | Intentar entrada en producto inactivo, desde HTTP y servicio. | Ambos rechazan el movimiento. | `test_inactive_product_rejects_movements_in_request_and_service` |
| CP-18 | CA-05 | Registrar 12 entradas y filtrar historial. | Paginación de 10 filas; filtros conservados; salidas excluidas. | `test_history_filters_and_pagination_preserve_filter` |
| CP-19 | CA-03, CA-05 | Dos procesos retiran 7 sobre saldo 10 al mismo tiempo. | Una salida aceptada, una rechazada; saldo 3; historial coherente. | `ConcurrencyTest` |
| CP-20 | CA-05 | Forzar fallo al guardar el responsable del movimiento. | Rollback del movimiento y del cambio de stock. | `test_movement_failure_rolls_back_stock_update` |
| CP-21 | Complementario | Registrar movimientos desde un modelo con saldo desactualizado. | Se consulta el saldo real y se conservan los saldos consecutivos. | `test_service_uses_current_database_balance_instead_of_stale_model` |
| CP-22 | Complementario | Solicitar edición/eliminación de un movimiento. | Ruta inexistente; historial intacto. | `test_history_has_no_edit_or_delete_endpoints` |
| CP-23 | Complementario | Intentar actualizar stock negativo directamente en SQLite. | Trigger rechaza la escritura. | `test_database_rejects_negative_stock` |

## Autenticación, datos y revisión manual

| ID | Pasos | Resultado esperado | Automatización |
| --- | --- | --- | --- |
| CP-24 | Abrir rutas y enviar formularios sin sesión. | Redirección al inicio de sesión; ninguna escritura. | `AuthenticationTest::test_internal_routes_require_authentication` |
| CP-25 | Iniciar sesión y cerrarla. | Acceso al dashboard; al salir se invalidan sesión y token. | `test_login_and_logout` |
| CP-26 | Enviar cinco contraseñas incorrectas y volver a intentar. | Mensajes de credenciales y bloqueo temporal. | `test_invalid_credentials_and_login_throttling` |
| CP-27 | Acceder a registro público. | Ruta inexistente. | `test_public_registration_is_not_available` |
| CP-28 | Ejecutar seeder dos veces y recorrer movimientos. | 12 productos, 5 categorías, 24 movimientos; saldos coherentes y sin duplicados. | `SeederTest` |
| CP-29 | Usar menú y formularios a 390, 768 y 1440 px. | Navegación accesible; sin desbordamiento de página; tablas desplazables. | Revisión de navegador |
| CP-30 | Enviar formulario inválido y corregirlo. | Errores legibles; se conserva entrada; confirmación al guardar. | Prueba HTTP y flujo de navegador |
| CP-31 | Usar Tab, Shift+Tab y Escape en menú móvil. | Foco visible y contenido alcanzable; Escape cierra el menú. | Revisión de navegador |
| CP-32 | Registrar entrada/salida sin JavaScript. | Las reglas y la persistencia funcionan desde el servidor. | Pruebas HTTP; comprobación manual opcional |

## Evidencia

Consulta [verificacion.md](verificacion.md) para las ejecuciones técnicas realizadas. Una ejecución de pruebas funcionales no reemplaza una revisión, inspección o auditoría SQA.
