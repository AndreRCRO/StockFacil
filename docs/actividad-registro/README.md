# Actividad Del comportamiento a la implementación

La versión corregida se encuentra en [la carpeta de auditoría y evidencias](correccion/README.md). Incluye la prueba del registro completo, un ciclo TDD nuevo con fallos reales del servicio, 60 pruebas y 419 aserciones, y una nueva repetición de los 11 casos de navegador. El informe final es `output/docx/DinamicaSQA-corregido.docx` y su PDF equivalente, desde la raíz del proyecto. Las salidas antiguas se conservan como historia y no se presentan como ejecuciones nuevas. La limitación de intentos con caché persistente también se verificó en esta corrección.

Esta entrega aplica ATDD, BDD, TDD y un modelo de dominio simple al registro de usuarios de StockFácil. El informe sigue las cuatro fases de la consigna. La ejecución técnica no sustituye la participación y explicación de tres estudiantes: completa sus nombres y la validación del rol cliente.

## Archivos

- `informe-actividad.md`: fuente del informe académico.
- `registro-usuario.feature`: dos escenarios Gherkin, uno por criterio. La consigna también menciona un escenario como entrega mínima; se incluyen los dos que pide la fase BDD.
- `tdd/`: versiones históricas del test, implementación mínima y refactorización. La extensión `.php.txt` evita que los snapshots se ejecuten como pruebas o código de producción.
- `evidencias/`: salidas literales, JUnit, JSON, capturas reales, trazas Playwright y manifiesto SHA-256.
- Documentos finales desde la raíz del proyecto: `output/docx/actividad-registro-stockfacil.docx` y `output/pdf/actividad-registro-stockfacil.pdf`.

## Ejecutar las pruebas

Desde la raíz del proyecto, con PHP 8.3 y las dependencias instaladas:

```powershell
php vendor/phpunit/phpunit/phpunit --filter RegistrationDataTest
php vendor/phpunit/phpunit/phpunit --filter RegistrationTest
php vendor/phpunit/phpunit/phpunit
php vendor/laravel/pint/builds/pint --test
```

`RegistrationDataTest` es una prueba unitaria pura de preparación y normalización de datos; no demuestra persistencia. `RegistrationTest` cubre los escenarios completos mediante HTTP y SQLite en memoria, incluido hash, unicidad y login. El archivo Gherkin documenta esos comportamientos y se vincula con los métodos de PHPUnit; no se utilizó un intérprete Gherkin ni se afirma haber ejecutado Cucumber o Behat.

## Repetir las capturas

1. Crea una base SQLite separada y ejecuta en ella las migraciones y el seeder. No apuntes estas pruebas al inventario habitual.
2. En una terminal PowerShell configura `$env:DB_DATABASE` con la ruta absoluta de esa base; usa `$env:CACHE_STORE='file'` para conservar contadores entre solicitudes e inicia `php artisan serve --port=8005`.
3. Instala o proporciona Playwright y Chromium. El capturador admite `$env:PLAYWRIGHT_MODULE` con la ruta del módulo y `$env:REGISTRO_URL` con la dirección de la instancia.
4. En otra terminal, ejecuta `node docs/actividad-registro/evidencias/capturar-registro.cjs`. Para la segunda ronda usa `$env:REGISTRO_FASE='final'`. Cada ronda presupone que su correo de prueba no existe; usa una base nueva al repetirla. Guarda la evidencia histórica antes de repetir, pues el script escribe nombres de archivo estables.
5. Comprueba los JSON y las filas de SQLite. Un formulario que muestra una confirmación no prueba por sí solo la persistencia ni la protección de contraseña.

La captura inicial se ejecutó con `CACHE_STORE=array` para aislar contadores. El límite de diez POST por minuto se comprobó en una prueba HTTP con contador compartido durante el método; no se verificó entre procesos del servidor de capturas. Esta limitación queda explícita en el informe.

## Interpretar los resultados

La primera suite de preparación (`00-baseline`) incluyó el nuevo test unitario antes de crear su clase: 43 pruebas anteriores aprobadas, más un error de preparación. No es una línea base limpia anterior a los cambios. El RED unitario aislado, el RED HTTP y el fallo de login por mayúsculas tienen salidas separadas.

El fallo REG-09 fue real y se corrigió normalizando el correo también en `LoginRequest`. Las capturas iniciales y finales permanecen separadas. Los errores esperados de validación son casos aprobados cuando rechazan correctamente los datos; no se contabilizan como defectos.

No hay verificación de correo, recuperación de contraseña, roles, inventarios privados por cuenta ni validación humana del equipo. Son límites de esta entrega y no se incluyen en el porcentaje de los dos criterios. El registro habilita el acceso al inventario compartido de esta demostración local.
