# Fichas académicas de historias de usuario

Elaboración: 13 de octubre de 2026. Fuente de requisitos: consigna de la actividad y proyecto existente.

## HU-01: Registro de productos

| Campo | Contenido |
| --- | --- |
| Código | HU-01 |
| Actor | Administrador de una tienda |
| Descripción | Como administrador de una tienda, quiero registrar nuevos productos con su información correspondiente para mantener actualizado el inventario de mi negocio. |
| Objetivo | Comprobar que el registro valida los datos, persiste un producto en SQLite y permite localizarlo en el inventario, conservando trazabilidad del stock inicial. |
| Prioridad | Alta propuesta para la actividad, pendiente de confirmación del equipo; la consigna no establece una prioridad contractual. |

### Criterios originales

- CA-01: El sistema debe exigir el nombre del producto.
- CA-02: El SKU o código del producto debe ser único.
- CA-03: El precio no puede ser negativo.
- CA-04: La cantidad inicial no puede ser negativa.
- CA-05: Cuando se registre correctamente un producto, este debe aparecer en el inventario.
- CA-06: Cuando se ingresen datos inválidos, el sistema debe mostrar mensajes de validación.

### Artefactos reales

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

### Funcionalidades y flujo documentado posteriormente

Acceso autenticado; formulario de producto; validación; creación transaccional; entrada inicial si es positiva; confirmación; catálogo paginado y búsqueda. La edición y desactivación son complementarias.

No se localizaron mockups previos ni diagramas de casos de uso en los artefactos del proyecto examinados. DESIGN.md documenta el sistema visual; las capturas de esta actividad se obtuvieron posteriormente desde la aplicación real y se etiquetan como evidencia funcional.

## HU-02: Control de entradas y salidas de inventario

| Campo | Contenido |
| --- | --- |
| Código | HU-02 |
| Actor | Administrador de una tienda |
| Descripción | Como administrador de una tienda, quiero registrar las entradas y salidas de productos para controlar las cantidades disponibles en mi inventario. |
| Objetivo | Comprobar la aritmética de entradas y salidas, el rechazo de cantidades inválidas o insuficientes, la persistencia del historial y las alertas al llegar al mínimo. |
| Prioridad | Alta propuesta para la actividad, pendiente de confirmación del equipo; la consigna no establece una prioridad contractual. |

### Criterios originales

- CA-01: Las entradas deben incrementar correctamente las existencias.
- CA-02: Las salidas deben disminuir correctamente las existencias.
- CA-03: No se debe permitir retirar más productos de los disponibles.
- CA-04: No se deben permitir movimientos con cantidades iguales o menores a cero.
- CA-05: Cada entrada y salida debe quedar registrada en el historial.
- CA-06: El sistema debe mostrar alertas cuando un producto alcance su stock mínimo.

### Artefactos reales

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

### Funcionalidades y flujo documentado posteriormente

Acceso autenticado; selección de producto activo; entrada/salida y cantidad; preview orientativo; validación del servidor; saldo e historial atómicos; consulta y alertas.

No se localizaron mockups previos ni diagramas de casos de uso en los artefactos del proyecto examinados. DESIGN.md documenta el sistema visual; las capturas de esta actividad se obtuvieron posteriormente desde la aplicación real y se etiquetan como evidencia funcional.

### Documentación existente

README.md; docs/historias-usuario.md; docs/arquitectura.md; docs/casos-prueba.md; docs/verificacion.md; PRODUCT.md y DESIGN.md. Los documentos previos no se sustituyen y los resultados de esta actividad se mantienen separados.
