# Requisitos del docente y estado de entrega

Fuente principal: Plan SQA_web.pdf, cinco páginas, proporcionado por Andre. Se extrajo el texto y se inspeccionaron visualmente las tablas de las páginas 3 y 4, que están incrustadas como imágenes. La consigna constituye la referencia académica; las decisiones de implementación proceden de la solicitud del equipo y del código real.

| ID | Requisito o evidencia | Localización | Estado verificable |
| --- | --- | --- | --- |
| RD-01 | Describir el marco ágil y roles de calidad, página 2 | Test Plan secciones 1, 4 y Kanban_Guia.md | Kanban definido para dos integrantes |
| RD-02 | Revisar plan anterior y adaptar estrategia continua, página 2 | Test Plan 1 | Se contrastaron informes previos; no se encontró Test Plan autónomo anterior |
| RD-03 | Usar dos entre TestLink, Squash, Selenium y Cypress, página 2 | tests/Browser y cypress/e2e | Selenium y Cypress ejecutados |
| RD-04 | Aplicar TDD, BDD o ATDD, página 2; repositorio con BDD o unitarias, página 3 | tests/Browser/inventario.feature y tests/Unit | Tres escenarios BDD vinculados; unidad ejecutada; no se atribuye TDD nuevo |
| RD-05 | Integración continua y priorización por valor, página 2 | .github/workflows/pruebas.yml y Test Plan 3 | Ejecución 40573040837 aprobada y artifact verificado |
| RD-06 | Introducción y alcance, página 3 | Test Plan 1 y 2 | Documentados sobre el producto real |
| RD-07 | Estrategia con unidad, integración, aceptación, regresión, exploración y herramientas, página 3 | Test Plan 3 y Casos_de_Prueba.md | Automatización ejecutada; exploración humana pendiente |
| RD-08 | Roles y ciclo de vida de pruebas, página 3 | Test Plan 4 y 5 | Reparto propuesto, sin simular colaboración humana |
| RD-09 | Definition of Ready y Definition of Done, página 3 | Test Plan 6 y Kanban_Guia.md | Políticas explícitas, WIP 2 |
| RD-10 | Métricas y control de calidad, página 3 | Test Plan 7 y Resultados_Pruebas.md | Indicadores calculados con XML y JSON |
| RD-11 | Riesgos y mitigación, página 3 | Test Plan 8 | Técnicos, entrega, acceso y validación |
| RD-12 | Repositorio del proyecto con pruebas, página 3 | https://github.com/AndreRCRO/StockFacil | main y test/sqa-kanban publicados; revisión pendiente |
| RD-13 | Informe breve de auditoría, página 3 | Auditoria_Interna_SQA.md | Revisión técnica con límites y seguimiento |
| RD-14 | Integrar plan con tablero ágil, página 3 | Kanban_Tareas.csv, Kanban_Guia.md y GitHub_Entrega.md | Trazabilidad local preparada; Projects remoto pendiente |
| RD-15 | Resultados, indicadores y mejoras, página 3 | Resultados_Pruebas.md y docs/evidencias | Resultados reales; fallos de prueba conservados |
| RD-16 | Colaboración continua desarrollo y QA, página 4 | Kanban_Guia.md y PR preparado | Revisión humana y evidencia de Santiago pendientes |

## Ponderación académica transcrita de la página 4

| Criterio | Ponderación |
| --- | --- |
| Actualización coherente del Test Plan alineada al entorno ágil | 25% |
| Integración de estrategias de prueba TDD BDD automatización CI/CD | 20% |
| Evidencias de control y seguimiento revisiones auditorías métricas | 20% |
| Calidad del documento y presentación | 15% |
| Participación y trabajo colaborativo | 20% |

Estas ponderaciones no se convierten en una nota autoasignada. El equipo y el docente verifican los pendientes. Los roles Scrum de las tablas son ejemplos del documento; Kanban adapta coordinación, QA, desarrollo y validación al equipo de dos sin inventar Scrum Master ni sprints.

La portada, la matriz detallada, Word y la organización específica de GitHub son requisitos adicionales expresos del equipo y se incorporan a esta entrega.
