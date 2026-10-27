# Test Plan SQA de StockFácil

Universidad del Valle Univalle

Materia Software Quality Assurance

Docente Rolando Lara

Integrantes Andre Romero Caballero y Santiago Camacho Echalar

Fecha 27 de octubre de 2026

Versión 1.0 ágil con Kanban

## 1 Introducción

### 1.1 Propósito y estado verificado

StockFácil es una aplicación web para pequeños negocios que administra catálogo, existencias, entradas, salidas, alertas e historial con responsable y saldos. Este Test Plan permite al equipo y al docente reproducir las pruebas, revisar las evidencias y decidir el cierre de las tareas. La entrega verifica ocho casos críticos mediante 69 comprobaciones automatizadas aprobadas. La exploración y aceptación humanas y la revisión cruzada se mantienen como pendientes explícitos.

El plan aplica aseguramiento de calidad de software (SQA) al flujo continuo de Kanban. Cada tarea contiene criterio de aceptación, caso, resultado y evidencia antes de solicitar la revisión del compañero. Aprobar la automatización es una condición de cierre técnico; la aceptación del equipo exige además una revisión humana real.

### 1.2 Objetivos

Verificar autenticación y consistencia del inventario; evitar duplicación de SKU y movimientos inválidos; demostrar Selenium y Cypress con resultados comprobables; conservar una regresión de unidad e integración; relacionar tareas, casos, defectos y evidencias; comunicar riesgos y pendientes sin convertir la asignación de trabajo en participación ficticia.

### 1.3 Situación inicial y actualización ágil

La revisión encontró informes de SQA sobre HU-01 y HU-02 en docs/sqa y actividades posteriores de registro en docs/actividad-registro. No se encontró un Test Plan autónomo anterior de ocho apartados; los documentos disponibles son antecedentes y evidencias históricas, no una versión de plan que pueda compararse línea por línea. La suite de entrada aprobó 60 pruebas y 419 aserciones. La carpeta no tenía repositorio Git; se inició uno con identidad AndreRCRO y fechas reales.

| Aspecto | Antecedente encontrado | Actualización de esta entrega |
| --- | --- | --- |
| Organización | Informes y casos por actividad | Plan único con ocho apartados y anexos trazables |
| Flujo | No había tablero Kanban local definido | Cinco estados, WIP 2 y reglas de paso explícitas |
| Pruebas | PHPUnit y evidencias históricas de navegador | Regresión nueva, Selenium y tres escenarios Cypress |
| Unidad | Normalización de correo y datos de registro | Cuatro datos adicionales sobre estado de stock |
| Evidencia | Resultados de actividades previas | Nuevos XML, JSON, logs y capturas con fecha de esta entrega |
| Seguimiento | Hallazgos de actividades anteriores | AUT-01 y AUT-02 con fallo, corrección y reejecución real |
| CI y revisión | Sin workflow ni historial Git en la carpeta | Git iniciado, rama de pruebas, workflow e instrucciones de PR |

Se conservan los antecedentes sin sobrescribirlos ni atribuirles nuevos resultados. Las pruebas actuales se escribieron sobre código existente; no se declara TDD en esta entrega. Los escenarios Dado Cuando Entonces documentan aceptación y se vinculan con pruebas ejecutables.

## 2 Alcance

### 2.1 Producto y requisitos verificables

La arquitectura permanece en Laravel 13 con PHP 8.3, Blade, Eloquent, SQLite, Tailwind CSS 4 y Vite 7. Los puntos principales son rutas protegidas, Form Requests para validación e InventoryService para transacciones y saldos. El inventario es compartido entre cuentas: no existe separación por negocio ni autorización por roles.

| Área e historia | Requisitos y aceptación | Casos |
| --- | --- | --- |
| HU-03 Acceso al inventario | Credenciales válidas abren dashboard; inválidas no autentican; logout protege acceso posterior | CP-01 y CP-02 |
| HU-01 Catálogo de productos | Alta válida, SKU normalizado y único, stock inicial e historial coherentes | CP-03 y CP-04 |
| HU-02 Movimientos y alertas | Entrada suma; salida resta; rechazo preserva saldo e historial; cantidades positivas enteras; alerta en mínimo | CP-05 a CP-08 |

HU-01 y HU-02 proceden de las historias existentes; HU-03 identifica el requisito de autenticación para esta matriz y no altera los identificadores históricos de registro de cuentas.

### 2.2 Exclusiones y límites

