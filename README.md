# StockFácil

Sistema web local para administrar el inventario de pequeños negocios. Registra productos, entradas y salidas; muestra existencias, alertas y un historial con responsable y saldos anteriores/posteriores.

## Entrega SQA con Kanban del 27 de octubre de 2026

El [Test Plan actualizado](docs/Test_Plan_SQA.md) integra ocho apartados, Selenium, Cypress y la regresión PHPUnit. Consulta [casos](docs/Casos_de_Prueba.md), [resultados verificables](docs/Resultados_Pruebas.md), [auditoría](docs/Auditoria_Interna_SQA.md), [reglas Kanban](docs/Kanban_Guia.md) y [publicación en GitHub](docs/GitHub_Entrega.md). La versión Word es `docs/Test_Plan_SQA.docx`. Los informes anteriores conservan su alcance y fechas históricos.

Después de instalar dependencias, compila y ejecuta desde la raíz:

```powershell
npm run build
php vendor/phpunit/phpunit/phpunit --colors=never
npx cypress install
npm run test:selenium
npm run test:cypress
```

Las dos pruebas de navegador preparan automáticamente una base SQLite nueva y datos de prueba, arrancan un servidor PHP en puerto libre y lo detienen al finalizar. Requieren Internet la primera vez para el ejecutable de Cypress y el driver de Selenium; usan Edge en Windows o Chrome en Linux. Las evidencias se guardan en `docs/evidencias/`. Para elegir otro navegador, define `SQA_BROWSER` para Selenium o `SQA_CYPRESS_BROWSER` para Cypress antes de ejecutar. No apuntes estos scripts a tu inventario habitual.

El workflow `.github/workflows/pruebas.yml` ejecuta las tres herramientas en push y pull_request. La exploración manual, aceptación y revisión del compañero se registran por separado; no se deducen de una prueba automatizada aprobada.

## Tecnologías y requisitos

- PHP 8.3 o superior con las extensiones de Laravel, especialmente `pdo_sqlite`, `sqlite3`, `mbstring`, `intl`, `openssl`, `fileinfo`, `curl`, `dom` y `xml`.
- Composer 2.
- Node.js 22.12 o superior compatible con Vite 7 y npm.
- Laravel 13, Blade, Eloquent, Tailwind CSS 4, Vite 7 y PHPUnit 12.
- SQLite local. No necesitas XAMPP, MySQL, Docker ni un servidor de base de datos.

Comprueba las herramientas antes de instalar:

```powershell
php -v
php -m
composer --version
node -v
npm -v
```

## Instalar en otra computadora

Abre una terminal en la carpeta del proyecto y ejecuta:

```powershell
composer install
php -r "file_exists('.env') || copy('.env.example', '.env');"
php artisan key:generate
php -r "file_exists('database/database.sqlite') || touch('database/database.sqlite');"
php artisan migrate --seed
npm ci
npm run build
php artisan serve
```

