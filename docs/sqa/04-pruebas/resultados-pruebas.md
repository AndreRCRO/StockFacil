# Resultados reales de pruebas

Fecha local: 13 de octubre de 2026, America/La_Paz. PHP 8.3.33, PHPUnit 12.5.39, Laravel 13 y SQLite. Los timestamps UTC de los JSON de navegador se conservan sin sustituirlos por fechas de reuniones.

## Ejecuciones

- Suite original: 42 pruebas aprobadas, 276 aserciones; evidencia phpunit-antes.txt/xml.
- Preparación inicial del test ampliado: 3 errores de aserción del test, 5 aprobadas; registro separado regresion-preparacion-error.txt/xml. No es un defecto del producto.
- Regresión válida anterior a HR-04: 3 fallidas, 5 aprobadas; las tres comprueban textos de cantidad mínimo/máximo. Evidencia regresion-antes.txt/xml.
- Suite posterior: **43 aprobadas, 286 aserciones; 0 fallos, 0 errores y 0 omitidas**. Evidencia phpunit-junit.xml y phpunit-salida.txt. Tiempo JUnit: 6.676218 s; el tiempo total mostrado por Artisan incluye su envoltura.
- Navegador: 14 casos de la actividad aprobados; CP-11 y CP-12 reejecutados después del cambio, más REG-MAX. Evidencia resultados-navegador.json y revalidacion-correccion.json.

| Clase | Pruebas | Aserciones | Fallos | Errores |
| --- | --- | --- | --- | --- |
| AuthenticationTest | 4 | 46 | 0 | 0 |
| ConcurrencyTest | 1 | 5 | 0 | 0 |
| InventoryTest | 19 | 83 | 0 | 0 |
| InventoryTest::test_invalid_movement_is_rejected | 8 | 38 | 0 | 0 |
| ProductTest | 18 | 81 | 0 | 0 |
| ProductTest::test_invalid_product_is_rejected | 11 | 44 | 0 | 0 |
| SeederTest | 1 | 71 | 0 | 0 |

## Resultados por caso

| Caso SQA | Historia | Estado | Resultado obtenido |
| --- | --- | --- | --- |
| CP-01 | HU-01 | Aprobado | Producto registrado. El stock inicial quedó en el historial. |
| CP-02 | HU-01 | Aprobado | El campo nombre es obligatorio. |
| CP-03 | HU-01 | Aprobado | El SKU ya está registrado. Usa otro valor. |
| CP-04 | HU-01 | Aprobado | El precio debe ser mayor o igual a 0. |
| CP-05 | HU-01 | Aprobado | El stock inicial debe ser mayor o igual a 0. |
| CP-06 | HU-01 | Aprobado | Producto SQA-001 visible en el listado filtrado, Bs 8,50 y stock 10. |
| CP-07 | HU-01 | Aprobado | Resumen y mensaje junto al nombre visibles; SKU conservado y aria-invalid=true. |
| CP-08 | HU-02 | Aprobado | Entrada de 5 aceptada; historial muestra stock 10 a 15. |
| CP-09 | HU-02 | Aprobado | Salida de 12 aceptada; historial muestra stock 15 a 3. |
| CP-10 | HU-02 | Aprobado | Stock insuficiente. Solo hay 3 unidades disponibles. Saldo conservado: 3. |
| CP-11 | HU-02 | Aprobado | La cantidad debe ser mayor o igual a 1. Saldo conservado: 3. |
| CP-12 | HU-02 | Aprobado | La cantidad debe ser mayor o igual a 1. Saldo conservado: 3. |
| CP-13 | HU-02 | Aprobado | Tres movimientos: entrada inicial 0 a 10, entrada 10 a 15 y salida 15 a 3; responsable, fecha y observaciones visibles. |
| CP-14 | HU-02 | Aprobado | Alerta Stock bajo visible con stock 3 y mínimo 3. |

## Protección de datos y coherencia

Los comandos de PHPUnit se ejecutaron con APP_ENV=testing, DB_CONNECTION=sqlite y DB_DATABASE=:memory:, además de phpunit.xml. ConcurrencyTest usa un archivo temporal y lo elimina. Las migraciones/seeders del navegador se ejecutaron solo sobre tmp/sqa/navegador.sqlite, con servidor en el puerto 8003.

integridad-final.json confirma sin cambios la huella lógica del inventario de desarrollo: 12 productos, 24 movimientos, 5 categorías y 184 unidades activas. sqlite-navegador.json comprueba los tres eventos 0 -> 10 -> 15 -> 3, fechas/responsables presentes, integrity_check=ok y sin infracciones de claves foráneas.

## Comandos reales

```powershell
$env:APP_ENV='testing'
$env:DB_CONNECTION='sqlite'
$env:DB_DATABASE=':memory:'
php artisan test --testdox --colors=never --log-junit=docs/sqa/04-pruebas/evidencias/phpunit-junit.xml
php vendor/laravel/pint/builds/pint --test --format=txt
composer validate --strict
```

El script capturar-evidencias.cjs utiliza Playwright ya disponible en el entorno mediante PLAYWRIGHT_MODULE. Debe apuntar únicamente a un servidor de pruebas mediante SQA_URL. No se añade Playwright a las dependencias de StockFácil. verificar-correccion.cjs usa el producto temporal creado por el primer script.

## Limitaciones

No hay casos bloqueados ni no ejecutados entre SQA/CP-01 y CP-14. No se evaluaron hosting, carga de producción, otros navegadores, lectores de pantalla ni una rúbrica de curso no aportada. La aprobación funcional no equivale a revisión externa, inspección formal o auditoría oficial.