Quedan fuera de la nueva matriz las pruebas de carga, accesibilidad exhaustiva, pruebas de penetración, compras, facturación, multiempresa, recuperación de contraseña y roles, que no se presentan como funcionalidades implementadas. El registro de cuentas, edición, desactivación, concurrencia y seeders permanecen en la regresión existente, aunque no tienen un caso nuevo de aceptación por cada variante. No se certifica compatibilidad con todos los navegadores ni despliegue productivo.

El alcance de entrega contiene ocho casos automatizados prioritarios y una exploración manual MAN-01 pendiente. La matriz completa incluye datos, precondiciones, pasos, esperado, obtenido, prioridad y evidencia. Los casos de aceptación automatizados no sustituyen la validación de los integrantes o del docente.

## 3 Estrategia de pruebas

### 3.1 Niveles y herramientas

| Tipo | Aplicación real | Estado |
| --- | --- | --- |
| Unidad | PHPUnit sobre EmailNormalizer, RegistrationData y estados de Product sin base de datos | 7 pruebas aprobadas |
| Funcional | Navegador Selenium para acceso y Cypress para catálogo y movimientos | 2 comprobaciones y 3 escenarios aprobados |
| Integración | HTTP Laravel, validaciones, Eloquent, SQLite, historial y concurrencia | Dentro de 57 pruebas Feature aprobadas |
| Aceptación | Criterios de los ocho CP expresados en pruebas; revisión humana separada | Técnica aprobada; aprobación humana pendiente |
| Regresión | Suite completa tras incorporar automatización y unidad; Cypress reejecutado tras correcciones | 64 PHPUnit y 3 Cypress aprobados |
| Exploración | MAN-01 con teclado, escritorio, móvil y recorrido de negocio | No ejecutada por personas |

Selenium y Cypress son prácticos para esta aplicación porque actúan sobre HTML servido por Laravel y no exigen sustituir Blade ni añadir una SPA. Se instalaron como dependencias de desarrollo, con versiones resueltas en package-lock.json. PHPUnit ya pertenecía al stack. No se instalaron TestLink ni Squash. La ejecución local utilizó Selenium WebDriver 4.51.0 con Edge y Cypress 16.2.0 con Electron 146.

### 3.2 Entorno y datos

PHPUnit usa SQLite en memoria; ConcurrencyTest genera un archivo temporal para dos procesos. scripts/run-browser-tests.mjs crea una base nueva por ejecución, aplica migraciones y datos de demostración, genera una clave de aplicación temporal y arranca PHP en un puerto libre. Al terminar detiene el servidor. La base y .env habituales no se sustituyen.

El entorno de navegador usa APP_ENV=sqa y sesiones y caché de base de datos, por lo que las solicitudes pasan por formularios y CSRF reales. La cuenta sqa@example.test y su contraseña SqaDemo2026! son fixtures sintéticos y se crean solo en la base temporal. No son secretos de GitHub ni credenciales productivas.

### 3.3 BDD y trazabilidad

Los tres escenarios de tests/Browser/inventario.feature siguen Dado Cuando Entonces y cubren acceso, unicidad de producto y saldo con alerta. CP-01 y CP-02 se ejecutan con Selenium; CP-03 y CP-04 con el primer escenario Cypress; CP-05 y CP-07 con el tercero; CP-06 con el segundo; CP-08 con PHPUnit. El archivo feature es una especificación legible, sin ejecutor Cucumber; la automatización asociada realiza las comprobaciones.

### 3.4 Priorización y CI

Se prioriza impedir accesos indebidos y pérdida de integridad del inventario. Después se comprueban unicidad, límites, mensajes y alertas. Las pruebas manuales evalúan comprensión y uso. La revisión de tablero ocurre por bloques de trabajo, sin sprints ni ceremonias de Scrum.

.github/workflows/pruebas.yml se activa con push, pull_request y ejecución manual. Prepara PHP 8.3 y Node 24, instala Composer y npm desde locks, crea .env de ejemplo y clave, compila Vite, ejecuta PHPUnit, Selenium con Chrome y Cypress con Electron y conserva evidencias incluso ante fallos. No requiere secretos ni un servicio externo de base de datos. El resultado remoto debe comprobarse en Actions y enlazarse antes de declararlo aprobado.

## 4 Roles y responsabilidades

| Integrante o rol | Responsabilidad propuesta | Revisión requerida |
| --- | --- | --- |
| Andre Romero Caballero | Catálogo, Test Plan, métricas y coordinación de calidad | Revisa trabajo y resultados de Santiago |
| Santiago Camacho Echalar | Movimientos, diseño y ejecución de pruebas, registro de defectos | Revisa trabajo y documentación de Andre |
| Ambos integrantes | Desarrollo, pruebas, correcciones, criterios y cuidado de datos | Calidad compartida y aceptación del equipo |
| Docente Rolando Lara | Evaluación académica y validación de la entrega | No se presume aprobación previa |

