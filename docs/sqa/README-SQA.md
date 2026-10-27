# Actividad: Aplicando SQA en nuestras historias de usuario

Proyecto StockFácil. Elaboración: 13 de octubre de 2026. Este paquete contiene fuentes Markdown completas y evidencia ejecutada; sus revisiones, inspecciones y auditorías son técnicas preliminares, pendientes de validación por los equipos y el docente.

## Entrega al docente

Entrega los dos informes por historia y el consolidado, acompañados del paquete docs/sqa con matrices, checklists, actas, logs JUnit y capturas. Las versiones PDF se generan en output/pdf desde las fuentes Markdown. El archivo ZIP de entrega reúne la documentación y esas versiones, sin incluir la base de desarrollo, .env ni credenciales privadas.

- [01-preparacion/historias-usuario.md](01-preparacion/historias-usuario.md)
- [01-preparacion/criterios-aceptacion.md](01-preparacion/criterios-aceptacion.md)
- [01-preparacion/matriz-trazabilidad.md](01-preparacion/matriz-trazabilidad.md)
- [02-revision/checklist-hu01.md](02-revision/checklist-hu01.md)
- [02-revision/checklist-hu02.md](02-revision/checklist-hu02.md)
- [02-revision/hallazgos-revision.md](02-revision/hallazgos-revision.md)
- [03-inspeccion/checklist-inspeccion-hu01.md](03-inspeccion/checklist-inspeccion-hu01.md)
- [03-inspeccion/checklist-inspeccion-hu02.md](03-inspeccion/checklist-inspeccion-hu02.md)
- [03-inspeccion/acta-inspeccion-hu01.md](03-inspeccion/acta-inspeccion-hu01.md)
- [03-inspeccion/acta-inspeccion-hu02.md](03-inspeccion/acta-inspeccion-hu02.md)
- [03-inspeccion/registro-acciones-correctivas.md](03-inspeccion/registro-acciones-correctivas.md)
- [04-pruebas/casos-prueba.md](04-pruebas/casos-prueba.md)
- [04-pruebas/resultados-pruebas.md](04-pruebas/resultados-pruebas.md)
- [05-auditoria/preauditoria-hu01.md](05-auditoria/preauditoria-hu01.md)
- [05-auditoria/preauditoria-hu02.md](05-auditoria/preauditoria-hu02.md)
- [05-auditoria/cumplimiento-global.md](05-auditoria/cumplimiento-global.md)
- [05-auditoria/validacion-independiente-pendiente.md](05-auditoria/validacion-independiente-pendiente.md)
- [06-informes-finales/informe-sqa-hu01.md](06-informes-finales/informe-sqa-hu01.md)
- [06-informes-finales/informe-sqa-hu02.md](06-informes-finales/informe-sqa-hu02.md)
- [06-informes-finales/informe-sqa-general.md](06-informes-finales/informe-sqa-general.md)

## Versiones finales

- [PDF de HU-01](../../output/pdf/informe-sqa-hu01.pdf).
- [PDF de HU-02](../../output/pdf/informe-sqa-hu02.pdf).
- [PDF consolidado](../../output/pdf/informe-sqa-general.pdf).
- [Paquete de entrega: documentos, PDF, evidencia y fuentes del proyecto](../../output/stockfacil-sqa-entrega.zip).

## Resultados técnicos

- HU-01: seis CA verificados de seis aplicables, 100% técnico.
- HU-02: seis CA verificados de seis aplicables, 100% técnico.
- Global del alcance: doce de doce, 100% ponderado por CA aplicables.
- Suite final: 43 pruebas aprobadas y 286 aserciones.
- Navegador: 14 casos de actividad aprobados; dos reejecutados después de HR-04 y una comprobación adicional de límite superior.
- Inventario de desarrollo preservado, con huella lógica idéntica.

El porcentaje no es una aprobación oficial ni cubre estándares del curso no aportados. HR-04 se conserva como hallazgo corregido, no desaparece del informe.

## Completar personalmente

Completa universidad, asignatura, docente e integrantes. Gestiona revisión por otro equipo, sesión formal de inspección y auditoría independiente. Los participantes deben llenar fechas reales, roles, observaciones, responsables y firmas. No firmes por otras personas ni conviertas la fecha de elaboración en una fecha de reunión no realizada.

## Reproducción y evidencia

phpunit.xml usa SQLite en memoria. Consulta 04-pruebas/resultados-pruebas.md para comandos. Los scripts de navegador requieren Playwright disponible y una instancia temporal; no deben apuntar a la base de desarrollo. generar-documentos.py regenera fuentes a partir de evidencia existente y exige la versión concreta de resultados documentada.

Los JSON conservan tiempos UTC; los informes usan la fecha local America/La_Paz. Capturas de implementación anteriores en .impeccable/review no se presentan como resultados nuevos: se generaron capturas frescas en esta actividad.

Después de completar datos académicos y validaciones humanas en los Markdown, exporta esos cambios mediante exportar-pdf.py o tu editor. No vuelvas a ejecutar generar-documentos.py sobre una versión validada: reconstruye los documentos preliminares y sobrescribe sus campos. El exportador PDF se ejecutó con ReportLab, pypdf y las fuentes Segoe UI del entorno Windows; los PDF ya generados no necesitan esas herramientas para abrirse.

## Calidad documental

Se separan criterio original, regla adicional, resultado técnico y aprobación externa. Los métodos y líneas se verificaron contra archivos reales. La ambigüedad de IDs se resuelve con SQA/CP, sin cambiar la numeración anterior. No existen mockups previos acreditados; las imágenes son capturas reales posteriores a la implementación.
