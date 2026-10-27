"""Genera métricas y anexos de esta entrega a partir de evidencias ejecutadas.

No modifica informes históricos. Ejecutar antes de las revisiones humanas;
regenera Casos_de_Prueba, Resultados_Pruebas y Kanban_Tareas.
"""
import csv
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]
docs = root / 'docs'
evidence = docs / 'evidencias'
php = ET.parse(evidence / 'phpunit-final.xml').getroot().find('testsuite')
assert php is not None
selenium = json.loads((evidence / 'selenium-resultados.json').read_text(encoding='utf-8'))
reports = [(p, ET.parse(p).getroot()) for p in evidence.glob('cypress-*.xml')]
final_path, cypress = max(reports, key=lambda item: item[0].stat().st_mtime)
assert int(php.attrib['tests']) == 64 and int(php.attrib['failures']) == 0 and int(php.attrib['errors']) == 0
assert int(cypress.attrib['tests']) == 3 and int(cypress.attrib['failures']) == 0
assert len(selenium['results']) == 2 and all(x['status'] == 'aprobado' for x in selenium['results'])
metrics = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'functional_cases_planned': 8, 'functional_cases_executed': 8,
    'functional_cases_passed': 8, 'functional_cases_failed': 0,
    'manual_charters_planned': 1, 'manual_charters_executed': 0,
    'total_planned': 9, 'total_executed': 8, 'total_passed': 8,
    'total_failed': 0, 'total_not_executed': 1,
    'execution_rate': 8 / 9 * 100, 'pass_rate_executed': 100,
    'functional_areas_covered': 3, 'functional_areas_in_scope': 3,
    'phpunit_tests': int(php.attrib['tests']), 'phpunit_assertions': int(php.attrib['assertions']),
    'phpunit_unit_tests': int(php.find("testsuite[@name='Unit']").attrib['tests']),
    'phpunit_feature_tests': int(php.find("testsuite[@name='Feature']").attrib['tests']),
    'selenium_checks': len(selenium['results']), 'cypress_scenarios': int(cypress.attrib['tests']),
    'automated_checks_total': int(php.attrib['tests']) + len(selenium['results']) + int(cypress.attrib['tests']),
    'automation_defects_found': 2, 'automation_defects_corrected': 2,
    'application_defects_confirmed_in_this_run': 0,
    'cypress_final_report': final_path.name,
}
(evidence / 'metricas.json').write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')

