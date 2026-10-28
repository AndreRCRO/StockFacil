# Kanban de StockFácil

Fecha 27 de octubre de 2026. Equipo Andre Romero Caballero y Santiago Camacho Echalar. Kanban gestiona trabajo continuo sin sprints ni roles de Scrum obligatorios.

## Flujo y reglas

| Estado | Política para entrar y salir |
| --- | --- |
| Pendiente | Requisito, responsable propuesto, prioridad y criterio comprobable. Sale al cumplir Definition of Ready. |
| En desarrollo | Máximo dos tareas simultáneas para todo el equipo. Incluye cambios reales y actualización del caso. Sale cuando existe una versión ejecutable. |
| En pruebas | Ejecutar casos y guardar resultados. Un fallo conduce a En corrección; aprobar pruebas permite solicitar revisión cruzada. |
| En corrección | Registrar reproducción, causa y solución del defecto. Vuelve a En pruebas; no se cierra solo por cambiar código. |
| Terminado | Pruebas y regresión aprobadas, evidencia enlazada, documentación actualizada y revisión cruzada humana registrada. |

Prioridad crítica: requisitos del PDF, integridad del inventario y acceso. Alta: dos herramientas, auditoría y trazabilidad. Complementaria: ajustes de presentación. Un bloqueo conserva su estado, motivo, responsable y próxima acción; no cuenta como terminado.

## Responsables y revisión

Andre desarrolla catálogo y coordina plan y métricas; revisa cambios de Santiago. Santiago desarrolla movimientos y coordina diseño y ejecución de pruebas; revisa cambios de Andre. Ambos prueban y corrigen. El docente valida criterios académicos y aceptación final. Este reparto propuesto debe confirmarse en el tablero; no representa contribuciones ya realizadas por Santiago.

Definition of Ready: tarea entendida, criterio de aceptación, datos de entrada, dependencias resueltas y responsable acordado. Definition of Done: criterio probado, regresión aprobada, evidencia y commit enlazados, plan sincronizado y revisión del compañero registrada.

Revisar el tablero al iniciar y cerrar cada bloque de trabajo y antes de la entrega. Comprobar bloqueos, fallos y límite WIP; priorizar terminar antes de comenzar. No se programa ninguna reunión ficticia ni se imponen ceremonias de Scrum.

## Registro de defectos

Registrar ID, caso, versión, entorno, pasos, esperado, obtenido, severidad y evidencia. Mover a En corrección, aplicar solución en rama fix cuando corresponda y volver a En pruebas. Reejecutar el caso que falló y la regresión relacionada. El revisor humano confirma el cierre con fecha real.

## Tablero y trazabilidad

Las tareas importables se guardan en `docs/Kanban_Tareas.csv`. Los avances técnicos se separan de la aprobación humana. Una tarea con ejecución aprobada y sin revisión del compañero permanece En pruebas. No se fabrican fechas anteriores ni movimientos humanos del tablero.
