# Código y evidencias de la corrección

Esta carpeta contiene la auditoría del informe y los resultados realmente ejecutados. La consigna original y el PDF entregado se leyeron completos antes de cambiar código. Los datos de portada proceden de DinamicaSQA.pdf: Andre Romero Caballero, Santiago Camacho y Rolando Lara. El tercer integrante y la aprobación del rol cliente siguen pendientes.

El documento corregido se guarda como una copia nueva porque el Word anterior estaba abierto. Desde la raíz del proyecto:

- Word: `output/docx/DinamicaSQA-corregido.docx`.
- PDF: `output/pdf/DinamicaSQA-corregido.pdf`.
- Fuente: `docs/actividad-registro/informe-actividad.md`.
- Auditoría: `docs/actividad-registro/correccion/AUDITORIA.md`.

## Comprobar la versión actual

Instala las dependencias de Composer según el README del proyecto y ejecuta desde su raíz, con PHP 8.3 o superior:

```powershell
php vendor/phpunit/phpunit/phpunit --colors=never --do-not-cache-result
php vendor/phpunit/phpunit/phpunit --filter RegistrationWorkflowTest
php vendor/laravel/pint/builds/pint --test
```

La suite usa `phpunit.xml`, SQLite en memoria y un archivo temporal propio para la prueba de concurrencia. No la apuntes a la base habitual. La ejecución registrada terminó con 60 pruebas y 419 aserciones. Las pruebas de registro completo y persistencia son de integración; las de normalización son unitarias. No se presentan como sesiones manuales ni como una aprobación del cliente.

## Reproducir el RED sin modificar la aplicación

El siguiente arranque alternativo carga las versiones guardadas únicamente dentro del proceso de PHPUnit. No reemplaza archivos de app, no cambia .env y sigue usando SQLite en memoria. Su resultado es una reproducción posterior del código archivado, separada de las ejecuciones originales.

```powershell
$env:SQA_TDD_STAGE='antes'
php vendor/phpunit/phpunit/phpunit --do-not-cache-result --bootstrap docs/actividad-registro/correccion/replay-bootstrap.php.txt --filter RegistrationWorkflowTest
$env:SQA_TDD_STAGE='green'
php vendor/phpunit/phpunit/phpunit --do-not-cache-result --bootstrap docs/actividad-registro/correccion/replay-bootstrap.php.txt --filter RegistrationWorkflowTest
$env:SQA_TDD_STAGE='refactor'
php vendor/phpunit/phpunit/phpunit --do-not-cache-result --bootstrap docs/actividad-registro/correccion/replay-bootstrap.php.txt --filter RegistrationWorkflowTest
Remove-Item Env:SQA_TDD_STAGE
```

En `antes` se esperan tres fallos y salida distinta de cero. En `green` y `refactor` se esperan cuatro pruebas aprobadas y 27 aserciones. La prueba del registro completo aprobaba ya en `antes`; no se le atribuye un RED nuevo.

## Repetir los casos de navegador

1. Prepara una copia nueva y aislada de SQLite. Configura DB_DATABASE solo en la terminal del servidor con su ruta absoluta; no edites .env.
2. Define CACHE_STORE=file y un CACHE_PREFIX propio, y ejecuta `php artisan serve --port=8006`.
3. Proporciona Playwright y Chromium. El script admite PLAYWRIGHT_MODULE para la ruta del módulo, REGISTRO_URL para la URL y REGISTRO_FASE para identificar la ronda. La captura registrada utilizó REGISTRO_URL=http://127.0.0.1:8006 y REGISTRO_FASE=correccion.
4. Ejecuta `node docs/actividad-registro/correccion/evidencias/capturar-registro.cjs`. La cuenta beatriz.sqa@example.test debe estar libre al empezar. Usa una base nueva al repetir. Conserva los archivos históricos: el capturador usa nombres estables y los sobrescribiría.
5. Para el límite de solicitudes ejecuta `node docs/actividad-registro/correccion/evidencias/verificar-limite.cjs` contra esa misma instancia. La caché debe ser persistente; el caso genera validaciones rechazadas y luego HTTP 429.

Los PNG originales están a color. Las salidas JSON identifican qué se esperaba, qué se observó, la hora UTC y la URL. En REG-08 el estado 419 corresponde a una respuesta HTTP comprobada; la captura muestra el formulario posterior.

## Localizar las pruebas y los fallos

`01-red` contiene la ejecución original nueva con tres fallos. `02-green` contiene la corrección mínima. `03-refactor` registra una extracción intermedia; `03-refactor-final` comprueba el código definitivo. `04-suite-final` contiene las 60 pruebas. Las reproducciones de snapshots, si se ejecutan, quedan en archivos separados con prefijo replay.

La primera invocación restringida de PHP y el primer arranque restringido del navegador tuvieron problemas del entorno. No se incluyeron como defectos de StockFácil ni como casos funcionales fallidos.

Los hashes de datos, esquema y .env coinciden antes y después. La base habitual se conserva. Los archivos anteriores del 19 de octubre se mantienen como historia: su fallo de login por mayúsculas ya estaba corregido al empezar esta auditoría.
