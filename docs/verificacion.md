# Verificación técnica ejecutada

Fecha: 13 de octubre de 2026. Entorno: Windows, PHP 8.3.33, Composer 2.10.3 y Node.js 24.15.0. Esta evidencia registra ejecuciones de desarrollo; no constituye una revisión, inspección ni auditoría SQA académica.

## Pruebas automatizadas

Comando ejecutado después de corregir los errores encontrados:

```text
php artisan test --compact
Tests: 42 passed (276 assertions)
Duration: 15.49s
```

La suite comprueba autenticación, rutas protegidas, validaciones, registro y edición, stock inicial trazable, entradas, salidas, insuficiencia, alertas, conservación del historial, filtros, paginación, transacciones y seeders repetibles. Incluye un campo SKU malformado y el rollback de la creación del producto si falla su movimiento inicial.

La prueba concurrente ejecutó dos procesos PHP con solicitudes de salida de siete unidades sobre un saldo de diez. Una operación se aceptó, otra se rechazó y el saldo terminó en tres. Solo quedó una salida adicional en el historial.

Las pruebas HTTP usaron SQLite en memoria; la concurrencia usó un archivo temporal. El inventario de desarrollo mantuvo sus doce productos y veinticuatro movimientos.

## Compilación y configuración

| Comando | Resultado observado |
| --- | --- |
| `npm run build` | Compilación Vite completada; generó manifiesto, CSS, JavaScript y fuentes locales. |
| `composer validate --strict` | `composer.json` válido. |
| `php vendor/laravel/pint/builds/pint --test --format=txt` | Formato aprobado. |
| `php artisan view:cache` | Plantillas Blade compiladas correctamente. |
| `php artisan migrate:status` | Todas las migraciones ejecutadas en desarrollo. |

## Flujos de navegador

Chromium, mediante Playwright disponible en el entorno, ejecutó los formularios contra un segundo servidor con un archivo SQLite temporal. Se verificó:

- Error de credenciales, inicio de sesión y cierre de sesión.
- Dashboard con datos reales.
- Rechazo de SKU duplicado y conservación de los valores del formulario.
- Registro de producto con cinco unidades iniciales y edición de nombre.
- Entrada de tres unidades, stock final ocho y vista previa coincidente.
- Salida de seis unidades, stock final dos y alerta de stock bajo.
- Rechazo de salida de tres cuando solo quedaban dos; saldo conservado.
- Desactivación, consulta de inactivos y permanencia de los tres movimientos del producto.
- Menú móvil y cierre con Escape.

Resultado del flujo: completado sin errores JavaScript. Se comprobaron las seis vistas internas a 390, 768 y 1440 px, sin desbordamiento horizontal de la página. Las tablas permiten desplazamiento dentro de su contenedor.

Las capturas de desarrollo están en `.impeccable/review/`, excluidas de Git. El script de navegador usa herramientas del entorno de trabajo y no forma parte de los requisitos para instalar StockFácil; las pruebas reproducibles del repositorio se ejecutan con `php artisan test`.

## Integridad del inventario de demostración

Consulta ejecutada sobre la base local después de las pruebas:

| Consulta | Resultado |
| --- | --- |
| Productos | 12 |
| Unidades de productos activos | 184 |
| Alertas, incluidos agotados | 5 |
| Productos agotados | 2 |
| Movimientos | 24 |
| `PRAGMA foreign_key_check` | Sin violaciones |
| `PRAGMA journal_mode` | `wal` |

## Alcance y límites

Los resultados respaldan los casos ejecutados y el entorno descrito. No prueban disponibilidad en hosting, navegadores distintos de Chromium, lectores de pantalla ni cargas de producción. No se incorporan API, Flutter, notificaciones externas ni múltiples roles porque quedan fuera de esta fase.

## Ajustes de accesibilidad verificados

La revisión técnica de interfaz detectó foco accesible en el menú móvil cerrado y contraste insuficiente en placeholders. Se corrigieron ambos. La comprobación posterior verificó `inert` al inicio/cierre, apertura con Enter, cierre con Escape, restauración del menú al pasar a escritorio y exclusión de enlaces invisibles durante Tab. El placeholder usa `#626e66`, con contraste de 5,33:1 sobre blanco. La revisión de resolución confirmó los dos ajustes; la captura final del menú se tomó después de concluir su transición.

