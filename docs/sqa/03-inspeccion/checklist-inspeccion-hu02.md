# Checklist de inspección preliminar: HU-02

Fecha: 13 de octubre de 2026. Se comprobaron los elementos mediante lectura de código, pruebas y evidencia visual. Cumple se refiere al alcance técnico, no a la aprobación formal por pares.

| ID | Elemento | Archivo y método (refs. abajo) | Criterio SQA | Resultado técnico | Hallazgo u observación | Acción correctiva | Evidencia |
| --- | --- | --- | --- | --- | --- | --- | --- |
| I02-01 | Entradas | M2, M3 / record y store | Aritmética de incremento | Cumple | 10 + 5 = 15; historial persiste saldos. | Mantener; validar por pares. | SQA/CP-08, T2 |
| I02-02 | Salidas | M2, M3 / record y store | Aritmética de decremento | Cumple | 15 - 12 = 3 en navegador; prueba aislada 10 - 7 = 3. | Mantener; validar por pares. | SQA/CP-09, T2 |
| I02-03 | Stock actualizado | M2 / record | Saldo real sin sobrescritura obsoleta | Cumple | Servicio relee después de adquirir escritura y actualiza condicionalmente. | Mantener; validar por pares. | T2 modelo desactualizado, T3 |
| I02-04 | Stock insuficiente | M2 / record | Saldo no negativo | Cumple | Salida 4 sobre saldo 3 rechazada; no nuevo historial. | Mantener; validar por pares. | SQA/CP-10, T2 |
| I02-05 | Cantidad válida | M1, M2, M10 | Enteros positivos y rango | Cumple | 0, -1 y exceso de límite rechazados; mensajes corregidos. | HR-04 corregido; regresión aprobada. | CP-11/12, REG-MAX, T2 |
| I02-06 | Historial | M2, M4, M5, M7 | Trazabilidad y conservación | Cumple | Tres registros con tipo, cantidad, saldos, fecha, usuario y notas; sin rutas de edición/borrado. | Mantener; validar por pares. | SQA/CP-13, T2 |
| I02-07 | Alertas | M8, M9 / scopeLowStock | Límite inclusivo y estado activo | Cumple | Stock 3 igual a mínimo 3 produce Stock bajo. | Mantener; validar por pares. | SQA/CP-14, T2 |
| I02-08 | Transacciones | M2, B1 / record | Atomicidad y concurrencia SQLite | Cumple | WAL, espera y primera escritura; rollback probado; dos procesos no venden de más. | Mantener; validar por pares. | T2 rollback, T3 |
| I02-09 | Stock protegido | P1, P8, A1 | Evitar modificación directa | Cumple | stock prohibido en formularios; no fillable; movimientos solo en activos. | Mantener; validar por pares. | T1 edición, T2 inactivo |
| I02-10 | Lógica de negocio | M1 a M5 | Responsabilidad y legibilidad | Cumple | Reglas centralizadas en servicio; mensajes específicos en Request; Pint aprobado. | Mantener; validar por pares. | M2, M10, pint-salida.txt |

## Archivos y líneas de las referencias

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

## Participación por pares

- Equipo externo o auditor designado: [Completar].
- Integrantes y roles: [Completar].
- Fecha de actividad formal: [Completar].
- Observaciones oficiales: [Completar].
- Resultado aprobado por el responsable independiente: [Completar].
- Firma o validación: [Completar].

La elaboración técnica por Codex no acredita la participación de otro equipo, una reunión de inspección ni una auditoría del docente.