Las funciones de QA Lead, QA Champion y desarrollo se distribuyen entre dos personas. La validación del producto se resuelve entre el equipo y docente; no se inventa un Product Owner externo. Kanban no requiere Scrum Master. Los responsables del CSV son una propuesta operativa, no una declaración de actividades humanas ya realizadas.

Los commits de esta ejecución usan la identidad Git configurada de AndreRCRO. El asistente es apoyo técnico y no se agrega como colaborador. Santiago debe registrar sus aportes y revisión desde su propia cuenta. No se aprueba el PR en su nombre ni se modifican autores, fechas o historia para simular participación.

## 5 Ciclo de vida de las pruebas

| Etapa | Actividad y evidencia | Estado Kanban |
| --- | --- | --- |
| Preparación | Requisito, riesgo, responsable y aceptación; vincular caso | Pendiente |
| Implementación | Reutilizar código, escribir comprobaciones y actualizar plan | En desarrollo |
| Ejecución | Preparar datos aislados, ejecutar y guardar log o captura | En pruebas |
| Defecto | Registrar versión, reproducción, esperado, obtenido y causa | En corrección |
| Reejecución | Corregir, repetir caso fallido y regresión relacionada | En pruebas |
| Cierre | Revisar evidencias, actualizar métricas y registrar revisión humana | Terminado |

AUT-01 se detectó con tres fallos por selector ambiguo y se corrigió limitando la acción al formulario. La segunda ronda aprobó dos escenarios y descubrió AUT-02: la búsqueda del producto creado asumía que estaba en la primera página. Se añadió el filtro por SKU y la tercera ronda aprobó los tres escenarios. Se preservan las tres ejecuciones; son defectos de las pruebas y no errores nuevos confirmados de producto.

La tarea vuelve de En corrección a En pruebas antes del cierre. Cambiar código no basta para declarar resuelto un hallazgo. Las tareas técnicamente verificadas permanecen En pruebas mientras falte la revisión del compañero.

## 6 Criterios de entrada y salida

### 6.1 Definition of Ready y entrada a pruebas

Una tarea está lista para desarrollo cuando tiene requisito comprensible, prioridad, responsable acordado, criterio de aceptación y dependencias identificadas. Para iniciar pruebas se necesita una versión ejecutable, PHP y dependencias disponibles, datos aislados, resultado esperado definido y un caso trazable. Hay como máximo dos tareas En desarrollo; una tarea bloqueada conserva motivo y próxima acción.

### 6.2 Definition of Done y salida

Para cierre técnico se requieren criterios comprobados, resultado final sin fallos críticos, regresión correspondiente aprobada, evidencia guardada, cambios en Git y documentos sincronizados. Para mover a Terminado se añade la revisión humana cruzada y la resolución o aceptación explícita de pendientes. Los problemas de seguridad o integridad abiertos impiden aceptar la funcionalidad.

La entrega técnica cumple los ocho casos automatizados y las dos herramientas. El cierre del equipo queda condicionado a MAN-01, el tablero remoto y la revisión cruzada. Una CI no consultada no se trata como CI aprobada. Los criterios pendientes se registran como tales antes de entregar.

## 7 Métricas y control de calidad

### 7.1 Indicadores calculados

| Indicador | Valor | Interpretación |
| --- | --- | --- |
| Casos críticos CP planificados y ejecutados | 8 y 8 | Todos tienen evidencia técnica |
| Exploración manual planificada y ejecutada | 1 y 0 | MAN-01 pendiente de intervención humana |
| Total planificado y ejecutado | 9 y 8 | Ejecución 8/9 = 88,89% |
| Aprobados fallidos y no ejecutados | 8, 0 y 1 | Estados finales del plan |
| Aprobación sobre casos ejecutados | 100% | 8/8; no implica aceptación oficial |
| Comprobaciones automatizadas | 69 aprobadas | 64 PHPUnit, 2 Selenium y 3 Cypress |
| Aserciones PHPUnit | 423 | Unidad e integración combinadas |
| Cobertura de áreas del alcance | 3/3 = 100% | Acceso, catálogo y movimientos con alertas |
| Defectos nuevos confirmados de aplicación | 0 | Observación de esta ejecución |
| Defectos de automatización corregidos | 2/2 | AUT-01 y AUT-02 |

