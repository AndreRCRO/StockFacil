El proyecto contaba con pruebas PHPUnit y documentación histórica, pero carecía de un plan Kanban actualizado y de pruebas con las dos herramientas exigidas. Esta rama incorpora el Test Plan en Word y Markdown, ocho casos trazables, pruebas Selenium y Cypress, cuatro comprobaciones unitarias del estado de stock y un workflow compatible con Laravel 13 y SQLite.

El ejecutor prepara bases temporales propias, arranca el servidor, guarda evidencias y lo detiene al finalizar. La corrección AUT-01 limita el botón de envío al formulario probado; se conservan la ejecución fallida y la reejecución. Consultar docs/Resultados_Pruebas.md para los conteos finales verificables.

Validación: PHPUnit, Selenium, Cypress, compilación Vite y validación de Composer. Los informes incluyen auditoría, métricas y tareas Kanban. No se declara revisión humana ni aceptación del docente. El compañero debe revisar los cambios y ejecutar la exploración indicada en docs/Casos_de_Prueba.md.

Relacionar Issues reales con K-01 a K-11 de docs/Kanban_Tareas.csv antes de publicar. Revisión solicitada a Santiago Camacho Echalar, pendiente de su usuario GitHub y revisión efectiva.