cases = [
    ('CP-01', 'Autenticación', 'HU-03 Acceder al inventario', 'Iniciar y cerrar sesión de forma verificable.',
     'Servidor SQA aislado; cuenta sqa@example.test disponible; sesión cerrada.',
     'Correo sqa@example.test y contraseña de fixture SqaDemo2026!.',
     'Abrir login, completar credenciales, enviar, comprobar dashboard, cerrar sesión e intentar abrir /products.',
     'Login redirige a dashboard; logout redirige a login y bloquea /products.',
     'Selenium comprobó ambas redirecciones y el encabezado del dashboard.',
     'Crítica', 'K-02', 'selenium-resultados.json; selenium/CP-01-dashboard.png; AuthenticationTest::test_login_and_logout'),
    ('CP-02', 'Autenticación', 'HU-03 Proteger rutas y rechazar credenciales incorrectas', 'Evitar acceso sin autenticación.',
     'Mismo entorno; cuenta existente; sesión cerrada.', 'GET /dashboard; correo SQA y contraseña incorrecta.',
     'Abrir /dashboard sin sesión; comprobar /login; enviar contraseña incorrecta y leer error.',
     'La ruta privada exige login y la contraseña incorrecta no autentica.',
     'Selenium observó /login y el mensaje de credenciales incorrectas; PHPUnit comprobó rutas privadas.',
     'Crítica', 'K-02', 'selenium-resultados.json; selenium/CP-02-acceso-rechazado.png; AuthenticationTest::test_internal_routes_require_authentication'),
    ('CP-03', 'Catálogo', 'HU-01 Registrar productos CA-01 a CA-05', 'Crear un producto con stock inicial trazable.',
     'Administrador autenticado; categoría Bebidas; SKU CY-ALTA inexistente.',
     'Nombre Producto CY-ALTA; SKU CY-ALTA; precio 8.50; stock 10; mínimo 3.',
     'Completar /products/create, enviar y filtrar /products?q=CY-ALTA; verificar fila. PHPUnit consulta producto y movimiento.',
     'Un producto con diez unidades, precio 8.50 y movimiento inicial de 0 a 10 del responsable.',
     'Cypress verificó la fila; PHPUnit verificó stock, precio, saldo inicial, saldo final y responsable.',
     'Crítica', 'K-03', 'cypress/inventario.cy.js/CP-03-producto-creado.png; phpunit-final.xml; ProductTest::test_valid_product_appears_in_listing_with_traceable_initial_stock'),
    ('CP-04', 'Catálogo', 'HU-01 SKU único CA-02', 'Rechazar duplicación tras normalizar mayúsculas.',
     'CP-03 creó CY-ALTA en la misma ejecución; administrador autenticado.',
     'Nuevo nombre, SKU cy-alta, categoría Bebidas y precio 8.50.',
     'Enviar segundo formulario y comprobar #sku-error; filtrar CY-ALTA y contar filas.',
     'Error de SKU; solo un producto con ese código.',
     'Cypress comprobó el error y una sola fila; PHPUnit comprobó un solo registro persistido.',
     'Alta', 'K-03', 'cypress/inventario.cy.js/CP-04-sku-duplicado.png; ProductTest::test_duplicate_sku_is_rejected_even_with_lowercase'),
    ('CP-05', 'Movimientos', 'HU-02 Entradas CA-01 y trazabilidad CA-05', 'Incrementar existencias y registrar historial.',
     'Producto CY-MOV con stock 10; mínimo 3; administrador autenticado.',
     'Entrada de 5; observación ENTRADA-CY-5.',
     'Seleccionar producto, enviar entrada y verificar fila del historial. PHPUnit comprueba base y responsable.',
     'Saldo 15, movimiento entrada 10 a 15 y responsable del registro.',
     'Cypress observó 15 en la fila; PHPUnit verificó tipo, cantidad, saldos y usuario.',
     'Crítica', 'K-04', 'cypress/inventario.cy.js/CP-05-entrada.png; InventoryTest::test_entry_increases_stock_and_records_history'),
    ('CP-06', 'Movimientos', 'HU-02 Evitar saldo negativo CA-03', 'Rechazar una salida superior al saldo sin efectos parciales.',
     'Producto CY-SALDO creado con stock 10 y un movimiento inicial.',
     'Salida de 11; observación INTENTO-RECHAZADO-CY.',
     'Enviar salida; comprobar error; consultar historial filtrado y catálogo filtrado.',
     'Stock insuficiente, saldo 10 e historial con una sola entrada inicial.',
     'Cypress verificó error, stock 10, historial de una fila y ausencia de la observación rechazada; PHPUnit verificó saldo y cantidad de movimientos.',
     'Crítica', 'K-04', 'cypress/inventario.cy.js/CP-06-stock-insuficiente.png; InventoryTest::test_insufficient_stock_preserves_balance_and_history'),
    ('CP-07', 'Movimientos y alertas', 'HU-02 Salidas CA-02 y alertas CA-06', 'Alertar cuando el saldo llega al mínimo exacto.',
     'Producto CY-MOV con saldo 15 tras CP-05 y mínimo 3.',
     'Salida de 12; observación SALIDA-CY-12.',
     'Enviar salida, verificar fila con saldos 15 y 3 y abrir /stock-bajo.',
     'Saldo 3, movimiento persistido y estado Stock bajo.',
     'Cypress verificó saldos e inclusión en alertas; PHPUnit y cuatro datos unitarios verificaron los límites del estado.',
     'Alta', 'K-04', 'cypress/inventario.cy.js/CP-07-alerta-minimo.png; InventoryTest::test_exit_decreases_stock_and_alert_appears_at_exact_minimum; ProductStockStatusTest'),
    ('CP-08', 'Movimientos', 'HU-02 Validar cantidades CA-04', 'Rechazar valores no enteros positivos en el servidor.',
     'Prueba PHPUnit con SQLite en memoria; producto con stock 10 y una entrada inicial.',
     'Cantidad 0, -1, 1.5, abc y null, mediante proveedor invalidMovements.',
     'Ejecutar InventoryTest::test_invalid_movement_is_rejected; enviar cada dato; verificar errores, stock e historial.',
     'Error de quantity, saldo 10 y un solo movimiento inicial para cada variante.',
     'Todas las variantes aprobaron en phpunit-final.xml; se comprobaron errores, stock e historial.',
     'Crítica', 'K-04', 'phpunit-final.xml; InventoryTest::test_invalid_movement_is_rejected'),
]
lines = ['# Casos de prueba de StockFácil', '',
         'Fecha 27 de octubre de 2026. Ocho casos funcionales críticos automatizados y una exploración manual pendiente. Cada caso agrupa comprobaciones relacionadas; no equivale a una prueba individual de PHPUnit. Los resultados corresponden a la ejecución final, conservando fallos intermedios de automatización.', '',
         '| ID | Funcionalidad | Estado técnico | Prioridad | Tarea |', '| --- | --- | --- | --- | --- |']
