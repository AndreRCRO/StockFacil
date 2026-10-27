# Acta de inspección: HU-02

**Borrador técnico preliminar, pendiente de sesión y firmas reales.**

Proyecto: StockFácil. Historia: HU-02, Control de entradas y salidas de inventario.

- Fecha de elaboración preliminar: 13 de octubre de 2026.
- Fecha de sesión formal: [Completar].
- Modalidad preliminar: lectura técnica asistida, pruebas HTTP automatizadas y navegador sobre SQLite aislado.
- Modalidad de inspección formal: [Completar].
- Objetivo: Comprobar la aritmética de entradas y salidas, el rechazo de cantidades inválidas o insuficientes, la persistencia del historial y las alertas al llegar al mínimo.
- Alcance: diez elementos de implementación y documentación identificados en el checklist; no certifica estándares del curso no aportados.
- Preparación técnica: Codex, herramienta de asistencia; no constituye un participante humano ni revisor independiente.
- Moderador: [Nombre, equipo y firma].
- Autor o representante del equipo de desarrollo: [Nombre y firma].
- Inspector o lector: [Nombre, equipo y firma].
- Secretario: [Nombre y firma].

Procedimiento realizado: lectura de artefactos, comparación de los seis CA originales, consulta de rutas y migración, ejecución de PHPUnit, captura de formularios reales y contraste del estado SQLite. Los intentos inválidos se enviaron con noValidate para probar las reglas del servidor.

Artefactos inspeccionados: referencias M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, P7, P8, C1, C2, A1, B1, T2, T3, T4, T5; inventario con archivos y líneas en este paquete. Las capturas corresponden a la interfaz ya implementada; no son mockups previos.

Hallazgos: HR-01, ambigüedad entre catálogos CP, corregido documentalmente; HR-02 y HR-03, actividades formales y rúbrica pendientes. HR-04, concordancia del mensaje de cantidad, corregido y comprobado antes/después.

Acciones y responsables: AC-01 y AC-02 ejecutadas técnicamente por Codex; equipo humano responsable de ratificarlas: [Completar]. AC-03 corresponde al equipo revisor/pares [Completar] y AC-04 al docente o auditor designado [Completar]. No se asigna un plazo inventado; fecha compromiso de cada equipo: [Completar].

Estado: inspección técnica preliminar completada; inspección formal por pares pendiente. Conclusión preliminar: los elementos comprobados cumplen el alcance implementado, con la limitación de no contar con aprobación de participantes externos. Acuerdos de la sesión real y conclusión formal: [Completar después de inspeccionar].

Firmas de participantes y validación del acta: [Completar].

## Checklist y artefactos anexos

[Checklist técnico detallado](checklist-inspeccion-hu02.md)

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
