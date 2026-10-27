# Auditoría interna de calidad de StockFácil

Fecha de revisión 27 de octubre de 2026, America/La_Paz. Revisión técnica asistida durante esta entrega, con fuentes y evidencia del repositorio. Responsables humanos del seguimiento propuestos Andre Romero Caballero y Santiago Camacho Echalar; su validación independiente permanece pendiente. No es un acta firmada ni una reunión de auditoría humana simulada.

## Objetivo y alcance

Comprobar correspondencia entre requisitos del docente, código, pruebas, resultados y documentación del plan Kanban. El alcance cubre acceso, catálogo, movimientos y alertas, infraestructura de pruebas, Git y archivos de evidencia. Se excluyen pentesting, evaluación exhaustiva de seguridad y certificación de calidad del producto completo.

## Elementos y criterios revisados

Se revisaron rutas, AuthController, ProductRequest, MovementRequest, InventoryService, Product, migraciones y pruebas de unidad e integración. Se contrastaron los scripts de navegador, XML JUnit, resultados Selenium, capturas Cypress, workflow, casos y CSV Kanban con los ocho apartados y evidencias del PDF. Criterios: reproducibilidad, ausencia de resultados inventados, consistencia transaccional, trazabilidad, protección de datos y registros Git auténticos.

La comprobación automática se conserva en docs/evidencias/auditoria-verificacion.json. Compara la huella de .env y el volcado lógico de la base habitual sin exportar sus valores. También comprueba exclusiones Git y busca patrones de claves privadas y tokens reconocibles en archivos de texto publicables. Esa búsqueda limitada no demuestra ausencia absoluta de secretos. Las contraseñas documentadas son fixtures locales de demostración, no secretos del usuario.

## Observaciones y acciones

| ID | Hallazgo verificado | Acción correctiva o seguimiento | Estado técnico |
| --- | --- | --- | --- |
| AUT-01 | Cypress seleccionaba dos botones de envío, guardar y logout; tres escenarios fallaron | Limitar selector al formulario data-submit-form; conservar ronda inicial y reejecutar | Corregido y reejecutado |
| AUT-02 | La prueba buscaba producto nuevo en primera página de un catálogo paginado; un escenario falló | Filtrar por SKU tras guardar; conservar ronda intermedia | Corregido; tres escenarios finales aprobados |
| NC-01 | No existía Git en la carpeta al inicio | Iniciar Git con identidad configurada, remoto proporcionado y commits reales | Registro local y main publicado |
| NC-02 | No había Test Plan autónomo actualizado con flujo Kanban | Crear ocho apartados, casos, métricas y reglas WIP | Documentación preparada para revisión humana |
| NC-03 | No hay evidencia de tablero Projects e Issues remotos creados | Publicar CSV y guía exacta; equipo crea y enlaza el tablero real | Pendiente de publicación y comprobación |
| NC-04 | No hay revisión cruzada humana ni participación de Santiago acreditada en GitHub | Cada integrante revisa y registra desde su cuenta; no asignar autorías ficticias | Pendiente humano |
| NC-05 | MAN-01 no tiene ejecución y aceptación humana | Santiago ejecuta el recorrido y Andre revisa evidencia | No ejecutado |
| OBS-01 | Workflow preparado; el resultado local no demuestra ejecución remota | Comprobar Actions, guardar URL y descargar artifact | Pendiente de comprobación remota |

Los dos hallazgos AUT son defectos de automatización. No se detectó un defecto nuevo confirmado de lógica de aplicación en esta ejecución. Los hallazgos históricos permanecen en su documentación y no se cuentan como nuevos o corregidos nuevamente.

## Resultados de control

Se comprobaron 64 pruebas PHPUnit con 423 aserciones, dos comprobaciones Selenium y tres escenarios Cypress finales aprobados. Los ocho casos críticos tienen referencia al código y a la evidencia. Las tres rondas Cypress permiten reproducir el paso de fallo a corrección. El plan tiene nueve actividades de prueba contando MAN-01; ocho ejecutadas y una no ejecutada. La aprobación de ejecutados es 100%; la ejecución global es 88,89%.

Las huellas de .env y de la base habitual se comparan en auditoria-verificacion.json y deben ser iguales para cerrar el control de preservación. Se verifican exclusiones de .env, SQLite y temporales; el resultado del escaneo de patrones y el número de archivos se obtienen de ese JSON. Los commits utilizan AndreRCRO y fechas reales; no prueban actividad humana del segundo integrante ni auditoría independiente.

## Seguimiento y conclusión

Andre coordina cierre documental y métricas; Santiago verifica pruebas y MAN-01. Ambos registran revisión cruzada y tablero. Se dispone de evidencia técnica reproducible y dos herramientas permitidas. El cierre académico completo depende de los pendientes humanos y remotos señalados. La ausencia de fallos finales no equivale a ausencia de defectos ni a aprobación del docente.

Mejoras inmediatas: publicar y enlazar tablero e Issues, abrir PR con revisión real, completar MAN-01 y verificar CI. Mejora posterior: ampliar compatibilidad de navegadores y medir cobertura de código con un instrumento apropiado, manteniendo el alcance explícito.
