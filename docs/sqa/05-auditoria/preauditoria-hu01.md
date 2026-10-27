# Preevaluación técnica de cumplimiento: HU-01

Fecha de elaboración: 13 de octubre de 2026. Auditoría independiente: pendiente. El responsable de esta evaluación técnica es Codex; no se atribuye al docente ni a otro equipo.

## Objetivo y alcance

Comprobar que el registro valida los datos, persiste un producto en SQLite y permite localizarlo en el inventario, conservando trazabilidad del stock inicial. Se consideran exclusivamente sus seis CA originales y las comprobaciones técnicas relacionadas. Plan de calidad/rúbrica del curso: no aportados; conformidad oficial con esos estándares: No verificado.

## Referencias y procedimiento

Consigna de la actividad, criterios de planificación, código real, convenciones MVC observadas, pruebas PHPUnit, capturas Chromium y estados SQLite. Se contrastó el requisito con el archivo, se ejecutaron casos válidos/negativos y se comprobó persistencia. Las comprobaciones de forma usan Pint y Composer; no se presentan como una norma del curso.

## Matriz de conformidad

| CA | Descripción original | Evidencia objetiva | Resultado | Observación | Recomendación |
| --- | --- | --- | --- | --- | --- |
| CA-01 | El sistema debe exigir el nombre del producto. | P1, P5; SQA/CP-02 | Cumple | Comprobado en código, PHPUnit y navegador. | Validar independientemente las evidencias. |
| CA-02 | El SKU o código del producto debe ser único. | P1, P7; SQA/CP-03 | Cumple | Comprobado en código, PHPUnit y navegador. | Validar independientemente las evidencias. |
| CA-03 | El precio no puede ser negativo. | P1, P7; SQA/CP-04 | Cumple | Comprobado en código, PHPUnit y navegador. | Validar independientemente las evidencias. |
| CA-04 | La cantidad inicial no puede ser negativa. | P1, P4; SQA/CP-05 | Cumple | Comprobado en código, PHPUnit y navegador. | Validar independientemente las evidencias. |
| CA-05 | Cuando se registre correctamente un producto, este debe aparecer en el inventario. | P2, P3, P6; SQA/CP-01, SQA/CP-06 | Cumple | Comprobado en código, PHPUnit y navegador. | Validar independientemente las evidencias. |
| CA-06 | Cuando se ingresen datos inválidos, el sistema debe mostrar mensajes de validación. | C1, C2, C3, C4; SQA/CP-02, SQA/CP-07 | Cumple | Comprobado en código, PHPUnit y navegador. | Validar independientemente las evidencias. |

## Porcentaje técnico verificado

(6 criterios comprobados que cumplen / 6 criterios aplicables) x 100 = **100%**.

Criterios no verificados: 0. No aplicables: 0. Pruebas bloqueadas de la actividad: 0. La validación independiente de este porcentaje y la conformidad con la rúbrica son pendientes separados; no se cuentan como CA aprobados por un docente.

## Hallazgos y recomendaciones

HR-01 resuelto con namespace SQA/CP. HR-02 y HR-03 pendientes por proceso/alcance. No se encontró una no conformidad funcional en los seis CA de registro.

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
