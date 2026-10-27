# Arquitectura de StockFácil

StockFácil sigue el patrón Modelo–Vista–Controlador (MVC) de Laravel. Blade genera las páginas del servidor; Eloquent consulta SQLite; Vite compila Tailwind CSS y JavaScript.

## Flujo de una solicitud

1. `routes/web.php` define la ruta y aplica `auth` a las páginas internas.
2. Un Form Request valida y normaliza los datos recibidos.
3. El controlador coordina la consulta o invoca `InventoryService`.
4. Eloquent persiste los datos y establece las relaciones.
5. El controlador devuelve una vista Blade o una redirección con confirmación.

Las vistas no contienen cifras de inventario prefijadas. Los indicadores se calculan desde los productos activos y el historial se consulta con relaciones precargadas para evitar consultas repetidas por fila.

## Módulos

| Módulo | Responsabilidad |
| --- | --- |
| Autenticación | Inicio y cierre de sesión, hash de contraseña, regeneración de sesión y límite de intentos. |
| Dashboard | Cantidad de productos activos, unidades, alertas, agotados y últimos movimientos. |
| Productos | Creación, edición, búsqueda por nombre/SKU, categoría y desactivación. |
| Existencias | Entradas y salidas mediante un servicio transaccional. |
| Alertas | Productos activos con stock menor o igual al mínimo, incluidos los agotados. |
| Historial | Consulta paginada por producto y tipo, sin operaciones de modificación. |

## Base de datos

La única conexión configurada es SQLite. El archivo local es `database/database.sqlite`, excluido de Git junto con sus archivos auxiliares WAL/SHM. Las migraciones y los seeders permiten reconstruir el inventario de demostración.

| Modelo | Datos principales | Relaciones |
| --- | --- | --- |
| `User` | Nombre, correo, contraseña con hash. | Responsable de movimientos mediante `Movement::user`. |
| `Category` | Nombre único. | Una categoría tiene muchos productos. |
| `Product` | SKU único, nombre, precio, descripción, stock, mínimo, activo y fechas. | Pertenece a una categoría; tiene muchos movimientos. |
| `Movement` | Tipo, cantidad, saldo anterior/posterior, observación, usuario y fecha. | Pertenece a un producto y a un usuario. |

Las claves foráneas restringen la eliminación de productos y usuarios con historial. Los triggers de la migración refuerzan cantidades no negativas y la coherencia aritmética de los movimientos, porque SQLite no hace cumplir `unsigned` como otros motores.

El proyecto conserva las migraciones auxiliares del esqueleto de Laravel. Las sesiones y la caché se almacenan en archivos; no necesita procesos de colas ni servidores externos.

## Servicio de inventario

`InventoryService::createProduct` crea el producto con saldo cero. Si hay unidades iniciales, llama a `record` para registrar su primera entrada. Ambas operaciones comparten una transacción; si el movimiento falla, no queda un producto incompleto.

`InventoryService::record` verifica tipo, cantidad positiva, producto activo, stock suficiente y límite de unidades. Guarda el nuevo saldo y el movimiento en la misma transacción. No se usa `lockForUpdate`, porque SQLite no implementa ese bloqueo por fila.

### Concurrencia en SQLite

Se configura WAL y un tiempo de espera de 5 segundos. La primera sentencia del servicio es una actualización sin cambio de saldo para adquirir el bloqueo de escritura antes de leer. SQLite admite un escritor a la vez, de modo que la segunda solicitud consulta el saldo después de la primera. Una actualización condicional verifica además el saldo anterior y el estado activo.

La opción `IMMEDIATE` de Laravel complementa esta estrategia en PHP 8.4 o superior. En PHP 8.3, Laravel inicia una transacción diferida; por eso el bloqueo se obtiene explícitamente con la primera escritura. Laravel reintenta hasta cinco veces los errores de concurrencia reconocidos dentro de la transacción. Una contención prolongada puede agotar la espera; la transacción no deja un saldo parcial.

`ConcurrencyTest` ejecuta dos procesos PHP contra un archivo temporal: ambos intentan retirar 7 unidades de un saldo de 10. Solo uno se acepta; el saldo final es 3 y solo se agrega una salida.

## Presentación y accesibilidad

El dashboard usa una cuadrícula Bento de proporciones distintas. Las páginas comparten navegación, colores, tipografía local y componentes Blade para campos, alertas, estados y paginación. Las tablas mantienen su desplazamiento dentro del contenedor. El menú móvil ofrece cierre con Escape y gestión de foco. Los formularios conservan la entrada inválida y muestran errores junto al campo y en el resumen.

## Ampliación futura

Los controladores dependen del servicio para modificar existencias. Una futura API podría reutilizar ese servicio después de validar y autenticar sus solicitudes. Esta versión no incorpora API REST ni Flutter.