La matriz agrupa requisitos; las 69 comprobaciones son ejecuciones de herramientas y no se suman a los nueve casos. La cobertura de áreas no mide líneas ni ramas de código. No se calcula defect density porque no se definió una medida de tamaño de software para el denominador. Tampoco velocidad, lead time ni throughput humano, porque no hay períodos y cierres humanos registrados. Estos límites impiden inflar indicadores.

### 7.2 Revisiones y control

Se revisaron rutas, validaciones, servicio transaccional, modelos, pruebas, dependencias, evidencia y trazabilidad. La auditoría técnica interna se documenta en Auditoria_Interna_SQA.md. La documentación conserva observaciones, acciones y pendientes. Resultados_Pruebas.md y metricas.json se calculan sobre XML y JSON reales; no se copian cifras de informes históricos.

La guía y CSV relacionan K-01 a K-11 con casos y evidencias. Los estados locales proponen trabajo a revisar; el tablero Projects, los Issues y la aprobación del PR requieren publicación y acción real del equipo. Una captura preparada o un enlace de comparación no constituye un PR creado.

## 8 Riesgos y mitigación

| Riesgo real | Probabilidad | Impacto | Mitigación y seguimiento |
| --- | --- | --- | --- |
| Entrega al 28 de octubre y dos integrantes | Alta | Alto | Alcance limitado, WIP 2 y prioridad a ocho casos existentes |
| Confundir datos de prueba con inventario habitual | Media | Alto | Bases nuevas y hashes de integridad antes y después |
| Descarga de Cypress o driver no disponible | Media | Alto | Lock, instalación previa, logs y entorno compatible |
| Diferencia Windows local y Linux de CI | Media | Medio | Selenium Edge local y Chrome en CI; comprobar ejecución remota |
| Falta de revisión humana o participación acreditada | Alta | Alto | Mantener tareas En pruebas y registrar aportes reales del compañero |
| Projects Issues y PR sin publicación verificable | Alta | Alto | CSV y guías exactas; completar desde cuenta del equipo |
| Aviso de deprecación de Electron en Cypress 16 | Media | Medio | Versión fijada; elegir navegador instalado al actualizar |
| Confiar en porcentajes fuera del alcance | Media | Medio | Explicitar denominadores y no declarar cobertura de código |

Las mejoras inmediatas son completar la exploración y revisión cruzada, enlazar el tablero y guardar la URL de CI. Como mejora posterior se recomienda ampliar compatibilidad y cobertura instrumental cuando exista tiempo; no se añaden funcionalidades ajenas a la entrega.

## Anexo A Matriz y escenarios de aceptación

La matriz completa se encuentra en Casos_de_Prueba.md y se incorpora a la versión Word. Incluye CP-01 a CP-08 y MAN-01, con todos los campos de diseño y resultado. Los tres escenarios BDD están en tests/Browser/inventario.feature.

## Anexo B Resultados y evidencias

Resultados_Pruebas.md contiene totales, fórmulas, rondas fallidas y reejecución. docs/evidencias contiene XML PHPUnit y Cypress, JSON Selenium, capturas y logs. El manifiesto SHA-256 de evidencia permite comprobar integridad. Los documentos históricos permanecen en sus carpetas originales.

## Anexo C Kanban y GitHub

Kanban_Guia.md establece cinco estados y WIP 2. Kanban_Tareas.csv prepara once tareas con responsable, prioridad, aceptación y evidencia. GitHub_Entrega.md indica cómo publicar Issues, crear el tablero, abrir el PR y comprobar Actions. Pull_Request_SQA.md contiene la descripción revisable. El repositorio de entrega es https://github.com/AndreRCRO/StockFacil.

## Anexo D Auditoría y mejora continua

Auditoria_Interna_SQA.md registra la revisión técnica, acciones correctivas y seguimiento. Las conclusiones técnicas del asistente no sustituyen una revisión humana o evaluación del docente. El plan se actualiza cuando cambia alcance, aparece un defecto, se reejecuta una prueba o se completa una revisión; se preserva evidencia anterior y se registra el nuevo resultado.

## Fuentes

Plan SQA_web.pdf, consigna del docente, páginas 1 a 5, con tablas verificadas visualmente en páginas 3 y 4. Código y pruebas de StockFácil; informes históricos en docs/sqa y docs/actividad-registro.

Documentación oficial consultada el 27 de octubre de 2026: https://docs.cypress.io/app/continuous-integration/overview y https://docs.cypress.io/app/continuous-integration/github-actions para instalación y CI; https://www.selenium.dev/selenium/docs/api/javascript/ y https://www.selenium.dev/documentation/selenium_manager/ para WebDriver y gestión del driver. La consulta técnica orienta configuración; los resultados se sustentan en las ejecuciones locales conservadas.
