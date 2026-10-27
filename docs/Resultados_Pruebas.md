# Resultados de pruebas de StockFácil

Fecha 27 de octubre de 2026, zona America/La_Paz. Evidencia calculable en `docs/evidencias/metricas.json`. Los XML y JSON tienen marcas reales de ejecución; no se mezclan con informes históricos de octubre.

## Casos del plan

| Indicador | Resultado | Cálculo o fuente |
| --- | --- | --- |
| Casos críticos automatizados planificados | 8 | CP-01 a CP-08 |
| Exploraciones manuales planificadas | 1 | MAN-01 |
| Total planificado | 9 | 8 + 1 |
| Total ejecutado | 8 | Casos CP con evidencias finales |
| Total aprobado | 8 | Criterios técnicos, sin aceptación humana implícita |
| Total fallido final | 0 | Reejecución final |
| Total no ejecutado | 1 | MAN-01 requiere evaluación humana |
| Ejecución del plan | 88,89% | 8 / 9 × 100 |
| Aprobación sobre ejecutados | 100% | 8 / 8 × 100 |
| Áreas funcionales con pruebas | 3 de 3, 100% | Acceso, catálogo y movimientos con alertas |
| Defectos nuevos confirmados de aplicación | 0 | No se identificó un defecto nuevo de producto |
| Defectos de automatización detectados y corregidos | 2 de 2 | AUT-01 y AUT-02 |

La cobertura anterior mide áreas del alcance con al menos un caso, no líneas ni ramas de código. No hay reporte de cobertura instrumental ni denominador de tamaño para defect density; no se calcula densidad. Velocidad y throughput del equipo no son calculables sin varios períodos y cierres humanos; asignar responsables no mide participación.

## Comprobaciones automatizadas

| Herramienta | Planificadas finales | Ejecutadas | Aprobadas | Fallidas | Evidencia |
| --- | --- | --- | --- | --- | --- |
| PHPUnit | 64 | 64 | 64 | 0 | phpunit-final.xml y phpunit-final.txt |
| Selenium WebDriver | 2 | 2 | 2 | 0 | selenium-resultados.json y selenium-salida.txt |
| Cypress | 3 | 3 | 3 | 0 | cypress-41748e572140623033750e5223d8e2a0.xml y cypress-final.txt |
| Total de comprobaciones | 69 | 69 | 69 | 0 | No sumar a los nueve casos del plan |

PHPUnit ejecutó 7 pruebas unitarias y 57 pruebas de funcionalidad e integración, con 423 aserciones en conjunto. Los cuatro datos nuevos de ProductStockStatusTest comprueban agotamiento, mínimo inferior, mínimo exacto y disponibilidad. La línea base real fue 60 pruebas y 419 aserciones en phpunit-inicial.xml; no se atribuye al sistema previo un fallo que no ocurrió.

## Fallos y correcciones observados

| Ronda | Resultado Cypress | Hallazgo y acción |
| --- | --- | --- |
| Inicial | 0 aprobados, 3 fallidos | AUT-01: selector global encontraba guardar y logout; se limitó a form data-submit-form. Evidencia cypress-inicial.txt y capturas cypress-inicial. |
| Intermedia | 2 aprobados, 1 fallido | AUT-02: el producto nuevo quedaba fuera de la primera página; la prueba debe filtrar por SKU. Evidencia cypress-intermedia.txt y capturas cypress-intermedia. |
| Final | 3 aprobados, 0 fallidos | Se aplicaron ambas correcciones y se creó una base nueva antes de repetir. |

Son defectos del código de prueba, no fallos de la lógica del inventario. Se conserva el historial real, sin simular TDD. PHPUnit inicial bajo aislamiento no llegó a cargar bootstrap; su reejecución autorizada sí ejecutó 60 pruebas. Ese bloqueo de entorno no cuenta como fallo funcional.

## Otras verificaciones

Vite compiló correctamente (`build.txt`) y Composer validó el manifiesto y lock (`composer-validacion.txt`). Selenium empleó Edge en Windows; Cypress 16.2.0 empleó Electron 146 sin interfaz. El workflow utiliza Chrome para Selenium en Linux y Electron para Cypress. Electron emite aviso de deprecación; la versión bloqueada funciona en esta ejecución, y puede elegirse otro navegador con SQA_CYPRESS_BROWSER.

La exploración manual y aceptación del equipo están pendientes. GitHub Actions aprobó la ejecución 40573040837 del commit cf285bf: https://github.com/AndreRCRO/StockFacil/actions/runs/40573040837. Los pasos PHPUnit, Selenium con Chrome y Cypress y la subida del artifact evidencias-sqa-1 se verificaron mediante la API pública. Se conservan github-actions.json, github-actions-jobs.json y github-actions-artifacts.json. No hay Issues, Projects ni PR remoto acreditados en esta entrega automática; existen CSV, guías y descripción listos para su creación. Los commits bajo AndreRCRO no prueban participación de Santiago.

## Reproducción y preservación

`composer install`, `npm ci`, `npx cypress install`, `npm run build`, `php vendor/phpunit/phpunit/phpunit --colors=never`, `npm run test:selenium`, `npm run test:cypress`.

PHPUnit utiliza SQLite en memoria salvo la prueba de concurrencia, que crea su archivo temporal. El ejecutor Selenium/Cypress crea bases nuevas en tmp/sqa-e2e sin ejecutar migrate:fresh en la base habitual, conserva CSRF real con APP_ENV=sqa y detiene el servidor al finalizar. Las credenciales SQA son fixtures. Los hashes de integridad de .env y de la base habitual se comparan mediante integridad-antes.json e integridad-despues.json; consultar el cierre de auditoría para el resultado.
