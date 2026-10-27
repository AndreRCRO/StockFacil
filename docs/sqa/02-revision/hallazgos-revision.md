# Hallazgos de revisión técnica preliminar

Fecha de elaboración: 13 de octubre de 2026. Hallazgos documentados inicialmente antes de aplicar las acciones. Revisión por otro equipo: pendiente.

| ID | Historia | Hallazgo | Evidencia | Importancia | Acción | Estado inicial / actual |
| --- | --- | --- | --- | --- | --- | --- |
| HR-01 | Ambas | CP-06 previo y CP-06 de la actividad designan casos distintos. | docs/casos-prueba.md y consigna, sección 8. | Bajo, documental | Namespace SQA/CP y trazabilidad a métodos. | Pendiente / Corregido documentalmente |
| HR-02 | Ambas | No hay revisión externa ni sesión formal de inspección por pares acreditadas. | Campos pendientes de consigna; documentos previos. | Medio, de proceso | Completar equipo, participantes, roles, observaciones y firmas reales. | Pendiente / Pendiente |
| HR-03 | Ambas | No se aportó plan/rúbrica de calidad del curso ni auditoría independiente aprobada. | Material recibido y alcance de la consigna. | Medio, de alcance | Validar los doce CA técnicamente y solicitar evaluación formal de estándares. | Pendiente / Pendiente |
| HR-04 | HU-02 | Mensaje de rango decía El cantidad; regla de rechazo sí funcionaba. | resultados-navegador-antes.json; hu02-error-cero-antes.png; regresion-antes.xml. | Bajo, claridad | MovementRequest::messages para quantity.min/max; regresión y capturas posteriores. | Pendiente / Corregido y verificado |

## Observaciones de revisión

No se detectó una discrepancia funcional entre la planificación de los doce CA y los casos ejecutados. HR-04 es un defecto de redacción; no se presenta como pérdida de stock ni se borra su evidencia anterior. HR-02 y HR-03 son límites del proceso académico y no defectos de la aplicación.

La primera preparación de la prueba de regresión tuvo una llamada de aserción inválida del propio test. Ese registro se conserva como regresion-preparacion-error.txt/xml, separado de la regresión válida; no se cuenta como defecto de StockFácil. Tras corregir la llamada, la regresión válida reprodujo tres fallos de mensajes antes del cambio de producción.

## Equipo externo

- Equipo externo o auditor designado: [Completar].
- Integrantes y roles: [Completar].
- Fecha de actividad formal: [Completar].
- Observaciones oficiales: [Completar].
- Resultado aprobado por el responsable independiente: [Completar].
- Firma o validación: [Completar].

La elaboración técnica por Codex no acredita la participación de otro equipo, una reunión de inspección ni una auditoría del docente.
