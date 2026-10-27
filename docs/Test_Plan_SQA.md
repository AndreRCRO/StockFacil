# Plan de pruebas de StockFácil

Universidad del Valle Univalle

Materia Software Quality Assurance

Docente Rolando Lara

Integrantes Andre Romero Caballero y Santiago Camacho Echalar

27 de octubre de 2026

## 1 Introducción

StockFácil es un sistema web para administrar el inventario de un pequeño negocio. Permite registrar productos, anotar entradas y salidas, consultar los movimientos y reconocer cuándo hace falta reponer un producto.

Este plan explica qué se revisó, cómo se hicieron las pruebas y qué resultados se obtuvieron. Se trabajó sobre el proyecto existente y se añadieron pruebas para comprobar sus funciones principales.

Ya existían casos de prueba e informes de actividades anteriores, pero no se encontró un plan completo organizado para Kanban. Esta versión reúne lo necesario para esta entrega y conserva los resultados anteriores por separado.

## 2 Alcance

La revisión se concentró en tres partes del sistema:

| Parte del sistema | Qué se espera comprobar |
| --- | --- |
| Inicio y cierre de sesión | Entrar con datos correctos, rechazar datos incorrectos y proteger las páginas privadas. |
| Registro de productos | Guardar un producto con sus existencias iniciales y evitar códigos SKU repetidos. El SKU es el código que identifica al producto. |
| Entradas, salidas y alertas | Sumar y restar unidades correctamente, impedir salidas mayores al saldo y mostrar una alerta al llegar al mínimo. |

Se priorizaron estas funciones porque un error en ellas afectaría el acceso o las cantidades del inventario. No se incluyeron pruebas de carga con muchos usuarios ni una revisión completa de seguridad.

## 3 Estrategia de pruebas

Se usaron **Selenium y Cypress**, las dos herramientas elegidas entre las permitidas por el docente. Ambas abren el sistema en un navegador y comprueban acciones como iniciar sesión, guardar un producto o registrar una salida. También se utilizó **PHPUnit** para revisar reglas pequeñas y la relación entre las funciones y los datos guardados.

Las pruebas utilizaron datos de ejemplo en una base separada. Así se pudo repetir el trabajo sin modificar el inventario habitual. Después de corregir un problema en una prueba, se volvió a ejecutar para comprobar el resultado.

Los ocho casos principales quedaron así:

| Caso | Qué se probó | Resultado esperado y comprobado |
| --- | --- | --- |
| CP-01 | Iniciar y cerrar sesión. | Se abre el sistema con datos correctos y se pierde el acceso al cerrar sesión. |
| CP-02 | Intentar entrar sin sesión o con contraseña incorrecta. | Se solicita iniciar sesión y se muestra el error correspondiente. |
| CP-03 | Registrar un producto con 10 unidades. | El producto aparece en el listado con sus 10 unidades y su movimiento inicial. |
| CP-04 | Repetir el código de un producto. | Se rechaza el código repetido, incluso escrito en minúsculas. |
| CP-05 | Agregar 5 unidades a un producto con 10. | El saldo pasa a 15 y la entrada queda en el historial. |
| CP-06 | Intentar sacar 11 unidades cuando solo hay 10. | Se rechaza la salida y se conservan el saldo y el historial. |
| CP-07 | Dejar un producto en su mínimo de 3 unidades. | El saldo queda en 3 y aparece la alerta de stock bajo. |
| CP-08 | Usar cantidades cero, negativas, decimales o sin valor. | Se rechazan las cantidades inválidas sin cambiar las existencias. |

Todos estos casos aprobaron. Además, quedó preparada una revisión manual para recorrer las pantallas en computadora y celular, probar el teclado y valorar si los mensajes son claros. Esa revisión todavía está pendiente.

Para expresar lo esperado antes de probar, se usaron estos ejemplos de **Dado, Cuando y Entonces**, conocidos como BDD:

- **Acceso:** dado un usuario registrado, cuando ingresa datos correctos, entonces puede entrar; cuando cierra sesión, debe volver a identificarse. Corresponde a CP-01 y CP-02.
- **Productos:** dado un producto ya guardado, cuando se intenta repetir su código, entonces el sistema lo rechaza. Corresponde a CP-03 y CP-04.
- **Inventario:** dado un producto con 10 unidades y mínimo de 3, cuando se agregan 5 y se retiran 12, entonces quedan 3 y aparece la alerta. Una salida mayor al saldo debe rechazarse. Corresponde a CP-05, CP-06 y CP-07.

Estos ejemplos se relacionaron con las pruebas del proyecto. No se afirma que se desarrolló con TDD, porque las pruebas de esta entrega se añadieron a un sistema que ya existía.

## 4 Roles y responsabilidades

La calidad es una responsabilidad compartida. Ambos integrantes pueden desarrollar, probar y corregir. El reparto propuesto es el siguiente:

| Integrante | Responsabilidad |
| --- | --- |
| Andre Romero Caballero | Trabajar en productos, actualizar el plan y los resultados, y revisar el trabajo de Santiago. |
| Santiago Camacho Echalar | Trabajar en movimientos, preparar y ejecutar pruebas, y revisar el trabajo de Andre. |

La revisión del compañero debe registrarse cuando realmente se haga. Las tareas asignadas no se presentan como prueba de participación ya realizada.

## 5 Ciclo de vida de las pruebas

Se eligió **Kanban** porque permite organizar el trabajo de dos personas con un flujo sencillo:

