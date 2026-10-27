# Registro de acciones correctivas

| Acción | Hallazgo | Archivo/artefacto | Resultado anterior | Corrección y resultado posterior | Responsable técnico / humano | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| AC-01 | HR-01 | Documentación docs/sqa | Identificadores CP ambiguos entre catálogos. | SQA/CP-01 a CP-14 y métodos PHPUnit explícitos; catálogo previo conservado. | Codex / ratificación del equipo [Completar] | Corregido |
| AC-02 | HR-04 | app/Http/Requests/MovementRequest.php; tests/Feature/InventoryTest.php | Suite previa: 42/42, 276 aserciones, sin comprobar concordancia. Regresión válida ampliada: 3 fallidas, 5 aprobadas por mensajes min/max. | Mensajes La cantidad para min/max. Suite posterior: 43/43, 286 aserciones. CP-11, CP-12 y REG-MAX aprobados en navegador; stock 3 e historial 3. | Codex / ratificación del equipo [Completar] | Corregido y verificado |
| AC-03 | HR-02 | Checklists y actas | Revisión/inspección formales sin acreditación. | Formatos completos preparados; sesión y observaciones oficiales pendientes. | Equipo revisor/pares [Completar] | Pendiente |
| AC-04 | HR-03 | Matrices e informes de auditoría | Rúbrica/plan y auditoría formal no aportados. | Preevaluación 12/12 CA; estándares y aprobación independientes pendientes. | Docente o auditor [Completar] | Pendiente |

La intervención en producción se limita a mensajes de validación. No se modificaron arquitectura, cálculos de stock, rutas ni funcionalidades. Las huellas de integridad muestran solo MovementRequest.php e InventoryTest.php modificados entre los archivos originales inspeccionados. El inventario de desarrollo conserva su huella lógica. Fecha y firma de cierre humano de cada acción: [Completar].

Evidencias: regresion-antes.txt/xml, phpunit-antes.txt/xml, phpunit-salida.txt, phpunit-junit.xml, revalidacion-correccion.json, capturas antes/después e integridad-final.json. El error de preparación del test se archiva por separado, sin atribuirlo al producto.
