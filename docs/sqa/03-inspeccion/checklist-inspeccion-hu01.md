# Checklist de inspección preliminar: HU-01

Fecha: 13 de octubre de 2026. Se comprobaron los elementos mediante lectura de código, pruebas y evidencia visual. Cumple se refiere al alcance técnico, no a la aprobación formal por pares.

| ID | Elemento | Archivo y método (refs. abajo) | Criterio SQA | Resultado técnico | Hallazgo u observación | Acción correctiva | Evidencia |
| --- | --- | --- | --- | --- | --- | --- | --- |
| I01-01 | Nombre obligatorio | P1 / ProductRequest::rules | Validación en servidor | Cumple | CP-02 rechaza nombre vacío; error visible. | Mantener; validar por pares. | SQA/CP-02, T1 |
| I01-02 | SKU único | P1, P7 / rules y migración | Integridad y normalización | Cumple | Unique en petición e índice SQLite; minúsculas se normalizan. | Mantener; validar por pares. | SQA/CP-03, T1 |
| I01-03 | Precio | P1 / rules | Dominio numérico no negativo | Cumple | numeric, min:0 y hasta dos decimales. | Mantener; validar por pares. | SQA/CP-04, T1 |
| I01-04 | Stock inicial | P1, P4 / rules y createProduct | Entero no negativo | Cumple | Rechazo de negativo/fraccionario; cero permitido. | Mantener; validar por pares. | SQA/CP-05, T1 |
| I01-05 | Persistencia SQLite | P2, P4, P7, B1 | Persistencia real | Cumple | Eloquent escribe producto; base temporal muestra SQA-001. | Mantener; validar por pares. | sqlite-navegador.json, CP-01 |
| I01-06 | Movimiento inicial | P4 / createProduct | Trazabilidad y atomicidad | Cumple | Entrada 0 a 10; con cero no hay movimiento; fallo revierte producto. | Mantener; validar por pares. | T1; sqlite-navegador.json |
| I01-07 | Producto en listado | P3, P6 / index | Visibilidad y búsqueda | Cumple | Fila filtrada por SKU muestra datos y stock 10. | Mantener; validar por pares. | SQA/CP-06 |
| I01-08 | Mensajes de error | C1 a C4, P5 | Claridad y recuperación | Cumple | Resumen, mensaje por campo, aria-invalid y SKU recuperado. | Mantener; validar por pares. | SQA/CP-07 |
| I01-09 | Autenticación | A1 / grupo auth | Control de acceso | Cumple | Sin sesión, lectura y POST redirigen a login. | Mantener; validar por pares. | T4; phpunit-junit.xml |
| I01-10 | Organización del código | P1 a P8, T1 | MVC y convenciones Laravel | Cumple | Request valida, controlador coordina y servicio persiste; Pint aprobado. | Mantener; validar por pares. | pint-salida.txt, fuentes-inspeccionadas.txt |

## Archivos y líneas de las referencias

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

## Participación por pares

- Equipo externo o auditor designado: [Completar].
- Integrantes y roles: [Completar].
- Fecha de actividad formal: [Completar].
- Observaciones oficiales: [Completar].
- Resultado aprobado por el responsable independiente: [Completar].
- Firma o validación: [Completar].

La elaboración técnica por Codex no acredita la participación de otro equipo, una reunión de inspección ni una auditoría del docente.
