# Revisión de StockFácil y del informe de la actividad

Se revisaron las siete páginas de DinamicaSQA.pdf y las seis páginas de la consigna del docente antes de corregir el código. Están disponibles ambos archivos de referencia. La consigna exige tres integrantes, dos criterios y un escenario por criterio; su resumen acepta un escenario como mínimo. La entrega conserva dos.

## Estado observado antes de editar el código

Laravel 13.35.0, PHP 8.3.33 y SQLite. La configuración efectiva usa `database/database.sqlite` sin caché de configuración y `CACHE_STORE=file`. La consulta de entorno quedó en `evidencias/entorno-runtime.json`; no incluye claves ni contraseñas.

El registro usa las rutas GET/POST `/register`, RegistrationController, RegisterRequest, RegistrationData, RegisterUser y User. LoginRequest prepara el correo y AuthController autentica y regenera la sesión. La migración existente contiene un índice único en users.email. No se cambiaron rutas, vistas, migraciones ni módulos de inventario en esta corrección.

La primera ejecución restringida no pudo leer el bootstrap de Composer. Se resolvió ejecutando PHP con autorización fuera de ese aislamiento. No se considera un error de StockFácil. La suite inicial realmente ejecutada aprobó 52 pruebas y 378 aserciones antes de cambiar código. La prueba nueva del contrato completo también aprobó en su primera ejecución y se documenta como regresión.

## Diferencias encontradas en el informe

1. La prueba de RegistrationData no guarda cuentas ni comprueba autenticación. Se mantiene como auxiliar. La prueba principal ahora es `RegistrationWorkflowTest::test_registration_contract_creates_one_account_and_allows_authentication`, que revisa respuesta, mensaje, cantidad de usuarios, correo, hash y acceso.
2. La clase de datos mostrada como GREEN no implementa el registro. El informe muestra RegisterUser y las reglas que efectivamente se ejecutan.
3. La normalización añadida anteriormente era una mejora de comportamiento, no solo una refactorización. Se separan ahora la corrección GREEN y la extracción posterior de reglas y normalización, con código guardado en cada etapa y las mismas cuatro pruebas aprobadas antes y después.
4. Registro y login eran procesos distintos. El rechazo de un duplicado podía funcionar al registrar, mientras que el login aún trataba las mayúsculas de otro modo. Esa corrección anterior sí tiene evidencia: 54 archivos históricos coincidieron con su manifiesto previo. No se presenta como un nuevo RED.
5. La tabla de 11 pruebas carecía de detalle por fila. Se añadieron resultado esperado, observado, estado e identificador de evidencia, junto con JSON, capturas y trazas de una repetición nueva.
6. El cumplimiento técnico no implica aprobación del cliente. El informe deja pendiente la asignación y aprobación de ese rol.
7. El primer Gherkin no decía expresamente que se ingresaba el correo ni que se protegía la contraseña. El archivo y el informe ahora lo indican.
8. La portada identifica a Andre Romero Caballero y Santiago Camacho; se conservan esos nombres. El tercer integrante queda pendiente. Docente: Rolando Lara; asignatura: Software Quality Assurance; gestión: 2/2026.

## Fallos reales nuevos y corrección

Las pruebas nuevas observaron que el servicio RegisterUser podía crear una cuenta con una contraseña de siete caracteres o con nombre vacío si se llamaba directamente. También se podía registrar nuevamente un correo cuando un registro existente estaba guardado con espacios o mayúsculas. Esos datos se prepararon únicamente en SQLite en memoria para comprobar el caso; no se alteró la base habitual.

La primera ejecución tuvo cuatro pruebas: el contrato completo aprobó y tres fallaron. No se retiró código ni se introdujo una avería para fabricar el RED. La corrección mínima añadió validación al servicio, con consulta del correo ya guardado usando LOWER y TRIM. Después aprobaron las mismas cuatro pruebas con 27 aserciones.

La refactorización extrajo UserRegistrationRules y EmailNormalizer. RegisterRequest comparte las reglas, añade la confirmación y prepara la respuesta del formulario. RegisterUser vuelve a comprobar los datos cuando es llamado sin formulario. La confirmación es responsabilidad de la entrada HTTP, no un atributo persistido del usuario. RegistrationData sigue siendo un objeto auxiliar, no una prueba de creación de cuentas.

La suite final aprobó 60 pruebas y 419 aserciones. Pint aprobó. El navegador repitió los 11 casos con resultado aprobado. Además, diez solicitudes independientes con caché file fueron aceptadas para validación y la siguiente recibió HTTP 429; el JSON y la captura están incluidos.

## Unicidad de SQLite y alcance

Se probó por separado una inserción directa de un correo idéntico, sin la validación de aplicación: SQLite lanzó la excepción de unicidad y quedó un solo usuario. La normalización y la consulta de equivalencia protegen mayúsculas y espacios en los caminos de registro de la aplicación. El índice existente compara el valor almacenado; no se afirma que sea un índice funcional ni que normalice cualquier escritura SQL externa.

El proyecto no incorpora verificación de correo, recuperación de contraseña ni separación de inventarios por cuenta. No se incluyeron esas funciones en los criterios evaluados. La revisión por el rol cliente y la explicación oral de cada integrante continúan pendientes de personas reales.

## Integridad y evidencia

La base habitual conservó un usuario, 12 productos y 24 movimientos. Coincidieron sus huellas de datos y esquema, así como el hash del archivo .env. No se ejecutaron migraciones sobre esa base. Las pruebas HTTP utilizaron SQLite en memoria; el navegador utilizó una copia independiente en `tmp/correccion-sqa/navegador.sqlite`.

El archivo `evidencias/ejecuciones.json` identifica los comandos, códigos de salida y resultados de cada etapa. `evidencias/historia-verificada.json` relaciona los archivos históricos comprobados. Los snapshots de código completos se encuentran en `tdd/antes`, `tdd/green` y `tdd/refactor`, con extensión de texto para evitar su ejecución accidental.
