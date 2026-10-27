# Preevaluación técnica de cumplimiento: HU-02

Fecha de elaboración: 13 de octubre de 2026. Auditoría independiente: pendiente. El responsable de esta evaluación técnica es Codex; no se atribuye al docente ni a otro equipo.

## Objetivo y alcance

Comprobar la aritmética de entradas y salidas, el rechazo de cantidades inválidas o insuficientes, la persistencia del historial y las alertas al llegar al mínimo. Se consideran exclusivamente sus seis CA originales y las comprobaciones técnicas relacionadas. Plan de calidad/rúbrica del curso: no aportados; conformidad oficial con esos estándares: No verificado.

## Referencias y procedimiento

Consigna de la actividad, criterios de planificación, código real, convenciones MVC observadas, pruebas PHPUnit, capturas Chromium y estados SQLite. Se contrastó el requisito con el archivo, se ejecutaron casos válidos/negativos y se comprobó persistencia. Las comprobaciones de forma usan Pint y Composer; no se presentan como una norma del curso.

## Matriz de conformidad

| CA | Descripción original | Evidencia objetiva | Resultado | Observación | Recomendación |
| --- | --- | --- | --- | --- | --- |
| CA-01 | Las entradas deben incrementar correctamente las existencias. | M2, M3; SQA/CP-08 | Cumple | Comprobado en código, PHPUnit y navegador. | Validar independientemente las evidencias. |
| CA-02 | Las salidas deben disminuir correctamente las existencias. | M2, M3; SQA/CP-09 | Cumple | Comprobado en código, PHPUnit y navegador. | Validar independientemente las evidencias. |
| CA-03 | No se debe permitir retirar más productos de los disponibles. | M2; SQA/CP-10 | Cumple | Comprobado en código, PHPUnit y navegador. | Validar independientemente las evidencias. |
| CA-04 | No se deben permitir movimientos con cantidades iguales o menores a cero. | M1, M2, M10; SQA/CP-11, SQA/CP-12 | Cumple | Comprobado en código, PHPUnit y navegador. | Validar independientemente las evidencias. |
| CA-05 | Cada entrada y salida debe quedar registrada en el historial. | M2, M4, M5, M7; SQA/CP-08, SQA/CP-09, SQA/CP-13 | Cumple | Comprobado en código, PHPUnit y navegador. | Validar independientemente las evidencias. |
| CA-06 | El sistema debe mostrar alertas cuando un producto alcance su stock mínimo. | M8, M9; SQA/CP-14 | Cumple | Comprobado en código, PHPUnit y navegador. | Validar independientemente las evidencias. |

## Porcentaje técnico verificado

(6 criterios comprobados que cumplen / 6 criterios aplicables) x 100 = **100%**.

Criterios no verificados: 0. No aplicables: 0. Pruebas bloqueadas de la actividad: 0. La validación independiente de este porcentaje y la conformidad con la rúbrica son pendientes separados; no se cuentan como CA aprobados por un docente.

## Hallazgos y recomendaciones

HR-01 resuelto con namespace SQA/CP. HR-02 y HR-03 pendientes por proceso/alcance. HR-04 corregido: concordancia de mensajes quantity.min/max, con regresión y capturas antes/después.

Recomendación: repetir los casos sobre una copia de pruebas, contrastar la matriz con la rúbrica real y conservar las evidencias originales antes de firmar. No usar el 100% técnico como una certificación del sistema completo.

## Conclusión preliminar y aprobación oficial

La implementación comprobada cumple los seis CA en el alcance y entorno documentados. La auditoría formal no se ha realizado ni validado en esta preparación.

- Equipo externo o auditor designado: [Completar].
- Integrantes y roles: [Completar].
- Fecha de actividad formal: [Completar].
- Observaciones oficiales: [Completar].
- Resultado aprobado por el responsable independiente: [Completar].
- Firma o validación: [Completar].

La elaboración técnica por Codex no acredita la participación de otro equipo, una reunión de inspección ni una auditoría del docente.

## Artefactos de soporte

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