**Pendiente → En desarrollo → En pruebas → En corrección, si falla → En pruebas → Terminado.**

Antes de comenzar se define qué debe hacer la tarea y cómo se comprobará. Durante el desarrollo se preparan las pruebas. Si algo falla, se registra qué pasó, se corrige y se vuelve a probar. La tarea termina cuando las pruebas aprueban, queda evidencia y el compañero realiza su revisión.

El límite es de **dos tareas al mismo tiempo en desarrollo**. Se revisa el avance al iniciar y cerrar cada bloque de trabajo. Se atienden primero los problemas de acceso y de cantidades del inventario.

Se prepararon once tareas con responsables, prioridad y resultados esperados. La publicación de los Issues y del tablero de GitHub, y la revisión del cambio propuesto, siguen pendientes del equipo.

## 6 Criterios de entrada y salida

**Para empezar una tarea, Definition of Ready:** se entiende lo que hay que hacer, existe un responsable, se conoce el resultado esperado y están disponibles los datos necesarios.

**Para empezar las pruebas:** el sistema funciona, se dispone de una versión para revisar y se utilizan datos de prueba separados del inventario habitual.

**Para terminar, Definition of Done:** la función cumple lo esperado, sus pruebas aprueban, los problemas encontrados se corrigieron, se guardaron los resultados y el compañero revisó el trabajo. Si falta esa revisión, la tarea permanece en pruebas.

## 7 Métricas y control de calidad

Los resultados de las herramientas fueron:

| Herramienta | Comprobaciones aprobadas | Fallidas al finalizar |
| --- | --- | --- |
| PHPUnit | 64 | 0 |
| Selenium | 2 | 0 |
| Cypress | 3 | 0 |
| Total | 69 | 0 |

Estas 69 comprobaciones sirven para revisar los ocho casos principales y otras reglas del sistema. No son 69 casos distintos del plan.

Los **8 casos principales aprobaron**. La revisión manual sigue sin ejecutar: por eso, al contar las nueve actividades previstas, se completaron 8 de 9, es decir, **88,89%**. La aprobación entre los casos ejecutados fue del **100%**. Se probaron las tres partes incluidas en el alcance; esto no significa que se haya revisado todo el código o que el sistema esté libre de errores.

Las siguientes capturas se guardaron durante las pruebas del 27 de octubre. Se incluyen junto a su explicación para mostrar los resultados más importantes.

Al registrar el producto de prueba, el listado mostró su código CY-ALTA y sus **10 unidades**.

![Producto de prueba registrado con 10 unidades](evidencias/cypress/inventario.cy.js/CP-03-producto-creado.png)

Cuando se intentó retirar **11 unidades de un producto que solo tenía 10**, el sistema mostró el mensaje de stock insuficiente. La prueba también comprobó que no se cambiaron las existencias ni se agregó un movimiento rechazado al historial.

![Salida rechazada porque la cantidad supera las existencias](evidencias/cypress/inventario.cy.js/CP-06-stock-insuficiente.png)

Después de una salida válida, el producto CY-MOV quedó con **3 unidades**, el mismo valor de su mínimo, y apareció con la alerta **Stock bajo**.

![Producto con tres unidades y alerta de stock bajo](evidencias/cypress/inventario.cy.js/CP-07-alerta-minimo.png)

**Qué se corrigió.** Al preparar Cypress aparecieron dos problemas en las propias pruebas: una seleccionaba más de un botón y otra buscaba el producto nuevo solo en la primera página del listado. Se ajustaron ambas y los tres escenarios aprobaron al repetirlos. No se detectó un error nuevo confirmado en las funciones del inventario durante esta revisión.

**Revisión de calidad.** Se comprobó que los casos correspondieran a las funciones existentes, que los resultados coincidieran con las ejecuciones y que los archivos de configuración y el inventario habitual no hubieran cambiado. Esta revisión técnica quedó registrada; la revisión entre los integrantes sigue pendiente.

Los cambios se guardaron en el [repositorio de StockFácil](https://github.com/AndreRCRO/StockFacil/tree/test/sqa-kanban). También se configuró GitHub Actions para ejecutar las pruebas cuando se suben cambios. La [ejecución comprobada en GitHub](https://github.com/AndreRCRO/StockFacil/actions/runs/40573878583) terminó correctamente. Esto permite detectar si un cambio posterior rompe algo que ya funcionaba.

## 8 Riesgos y mitigación

| Riesgo | Probabilidad e impacto | Qué se hace para reducirlo |
| --- | --- | --- |
| Poco tiempo antes de la entrega. | Alta y alto. | Concentrar el trabajo en las funciones principales y mantener el límite de dos tareas. |
| Cambiar por error el inventario habitual al probar. | Media y alto. | Usar datos separados y comprobar que la base habitual se conserva. |
| Problemas al instalar o ejecutar las herramientas. | Media y medio. | Dejarlas instaladas, conservar los comandos y comprobar que también funcionan en GitHub. |
| Entregar sin revisión del compañero o sin tablero publicado. | Alta y alto. | Mantener esos pendientes visibles y completarlos con participación real de ambos integrantes. |

Antes de cerrar la entrega, el equipo debe publicar el tablero y los Issues, revisar el cambio propuesto y ejecutar el recorrido manual en computadora y celular. Después se actualiza el resultado con la fecha y las evidencias de esa revisión.

El plan se ajusta cada vez que cambia una tarea, aparece un problema o se repite una prueba. Así la calidad se revisa durante el trabajo y no solamente al final.