for case in cases:
    lines.append(f'| {case[0]} | {case[1]} | Aprobado | {case[9]} | {case[10]} |')
for case in cases:
    fields = ['Funcionalidad', 'Historia o requisito', 'Objetivo', 'Precondiciones', 'Datos de entrada', 'Pasos', 'Resultado esperado', 'Resultado obtenido']
    lines += ['', f'## {case[0]}', '']
    for label, value in zip(fields, case[1:9]):
        lines += [f'**{label}:** {value}', '']
    lines += [f'**Estado:** Aprobado automatizado. **Prioridad:** {case[9]}. **Tarea preparada:** {case[10]}.', '',
              f'**Evidencia:** docs/evidencias/{case[11]}.', '']
lines += ['## MAN-01 Exploración y aceptación humana', '',
          '**Objetivo:** comprobar comprensión, navegación y respuesta visual en escritorio y móvil. **Responsable propuesto:** Santiago, con revisión de Andre. **Prioridad:** alta. **Estado:** no ejecutado; requiere interacción y valoración humana real.', '',
          '**Precondiciones y datos:** usar instalación local o base de demostración desechable; nunca alterar inventario real para practicar. Cuenta de demo, producto nuevo con SKU MAN-01, stock 10 y mínimo 3.', '',
          '**Pasos:** 1. Abrir login en escritorio y tamaño móvil de 390 píxeles. 2. Navegar con Tab y verificar foco visible y etiquetas. 3. Acceder y abrir/cerrar menú móvil. 4. Crear producto, provocar un campo requerido y revisar mensajes. 5. Registrar entrada y salida y comprobar historial. 6. Cerrar sesión y verificar protección de rutas. 7. Registrar fecha real, navegador, observaciones y captura propia.', '',
          '**Esperado:** navegación usable, sin superposición, errores comprensibles y saldos coherentes. **Obtenido:** sin ejecución humana registrada. **Evidencia:** pendiente; no se reutiliza una captura automatizada como sesión manual. **Tarea:** K-11.', '',
          '## Reproducir la automatización', '',
          'Desde la raíz: `php vendor/phpunit/phpunit/phpunit --colors=never`, `npm run build`, `npm run test:selenium` y `npm run test:cypress`. El ejecutor de navegador crea SQLite nuevo, migra, carga fixtures, arranca PHP en puerto libre y lo detiene al acabar. El correo y contraseña anteriores son datos sintéticos de prueba, no credenciales de la cuenta GitHub.']
(docs / 'Casos_de_Prueba.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')

results = f'''# Resultados de pruebas de StockFácil

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
| Cypress | 3 | 3 | 3 | 0 | {final_path.name} y cypress-final.txt |
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

La exploración manual y aceptación del equipo están pendientes. La configuración de CI está preparada y se publica en GitHub; hasta verificar una ejecución remota no se declara aprobada. No hay Issues, Projects ni PR remoto acreditados en esta entrega automática; existen CSV, guías y descripción listos para su creación. Los commits bajo AndreRCRO no prueban participación de Santiago.

## Reproducción y preservación

`composer install`, `npm ci`, `npx cypress install`, `npm run build`, `php vendor/phpunit/phpunit/phpunit --colors=never`, `npm run test:selenium`, `npm run test:cypress`.

PHPUnit utiliza SQLite en memoria salvo la prueba de concurrencia, que crea su archivo temporal. El ejecutor Selenium/Cypress crea bases nuevas en tmp/sqa-e2e sin ejecutar migrate:fresh en la base habitual, conserva CSRF real con APP_ENV=sqa y detiene el servidor al finalizar. Las credenciales SQA son fixtures. Los hashes de integridad de .env y de la base habitual se comparan mediante integridad-antes.json e integridad-despues.json; consultar el cierre de auditoría para el resultado.
'''
(docs / 'Resultados_Pruebas.md').write_text(results, encoding='utf-8')