Abre [StockFácil en localhost](http://127.0.0.1:8000). La página de inicio de sesión debe aparecer. Si el puerto está ocupado, ejecuta `php artisan serve --port=8002` y abre ese puerto.

Como alternativa, `composer run setup` instala dependencias, genera la clave y crea la base con sus datos de ejemplo. Úsalo para preparar una instalación local; genera una nueva clave de aplicación.

### SQLite

El archivo `.env` debe tener:

```dotenv
DB_CONNECTION=sqlite
APP_TIMEZONE=America/La_Paz
```

No necesitas definir `DB_DATABASE`: la conexión usa `database_path('database.sqlite')`. Si defines esa variable, proporciona la ruta absoluta a tu archivo SQLite. No apuntes las pruebas a tu archivo de desarrollo.

`database/database.sqlite` y sus archivos auxiliares están excluidos de Git. Conserva las migraciones y los seeders para reconstruir la demostración. Antes de trasladar datos reales, detén el servidor y realiza una copia del archivo SQLite.

### Administrador de demostración

Las credenciales locales predeterminadas son:

| Campo | Valor |
| --- | --- |
| Correo | `admin@stockfacil.test` |
| Contraseña | `StockFacil2026!` |

Para cambiarlas, edita `.env`:

```dotenv
ADMIN_NAME=Administrador
ADMIN_EMAIL=admin@stockfacil.test
ADMIN_PASSWORD=StockFacil2026!
```

Si el nombre contiene espacios, enciérralo entre comillas. Después aplica los cambios:

```powershell
php artisan config:clear
php artisan db:seed
```

El seeder actualiza el nombre y la contraseña del usuario identificado por `ADMIN_EMAIL`. Cambiar el correo crea un usuario con el nuevo correo; no elimina el anterior. La actividad de registro incorpora **Crear cuenta** en `/register`. Las cuentas registradas acceden al mismo inventario compartido; no hay gestión de roles ni separación por negocio. Estas credenciales se proporcionan para desarrollo local.

### Actividad de registro de usuarios

En **Iniciar sesión → Crear cuenta**, ingresa nombre, correo, contraseña de al menos ocho caracteres y su confirmación. El sistema rechaza correos duplicados, normaliza el correo y guarda la contraseña mediante el cast `hashed` de Eloquent. Tras registrarte, inicia sesión con la cuenta creada.

Consulta [la actividad ATDD BDD TDD y DDD](docs/actividad-registro/README.md) y [su corrección con evidencias reproducibles](docs/actividad-registro/correccion/README.md). El servicio de registro valida sus entradas incluso al usarse sin formulario, y el registro y el login comparten la normalización del correo. Los informes SQA del 13 de octubre conservan su alcance y resultados históricos.

### Datos de ejemplo

`php artisan db:seed` crea cinco categorías, doce productos y veinticuatro movimientos. El inventario de demostración comienza con 184 unidades, cinco alertas y dos productos agotados. Todas las cifras se consultan desde SQLite.

Los productos se identifican por SKU. Repetir el seeder no duplica sus movimientos ni restablece existencias que hayas modificado. El administrador sí recibe la contraseña definida en `.env` cada vez que ejecutas el seeder.

## Iniciar y trabajar con estilos

Con los recursos compilados basta con iniciar Laravel:

```powershell
php artisan serve
```

También puedes usar `composer run dev` para ese servidor. Para modificar estilos o JavaScript con recarga de Vite, abre una segunda terminal:

```powershell
npm run dev
```

Al terminar, detén Vite con Ctrl+C y compila para ejecutar sin el servidor de recursos:

```powershell
npm run build
```

La tipografía Manrope se distribuye como archivos locales mediante Vite. La aplicación no depende de fuentes alojadas en un servicio externo.

## Usar el sistema

1. Inicia sesión con el administrador.
2. Abre **Productos → Nuevo producto** y completa los campos obligatorios.
3. Usa **Registrar entrada** o **Registrar salida** para modificar existencias.
4. Revisa **Stock bajo** para planificar reposiciones.
5. Consulta **Movimientos** y filtra por producto o tipo.

El stock inicial positivo crea una entrada. La edición del producto no permite modificar stock. Las salidas superiores al saldo, las cantidades inválidas y los movimientos de productos inactivos se rechazan. Desactivar conserva el historial.

Una alerta incluye productos activos con stock menor o igual al mínimo. Los productos con cero unidades se muestran como **Agotado**, y también cuentan dentro de las alertas.

## Ejecutar pruebas

Ejecuta la suite funcional:

```powershell
php artisan test
```

O ejecuta las pruebas de una historia:

```powershell
php artisan test --filter=ProductTest
php artisan test --filter=InventoryTest
php artisan test --filter=ConcurrencyTest
```

`phpunit.xml` configura SQLite `:memory:` para las pruebas HTTP. `ConcurrencyTest` crea su propio archivo temporal, lanza dos procesos PHP y elimina ese archivo. La suite no modifica `database/database.sqlite`. La prueba concurrente requiere que PHP permita ejecutar procesos mediante Symfony Process.

Para comprobar formato y configuración:

```powershell
vendor/bin/pint --test
composer validate
```

En PowerShell puedes invocar el formateador con `php vendor/laravel/pint/builds/pint --test`.

Consulta [la evidencia de verificación](docs/verificacion.md) para los resultados ejecutados. Los casos planificados están en [casos-prueba.md](docs/casos-prueba.md).

## Estructura

```text
app/Models/                 User, Category, Product, Movement
app/Http/Controllers/       Autenticación, dashboard, productos y movimientos
app/Http/Requests/          Validaciones y normalización
app/Services/InventoryService.php
config/database.php        Única conexión: SQLite
config/stockfacil.php       Credenciales configurables
routes/web.php             Rutas públicas y protegidas
resources/views/           Vistas y componentes Blade
resources/css/app.css      Diseño Bento y adaptación responsiva
resources/js/app.js        Menú, confirmación y vista previa de stock
lang/es/                   Validaciones y paginación en español
database/migrations/       Estructura y restricciones de SQLite
database/seeders/          Administrador y datos de demostración
tests/Feature/             Pruebas HTTP, servicio, seeder y concurrencia
tests/Support/             Proceso auxiliar de prueba concurrente
docs/                      Historias, arquitectura, casos y evidencia
```

## Documentación académica

- [Historias HU-01 y HU-02 y criterios de aceptación](docs/historias-usuario.md).
- [Arquitectura y estrategia de concurrencia SQLite](docs/arquitectura.md).
- [Casos de prueba planificados](docs/casos-prueba.md).
- [Verificación técnica ejecutada](docs/verificacion.md).
- [Sistema visual](DESIGN.md).

Las actividades formales de revisión, inspección y auditoría SQA quedan para una evaluación posterior. No se presentan resultados ficticios de esas actividades.

## Solución de problemas

- **`could not find driver`:** verifica el `php.ini` utilizado con `php --ini` y activa `pdo_sqlite` y `sqlite3`.
- **Archivo SQLite inexistente:** ejecuta el comando de creación del archivo antes de migrar.
- **`Vite manifest not found`:** ejecuta `npm ci` y `npm run build`.
- **Página sin estilos tras cerrar Vite:** si un cierre forzado dejó `public/hot`, elimina solo ese archivo y ejecuta `npm run build`.
- **Configuración antigua:** ejecuta `php artisan config:clear` después de cambiar `.env`.
- **Base bloqueada:** cierra herramientas que mantengan transacciones de escritura abiertas. SQLite admite un escritor a la vez y la conexión espera hasta cinco segundos.

La instalación de desarrollo usa `APP_DEBUG=true`. Si preparas otro entorno, revisa las credenciales y la configuración de Laravel antes de exponerlo públicamente.