tasks = [
    ('K-01 Revisar consigna y alcance', 'Andre Romero Caballero', 'Crítica', 'En pruebas', 'Analizar PDF y documentación previa.', 'Ocho apartados y evidencias obligatorias trazados.', 'docs/Requisitos_Docente.md; docs/Test_Plan_SQA.md'),
    ('K-02 Verificar autenticación', 'Santiago Camacho Echalar', 'Crítica', 'En pruebas', 'CP-01 y CP-02: login, logout y rutas privadas.', 'Selenium y PHPUnit aprobados; revisión cruzada registrada.', 'docs/evidencias/selenium-resultados.json; AuthenticationTest'),
    ('K-03 Verificar catálogo', 'Andre Romero Caballero', 'Crítica', 'En pruebas', 'CP-03 y CP-04: alta con stock y unicidad de SKU.', 'Una alta trazable y duplicado rechazado sin nuevo producto.', 'ProductTest; cypress/e2e/inventario.cy.js'),
    ('K-04 Verificar movimientos y alertas', 'Santiago Camacho Echalar', 'Crítica', 'En pruebas', 'CP-05 a CP-08: entradas, salidas, rechazo y mínimo.', 'Sin saldo negativo ni historial parcial; cantidades inválidas rechazadas.', 'InventoryTest; ProductStockStatusTest; capturas Cypress'),
    ('K-05 Automatizar con dos herramientas', 'Santiago Camacho Echalar', 'Alta', 'En pruebas', 'Ejecutar Selenium y tres escenarios Cypress con SQLite aislado.', 'Reportes y capturas reales aprobados con comandos reproducibles.', 'scripts/run-browser-tests.mjs; docs/Resultados_Pruebas.md'),
    ('K-06 Corregir AUT-01 y AUT-02', 'Santiago Camacho Echalar', 'Alta', 'En pruebas', 'Acotar formulario y filtrar catálogo paginado en Cypress.', 'Conservar rondas inicial intermedia final y regresión de tres escenarios aprobada.', 'docs/evidencias/cypress-inicial.txt; cypress-intermedia.txt; cypress-final.txt'),
    ('K-07 Completar Test Plan Word y Markdown', 'Andre Romero Caballero', 'Crítica', 'En pruebas', 'Preparar ocho apartados y anexos de la entrega.', 'Portada real, resultados verificables y Word revisado visualmente.', 'docs/Test_Plan_SQA.md; docs/Test_Plan_SQA.docx'),
    ('K-08 Auditar y calcular métricas', 'Andre Romero Caballero', 'Alta', 'En pruebas', 'Revisar trazabilidad y preservar datos; distinguir pruebas manuales pendientes.', 'Métricas coinciden con XML y JSON; auditoría registra límites y seguimiento.', 'docs/Auditoria_Interna_SQA.md; docs/evidencias/metricas.json'),
    ('K-09 Verificar integración continua', 'Santiago Camacho Echalar', 'Alta', 'En pruebas', 'Publicar workflow y comprobar una ejecución remota.', 'GitHub Actions termina y conserva artifact; registrar URL real.', '.github/workflows/pruebas.yml; docs/GitHub_Entrega.md'),
    ('K-10 Publicar tablero y revisar PR', 'Ambos integrantes', 'Crítica', 'Pendiente', 'Crear Issues y Projects; revisión cruzada real desde ambas cuentas.', 'Cinco estados, WIP 2, enlaces y revisión sin suplantación de autoría.', 'docs/Kanban_Guia.md; docs/Pull_Request_SQA.md'),
    ('K-11 Ejecutar exploración y aceptación', 'Santiago Camacho Echalar con revisión de Andre', 'Alta', 'Pendiente', 'MAN-01: escritorio, móvil, teclado y recorrido de negocio.', 'Fecha, navegador, resultado y evidencia humana registrados.', 'docs/Casos_de_Prueba.md MAN-01'),
]
with (docs / 'Kanban_Tareas.csv').open('w', encoding='utf-8-sig', newline='') as stream:
    writer = csv.writer(stream)
    writer.writerow(['Titulo', 'Responsable', 'Prioridad', 'Estado', 'Descripcion', 'Criterios', 'Evidencias'])
    writer.writerows(tasks)
print(json.dumps(metrics, ensure_ascii=False, indent=2))
