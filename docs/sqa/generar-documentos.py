"""Regenera el paquete Markdown a partir de evidencias locales ya ejecutadas.

No ejecuta migraciones ni modifica la aplicación. Requiere Python estándar.
"""
from pathlib import Path
import json
import os
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
SQA = ROOT / 'docs/sqa'
EV = SQA / '04-pruebas/evidencias'
DATE = '13 de octubre de 2026'
browser = json.loads((EV / 'resultados-navegador.json').read_text(encoding='utf-8'))
observed = {case['id']: case for case in browser['cases']}
junit = ET.parse(EV / 'phpunit-junit.xml').getroot()
suite = junit.find('testsuite')
summary = {key: int(suite.get(key, '0')) for key in ['tests', 'assertions', 'errors', 'failures', 'skipped']}
assert summary == {'tests': 43, 'assertions': 286, 'errors': 0, 'failures': 0, 'skipped': 0}, summary
tests = list(junit.iter('testcase'))
integrity = json.loads((EV / 'integridad-final.json').read_text(encoding='utf-8'))
assert integrity['development_database_unchanged']

def test_ok(fragment):
    matches = [test for test in tests if fragment in test.get('name', '')]
    assert matches, fragment
    return all(not list(test) for test in matches)

def table(headers, rows):
    clean = lambda value: str(value).replace('|', '/').replace('\n', ' ')
    lines = ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |']
    lines += ['| ' + ' | '.join(clean(value) for value in row) + ' |' for row in rows]
    return '\n'.join(lines) + '\n'

def write(relative, content):
    target = SQA / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.strip() + '\n', encoding='utf-8')

def link(relative, target, label):
    url = os.path.relpath(ROOT / target, (SQA / relative).parent).replace('\\', '/')
    return f'[{label}]({url})'

def evidence(relative, name, label=None):
    return link(relative, f'docs/sqa/04-pruebas/evidencias/{name}', label or name)

def doc(relative, other, label):
    return link(relative, 'docs/sqa/' + other, label)

refs = {
    'P1': ('app/Http/Requests/ProductRequest.php', 'ProductRequest::rules', 'public function rules'),
    'P2': ('app/Http/Controllers/ProductController.php', 'ProductController::store', 'public function store'),
    'P3': ('app/Http/Controllers/ProductController.php', 'ProductController::index', 'public function index'),
    'P4': ('app/Services/InventoryService.php', 'InventoryService::createProduct', 'public function createProduct'),
    'P5': ('resources/views/products/form.blade.php', 'Formulario Blade de creación y edición', '<form action='),
    'P6': ('resources/views/products/index.blade.php', 'Listado Blade paginado', '<table>'),
    'P7': ('database/migrations/2026_10_13_000001_create_inventory_tables.php', 'Migración: productos y restricciones SQLite', "Schema::create('products'"),
    'P8': ('app/Models/Product.php', 'Product::category / movements / casts', 'protected function casts'),
    'M1': ('app/Http/Requests/MovementRequest.php', 'MovementRequest::rules', 'public function rules'),
    'M2': ('app/Services/InventoryService.php', 'InventoryService::record', 'public function record'),
    'M3': ('app/Http/Controllers/MovementController.php', 'MovementController::store', 'public function store'),
    'M4': ('app/Http/Controllers/MovementController.php', 'MovementController::index', 'public function index'),
    'M5': ('app/Models/Movement.php', 'Movement: atributos, casts y relaciones', 'protected $fillable'),
    'M6': ('resources/views/movements/form.blade.php', 'Formulario Blade de movimientos', 'data-movement-form'),
    'M7': ('resources/views/movements/index.blade.php', 'Historial Blade', '<table'),
    'M8': ('app/Models/Product.php', 'Product::scopeLowStock / getStockStatusAttribute', 'public function scopeLowStock'),
    'M9': ('resources/views/products/low-stock.blade.php', 'Listado Blade de alertas', '<table'),
    'M10': ('app/Http/Requests/MovementRequest.php', 'MovementRequest::messages, corrección HR-04', 'public function messages'),
    'C1': ('resources/views/components/field.blade.php', 'Componente: etiqueta, ayuda y error del campo', '@error($name)'),
    'C2': ('resources/views/components/flash.blade.php', 'Componente: resumen de errores y confirmación', '@if($errors->any())'),
    'C3': ('lang/es/validation.php', 'Mensajes de validación en español', "'required'"),
    'C4': ('bootstrap/app.php', 'Respuesta de validación: recuperación segura de campos escalares', '$exceptions->render'),
    'A1': ('routes/web.php', 'Grupo de rutas protegido por auth', "Route::middleware('auth')"),
    'B1': ('config/database.php', 'Conexión SQLite, WAL y espera de escritura', "'sqlite' =>"),
    'T1': ('tests/Feature/ProductTest.php', 'ProductTest: registro válido, invalidaciones y listado', 'public function test_valid_product'),
    'T2': ('tests/Feature/InventoryTest.php', 'InventoryTest: entradas, salidas, alertas y rollback', 'public function test_entry'),
    'T3': ('tests/Feature/ConcurrencyTest.php', 'ConcurrencyTest: dos procesos sobre SQLite temporal', 'public function test_simultaneous'),
    'T4': ('tests/Feature/AuthenticationTest.php', 'AuthenticationTest: rutas internas protegidas', 'public function test_internal'),
    'T5': ('phpunit.xml', 'SQLite de pruebas en memoria', 'name="DB_DATABASE"'),
}
for key, (file, method, needle) in list(refs.items()):
    lines = (ROOT / file).read_text(encoding='utf-8').splitlines()
    line = next((number for number, text in enumerate(lines, 1) if needle in text), None)
    assert line is not None, (key, file, needle)
    refs[key] = {'file': file, 'method': method, 'line': line}
(EV / 'referencias-codigo.json').write_text(json.dumps(refs, ensure_ascii=False, indent=2), encoding='utf-8')

stories = {
    'HU-01': {
        'title': 'Registro de productos',
        'description': 'Como administrador de una tienda, quiero registrar nuevos productos con su información correspondiente para mantener actualizado el inventario de mi negocio.',
        'objective': 'Comprobar que el registro valida los datos, persiste un producto en SQLite y permite localizarlo en el inventario, conservando trazabilidad del stock inicial.',
        'criteria': ['El sistema debe exigir el nombre del producto.', 'El SKU o código del producto debe ser único.', 'El precio no puede ser negativo.', 'La cantidad inicial no puede ser negativa.', 'Cuando se registre correctamente un producto, este debe aparecer en el inventario.', 'Cuando se ingresen datos inválidos, el sistema debe mostrar mensajes de validación.'],
        'refs': ['P1','P2','P3','P4','P5','P6','P7','P8','C1','C2','C3','C4','A1','B1','T1','T4','T5'],
        'cases': ['CP-01','CP-02','CP-03','CP-04','CP-05','CP-06','CP-07'],
        'ca_cases': [['CP-02'],['CP-03'],['CP-04'],['CP-05'],['CP-01','CP-06'],['CP-02','CP-07']],
        'ca_refs': [['P1','P5'],['P1','P7'],['P1','P7'],['P1','P4'],['P2','P3','P6'],['C1','C2','C3','C4']],
        'ca_tests': [['test_invalid_product_is_rejected with data set #0'],['test_duplicate_sku_is_rejected_even_with_lowercase'],['test_invalid_product_is_rejected with data set #3'],['test_invalid_product_is_rejected with data set #6'],['test_valid_product_appears_in_listing_with_traceable_initial_stock'],['test_invalid_product_is_rejected']],
    },
    'HU-02': {
        'title': 'Control de entradas y salidas de inventario',
        'description': 'Como administrador de una tienda, quiero registrar las entradas y salidas de productos para controlar las cantidades disponibles en mi inventario.',
        'objective': 'Comprobar la aritmética de entradas y salidas, el rechazo de cantidades inválidas o insuficientes, la persistencia del historial y las alertas al llegar al mínimo.',
        'criteria': ['Las entradas deben incrementar correctamente las existencias.', 'Las salidas deben disminuir correctamente las existencias.', 'No se debe permitir retirar más productos de los disponibles.', 'No se deben permitir movimientos con cantidades iguales o menores a cero.', 'Cada entrada y salida debe quedar registrada en el historial.', 'El sistema debe mostrar alertas cuando un producto alcance su stock mínimo.'],
        'refs': ['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10','P7','P8','C1','C2','A1','B1','T2','T3','T4','T5'],
        'cases': ['CP-08','CP-09','CP-10','CP-11','CP-12','CP-13','CP-14'],
        'ca_cases': [['CP-08'],['CP-09'],['CP-10'],['CP-11','CP-12'],['CP-08','CP-09','CP-13'],['CP-14']],
        'ca_refs': [['M2','M3'],['M2','M3'],['M2'],['M1','M2','M10'],['M2','M4','M5','M7'],['M8','M9']],
        'ca_tests': [['test_entry_increases_stock_and_records_history'],['test_exit_decreases_stock_and_alert_appears_at_exact_minimum'],['test_insufficient_stock_preserves_balance_and_history'],['test_invalid_movement_is_rejected with data set #0','test_invalid_movement_is_rejected with data set #1'],['test_entry_increases_stock_and_records_history','test_exit_decreases_stock_and_alert_appears_at_exact_minimum'],['test_exit_decreases_stock_and_alert_appears_at_exact_minimum']],
    },
}
cases = {
    'CP-01': ('Registrar producto válido', 'Sesión de administrador, categoría Bebidas y SKU SQA-001 libre.', 'Nombre Producto SQA - HU01; SKU SQA-001; precio 8,50; inicial 10; mínimo 3.', 'Abrir Nuevo producto; completar campos; pulsar Registrar producto.', 'Confirmación, persistencia del producto y entrada inicial 0 a 10.'),
    'CP-02': ('Rechazar producto sin nombre', 'Sesión iniciada y formulario disponible.', 'Nombre vacío; SKU SQA-INVALID; precio 8,50; inicial 10; mínimo 3.', 'Enviar el formulario con nombre vacío, omitiendo solo la validación nativa del navegador.', 'Mensaje de nombre obligatorio; sin nuevo producto.'),
    'CP-03': ('Rechazar SKU duplicado', 'CP-01 creó SQA-001.', 'SKU SQA-001; otros campos válidos.', 'Abrir Nuevo producto e intentar guardar el SKU existente.', 'Mensaje de SKU duplicado; sin duplicación en SQLite.'),
    'CP-04': ('Rechazar precio negativo', 'Sesión iniciada, categoría válida.', 'Precio -1; SKU SQA-INVALID; otros campos válidos.', 'Enviar el formulario omitiendo validación HTML5 para ejercitar el servidor.', 'Mensaje de precio no negativo; producto no persistido.'),
    'CP-05': ('Rechazar stock inicial negativo', 'Sesión iniciada, categoría válida.', 'Stock inicial -1; SKU SQA-INVALID; otros campos válidos.', 'Enviar el formulario omitiendo validación HTML5 para ejercitar el servidor.', 'Mensaje de stock inicial no negativo; sin producto ni movimiento.'),
    'CP-06': ('Localizar producto guardado', 'CP-01 aprobado; errores previos no añadieron productos.', 'Filtro de búsqueda SQA-001.', 'Abrir Productos, buscar el SKU y comprobar la fila.', 'Una fila con nombre, SKU, precio y stock 10.'),
    'CP-07': ('Visualizar errores de validación', 'Sesión iniciada y formulario disponible.', 'Nombre vacío; SKU SQA-ERROR; otros campos válidos.', 'Enviar, comprobar resumen de errores, mensaje junto al nombre, aria-invalid y conservación del SKU.', 'Errores visibles y entrada válida recuperada.'),
    'CP-08': ('Registrar entrada válida', 'Producto SQA-001 activo con stock 10.', 'Entrada 5; observación Entrada SQA CP-08.', 'Abrir movimiento del producto; verificar preview 15; guardar.', 'Stock 15 y movimiento de 10 a 15.'),
    'CP-09': ('Registrar salida válida', 'CP-08 aprobado; stock 15.', 'Salida 12; observación Salida SQA CP-09.', 'Verificar preview 3 y guardar salida.', 'Stock 3 y movimiento de 15 a 3.'),
    'CP-10': ('Rechazar salida superior al saldo', 'CP-09 aprobado; stock 3.', 'Salida 4.', 'Enviar y comprobar mensaje; volver a consultar el saldo.', 'Stock insuficiente; saldo 3 e historial sin cambios.'),
    'CP-11': ('Rechazar cantidad cero', 'Producto activo con stock 3.', 'Salida 0.', 'Enviar sin validación HTML5; leer error y saldo. Repetir después de HR-04.', 'Rechazo por cantidad mínima; saldo 3.'),
    'CP-12': ('Rechazar cantidad negativa', 'Producto activo con stock 3.', 'Salida -1.', 'Enviar sin validación HTML5; leer error y saldo. Repetir después de HR-04.', 'Rechazo por cantidad mínima; saldo 3.'),
    'CP-13': ('Comprobar historial persistido', 'CP-01, CP-08 y CP-09 aprobados; intentos inválidos rechazados.', 'Filtro por ID del producto SQA-001.', 'Abrir historial filtrado; contar filas y comprobar tipos, saldos, responsable, fechas y notas; contrastar SQLite.', 'Tres eventos consecutivos 0 a 10, 10 a 15 y 15 a 3.'),
    'CP-14': ('Comprobar alerta en mínimo exacto', 'SQA-001 activo, stock 3 y mínimo 3.', 'Filtro de alertas SQA-001.', 'Abrir Stock bajo, buscar producto y leer estado/stock/mínimo.', 'Estado Stock bajo al cumplirse stock igual al mínimo.'),
}

compliance = {}
for hu, story in stories.items():
    verified = [all(observed[cp]['status'] == 'aprobado' for cp in ids) and all(test_ok(test) for test in fragments) for ids, fragments in zip(story['ca_cases'], story['ca_tests'])]
    compliance[hu] = {'applicable':6,'compliant':sum(verified),'unverified':0,'not_applicable':0,'results':verified,'percent':sum(verified)/6*100}
global_compliant = sum(row['compliant'] for row in compliance.values())
global_applicable = sum(row['applicable'] for row in compliance.values())
(EV/'cumplimiento-calculado.json').write_text(json.dumps({'scope':'Doce CA de HU-01 y HU-02; preevaluación técnica, no aprobación oficial','stories':compliance,'global':{'compliant':global_compliant,'applicable':global_applicable,'percent':100*global_compliant/global_applicable,'unverified':0},'suite':summary},ensure_ascii=False,indent=2),encoding='utf-8')

def artifact_table(relative, hu):
    rows=[]
    for key in stories[hu]['refs']:
        item=refs[key]
        rows.append((key, f"`{item['file']}:{item['line']}`", item['method']))
    return table(['Ref.','Archivo y línea verificados','Clase, método o artefacto'],rows)

def ca_table(relative, hu, detailed=True):
    rows=[]
    for index, description in enumerate(stories[hu]['criteria']):
        cp=stories[hu]['ca_cases'][index]
        proof=', '.join(stories[hu]['ca_refs'][index])+'; '+', '.join('SQA/'+value for value in cp)
        result='Cumple' if compliance[hu]['results'][index] else 'No verificado'
        if detailed: rows.append((f'CA-{index+1:02}',description,proof,result,'Comprobado en código, PHPUnit y navegador.','Validar independientemente las evidencias.'))
        else: rows.append((f'CA-{index+1:02}',description,result,proof))
    return table(['CA','Descripción original','Evidencia objetiva','Resultado','Observación','Recomendación'] if detailed else ['CA','Criterio original','Resultado','Evidencia'],rows)

review_aspects=['Descripción clara','Actor identificado','Objetivo comprensible','Criterios definidos','Criterios verificables','Ausencia de contradicciones en el alcance seleccionado','Diseño acorde con la funcionalidad','Campos necesarios en formularios','Validaciones contempladas','Mensajes de error contemplados','Flujo de uso coherente','Artefactos identificables']
review_notes={
    'HU-01': [('Registro para actualizar inventario, con actor y finalidad explícitos.','Ficha y consigna'),('Administrador de tienda; las rutas exigen sesión.','A1, T4'),('Conservar un catálogo válido y localizar el producto creado.','Ficha HU-01'),('Seis CA originales conservados sin reformulación.','Criterios CA-01 a CA-06'),('Cada CA se vincula con entrada, rechazo o presencia de una fila.','SQA/CP-01 a CP-07, T1'),('Inicial cero es válido; no produce movimiento cero. No contradice el rechazo de movimientos cero.','P1, P4, T1'),('Formulario, confirmación y búsqueda corresponden al registro real.','P5, P6, capturas HU-01'),('Nombre, SKU, categoría, descripción, precio, inicial y mínimo presentes.','P5; hu01-formulario.png'),('required, unique, numeric, integer y mínimos en el servidor.','P1; pruebas negativas'),('Resumen y errores por campo, en español; valores válidos conservados.','C1 a C4; CP-07'),('Formulario POST, transacción, redirección y listado paginado/buscable.','P2 a P6; CP-01/06'),('Modelos, migración, rutas, vistas, pruebas y documentación reales.','Inventario de artefactos P1 a T5')],
    'HU-02': [('Registro de entradas y salidas para controlar cantidades.','Ficha y consigna'),('Administrador autenticado; responsable extraído de la sesión.','A1, M3, T4'),('Conocer el saldo y conservar cambios verificables.','Ficha HU-02'),('Seis CA originales conservados; reglas adicionales separadas.','Criterios CA-01 a CA-06'),('Saldos antes/después, rechazos, historial y mínimo exacto observables.','SQA/CP-08 a CP-14, T2'),('Cantidad positiva para movimientos; alerta con <= incluye el mínimo exigido.','M1, M2, M8'),('Tipos Entrada/Salida y preview respaldados por validación del servidor.','M6, M2; capturas HU-02'),('Producto, tipo, cantidad y observación; responsable/fecha automáticos.','M6, M3, M5'),('Producto activo, cantidad entera positiva, tipo y saldo suficiente.','M1, M2, T2'),('Errores de insuficiencia y cantidad presentes; concordancia corregida en HR-04.','CP-10/11/12, M10'),('Selección, preview, guardado atómico, historial y alerta.','M2 a M9; navegador'),('Servicio, controladores, modelos, migración, pruebas y docs identificados.','Inventario de artefactos M1 a T5')],
}

def review_table(hu, full=True):
    rows=[]
    for number,(aspect,(note,proof)) in enumerate(zip(review_aspects,review_notes[hu]),1):
        action='Mantener evidencia y validar por otro equipo.'
        if number==12: action='Usar namespace SQA/CP para evitar HR-01.'
        if hu=='HU-02' and number==10: action='HR-04 corregido y reejecutado; conservar antes/después.'
        rows.append((number,aspect,'Cumple',note,action,proof) if full else (number,aspect,'Cumple',note+' Evidencia: '+proof))
    return table(['N.º','Aspecto evaluado','Resultado preliminar','Observación','Acción de mejora','Evidencia'] if full else ['N.º','Aspecto','Resultado','Observación y evidencia'],rows)

inspection={
    'HU-01': [('Nombre obligatorio','P1 / ProductRequest::rules','Validación en servidor','CP-02 rechaza nombre vacío; error visible.','SQA/CP-02, T1'),('SKU único','P1, P7 / rules y migración','Integridad y normalización','Unique en petición e índice SQLite; minúsculas se normalizan.','SQA/CP-03, T1'),('Precio','P1 / rules','Dominio numérico no negativo','numeric, min:0 y hasta dos decimales.','SQA/CP-04, T1'),('Stock inicial','P1, P4 / rules y createProduct','Entero no negativo','Rechazo de negativo/fraccionario; cero permitido.','SQA/CP-05, T1'),('Persistencia SQLite','P2, P4, P7, B1','Persistencia real','Eloquent escribe producto; base temporal muestra SQA-001.','sqlite-navegador.json, CP-01'),('Movimiento inicial','P4 / createProduct','Trazabilidad y atomicidad','Entrada 0 a 10; con cero no hay movimiento; fallo revierte producto.','T1; sqlite-navegador.json'),('Producto en listado','P3, P6 / index','Visibilidad y búsqueda','Fila filtrada por SKU muestra datos y stock 10.','SQA/CP-06'),('Mensajes de error','C1 a C4, P5','Claridad y recuperación','Resumen, mensaje por campo, aria-invalid y SKU recuperado.','SQA/CP-07'),('Autenticación','A1 / grupo auth','Control de acceso','Sin sesión, lectura y POST redirigen a login.','T4; phpunit-junit.xml'),('Organización del código','P1 a P8, T1','MVC y convenciones Laravel','Request valida, controlador coordina y servicio persiste; Pint aprobado.','pint-salida.txt, fuentes-inspeccionadas.txt')],
    'HU-02': [('Entradas','M2, M3 / record y store','Aritmética de incremento','10 + 5 = 15; historial persiste saldos.','SQA/CP-08, T2'),('Salidas','M2, M3 / record y store','Aritmética de decremento','15 - 12 = 3 en navegador; prueba aislada 10 - 7 = 3.','SQA/CP-09, T2'),('Stock actualizado','M2 / record','Saldo real sin sobrescritura obsoleta','Servicio relee después de adquirir escritura y actualiza condicionalmente.','T2 modelo desactualizado, T3'),('Stock insuficiente','M2 / record','Saldo no negativo','Salida 4 sobre saldo 3 rechazada; no nuevo historial.','SQA/CP-10, T2'),('Cantidad válida','M1, M2, M10','Enteros positivos y rango','0, -1 y exceso de límite rechazados; mensajes corregidos.','CP-11/12, REG-MAX, T2'),('Historial','M2, M4, M5, M7','Trazabilidad y conservación','Tres registros con tipo, cantidad, saldos, fecha, usuario y notas; sin rutas de edición/borrado.','SQA/CP-13, T2'),('Alertas','M8, M9 / scopeLowStock','Límite inclusivo y estado activo','Stock 3 igual a mínimo 3 produce Stock bajo.','SQA/CP-14, T2'),('Transacciones','M2, B1 / record','Atomicidad y concurrencia SQLite','WAL, espera y primera escritura; rollback probado; dos procesos no venden de más.','T2 rollback, T3'),('Stock protegido','P1, P8, A1','Evitar modificación directa','stock prohibido en formularios; no fillable; movimientos solo en activos.','T1 edición, T2 inactivo'),('Lógica de negocio','M1 a M5','Responsabilidad y legibilidad','Reglas centralizadas en servicio; mensajes específicos en Request; Pint aprobado.','M2, M10, pint-salida.txt')],
}

def inspection_table(hu, full=True):
    rows=[]
    for number,(element,method,criterion,note,proof) in enumerate(inspection[hu],1):
        identifier=f"I{hu[-2:]}-{number:02}"
        action='Mantener; validar por pares.'
        if hu=='HU-02' and number==5: action='HR-04 corregido; regresión aprobada.'
        rows.append((identifier,element,method,criterion,'Cumple',note,action,proof) if full else (identifier,element,'Cumple',note+' Evidencia: '+proof))
    return table(['ID','Elemento','Archivo y método (refs. abajo)','Criterio SQA','Resultado técnico','Hallazgo u observación','Acción correctiva','Evidencia'] if full else ['ID','Elemento','Resultado','Observación y evidencia'],rows)

def pending_block():
    return '''- Equipo externo o auditor designado: [Completar].
- Integrantes y roles: [Completar].
- Fecha de actividad formal: [Completar].
- Observaciones oficiales: [Completar].
- Resultado aprobado por el responsable independiente: [Completar].
- Firma o validación: [Completar].

La elaboración técnica por Codex no acredita la participación de otro equipo, una reunión de inspección ni una auditoría del docente.'''

def minutes_body(hu):
    return f'''Proyecto: StockFácil. Historia: {hu}, {stories[hu]['title']}.

- Fecha de elaboración preliminar: {DATE}.
- Fecha de sesión formal: [Completar].
- Modalidad preliminar: lectura técnica asistida, pruebas HTTP automatizadas y navegador sobre SQLite aislado.
- Modalidad de inspección formal: [Completar].
- Objetivo: {stories[hu]['objective']}
- Alcance: diez elementos de implementación y documentación identificados en el checklist; no certifica estándares del curso no aportados.
- Preparación técnica: Codex, herramienta de asistencia; no constituye un participante humano ni revisor independiente.
- Moderador: [Nombre, equipo y firma].
- Autor o representante del equipo de desarrollo: [Nombre y firma].
- Inspector o lector: [Nombre, equipo y firma].
- Secretario: [Nombre y firma].

Procedimiento realizado: lectura de artefactos, comparación de los seis CA originales, consulta de rutas y migración, ejecución de PHPUnit, captura de formularios reales y contraste del estado SQLite. Los intentos inválidos se enviaron con noValidate para probar las reglas del servidor.

Artefactos inspeccionados: referencias {', '.join(stories[hu]['refs'])}; inventario con archivos y líneas en este paquete. Las capturas corresponden a la interfaz ya implementada; no son mockups previos.

Hallazgos: HR-01, ambigüedad entre catálogos CP, corregido documentalmente; HR-02 y HR-03, actividades formales y rúbrica pendientes. {'HR-04, concordancia del mensaje de cantidad, corregido y comprobado antes/después.' if hu=='HU-02' else 'No se detectó un defecto funcional en los seis CA de registro.'}

Acciones y responsables: AC-01 y AC-02 ejecutadas técnicamente por Codex; equipo humano responsable de ratificarlas: [Completar]. AC-03 corresponde al equipo revisor/pares [Completar] y AC-04 al docente o auditor designado [Completar]. No se asigna un plazo inventado; fecha compromiso de cada equipo: [Completar].

Estado: inspección técnica preliminar completada; inspección formal por pares pendiente. Conclusión preliminar: los elementos comprobados cumplen el alcance implementado, con la limitación de no contar con aprobación de participantes externos. Acuerdos de la sesión real y conclusión formal: [Completar después de inspeccionar].

Firmas de participantes y validación del acta: [Completar].'''

# Fase 1
path='01-preparacion/historias-usuario.md'
body=f'# Fichas académicas de historias de usuario\n\nElaboración: {DATE}. Fuente de requisitos: consigna de la actividad y proyecto existente.\n'
for hu,story in stories.items():
    body+=f"\n## {hu}: {story['title']}\n\n"+table(['Campo','Contenido'],[("Código",hu),("Actor","Administrador de una tienda"),("Descripción",story['description']),("Objetivo",story['objective']),("Prioridad","Alta propuesta para la actividad, pendiente de confirmación del equipo; la consigna no establece una prioridad contractual.")])
    body+='\n### Criterios originales\n\n'+ '\n'.join(f'- CA-{i+1:02}: {text}' for i,text in enumerate(story['criteria']))+'\n\n### Artefactos reales\n\n'+artifact_table(path,hu)
    body+='\n### Funcionalidades y flujo documentado posteriormente\n\n'
    body+=('Acceso autenticado; formulario de producto; validación; creación transaccional; entrada inicial si es positiva; confirmación; catálogo paginado y búsqueda. La edición y desactivación son complementarias.\n' if hu=='HU-01' else 'Acceso autenticado; selección de producto activo; entrada/salida y cantidad; preview orientativo; validación del servidor; saldo e historial atómicos; consulta y alertas.\n')
    body+='\nNo se localizaron mockups previos ni diagramas de casos de uso en los artefactos del proyecto examinados. DESIGN.md documenta el sistema visual; las capturas de esta actividad se obtuvieron posteriormente desde la aplicación real y se etiquetan como evidencia funcional.\n'
body+='\n### Documentación existente\n\nREADME.md; docs/historias-usuario.md; docs/arquitectura.md; docs/casos-prueba.md; docs/verificacion.md; PRODUCT.md y DESIGN.md. Los documentos previos no se sustituyen y los resultados de esta actividad se mantienen separados.\n'
write(path,body)
path='01-preparacion/criterios-aceptacion.md'
body='# Criterios de aceptación originales y alcance\n\n'+f'Fecha: {DATE}. Se preserva el texto de la consigna; las reglas complementarias no reemplazan los CA.\n'
for hu,story in stories.items():
    body+=f'\n## {hu}\n\n'+table(['Código','Descripción original'],[(f'CA-{i+1:02}',text) for i,text in enumerate(story['criteria'])])
body+='''
## Precisiones de implementación

HU-01 exige además categoría válida, precio con hasta dos decimales, mínimo entero no negativo y stock inicial entero. El SKU se normaliza a mayúsculas. El stock inicial cero se guarda sin crear un movimiento cero. Son reglas complementarias observadas, no modificaciones de los seis CA.

HU-02 agrega cantidad entera, límite superior de 2147483647, producto activo, responsable autenticado, protección transaccional y conservación del historial. La alerta usa stock <= mínimo, lo cual incluye el límite solicitado y los productos por debajo de él. No se encontró una discrepancia funcional con los doce CA originales en los casos ejecutados.

## Identificación de casos

SQA/CP-01 a SQA/CP-14 designan exclusivamente los casos de esta actividad. Los CP de docs/casos-prueba.md pertenecen al catálogo previo y conservan sus IDs. Esta distinción resuelve HR-01 sin alterar la planificación anterior.
'''
write(path,body)
path='01-preparacion/matriz-trazabilidad.md'
rows=[]
for hu,story in stories.items():
    for i,text in enumerate(story['criteria']):
        ids=story['ca_cases'][i]
        proof=', '.join(evidence(path,observed[cp]['evidence'],cp+' captura') for cp in ids)
        rows.append((hu,f'CA-{i+1:02}',', '.join(story['ca_refs'][i]),', '.join('SQA/'+cp for cp in ids),'Cumple',proof))
write(path,'# Matriz de trazabilidad\n\n'+table(['Historia','CA','Archivo/módulo (ref.)','Caso','Resultado técnico','Evidencia real'],rows)+'\n## Correspondencia de referencias\n\n'+artifact_table(path,'HU-01')+'\n'+artifact_table(path,'HU-02')+'\nLos métodos de prueba concretos y resultados JUnit se detallan en 04-pruebas/casos-prueba.md. Revisión y auditoría independientes permanecen pendientes.\n')

# Revisión e inspección
for hu in stories:
    suffix=hu[-2:]
    path=f'02-revision/checklist-hu{suffix}.md'
    write(path,f'# Checklist de revisión técnica preliminar: {hu}\n\nFecha de elaboración: {DATE}. Los resultados siguientes proceden de lectura y pruebas de Codex; no han sido ratificados por otro equipo.\n\n'+review_table(hu)+'\n## Referencias de artefactos\n\n'+artifact_table(path,hu)+'\n## Validación externa pendiente\n\n'+pending_block())
    path=f'03-inspeccion/checklist-inspeccion-hu{suffix}.md'
    write(path,f'# Checklist de inspección preliminar: {hu}\n\nFecha: {DATE}. Se comprobaron los elementos mediante lectura de código, pruebas y evidencia visual. Cumple se refiere al alcance técnico, no a la aprobación formal por pares.\n\n'+inspection_table(hu)+'\n## Archivos y líneas de las referencias\n\n'+artifact_table(path,hu)+'\n## Participación por pares\n\n'+pending_block())
    path=f'03-inspeccion/acta-inspeccion-hu{suffix}.md'
    write(path,f'# Acta de inspección: {hu}\n\n**Borrador técnico preliminar, pendiente de sesión y firmas reales.**\n\n'+minutes_body(hu)+'\n\n## Checklist y artefactos anexos\n\n'+doc(path,f'03-inspeccion/checklist-inspeccion-hu{suffix}.md','Checklist técnico detallado')+'\n\n'+artifact_table(path,hu))

path='02-revision/hallazgos-revision.md'
write(path,f'''# Hallazgos de revisión técnica preliminar

Fecha de elaboración: {DATE}. Hallazgos documentados inicialmente antes de aplicar las acciones. Revisión por otro equipo: pendiente.

'''+table(['ID','Historia','Hallazgo','Evidencia','Importancia','Acción','Estado inicial / actual'],[
('HR-01','Ambas','CP-06 previo y CP-06 de la actividad designan casos distintos.','docs/casos-prueba.md y consigna, sección 8.','Bajo, documental','Namespace SQA/CP y trazabilidad a métodos.','Pendiente / Corregido documentalmente'),
('HR-02','Ambas','No hay revisión externa ni sesión formal de inspección por pares acreditadas.','Campos pendientes de consigna; documentos previos.','Medio, de proceso','Completar equipo, participantes, roles, observaciones y firmas reales.','Pendiente / Pendiente'),
('HR-03','Ambas','No se aportó plan/rúbrica de calidad del curso ni auditoría independiente aprobada.','Material recibido y alcance de la consigna.','Medio, de alcance','Validar los doce CA técnicamente y solicitar evaluación formal de estándares.','Pendiente / Pendiente'),
('HR-04','HU-02','Mensaje de rango decía El cantidad; regla de rechazo sí funcionaba.','resultados-navegador-antes.json; hu02-error-cero-antes.png; regresion-antes.xml.','Bajo, claridad','MovementRequest::messages para quantity.min/max; regresión y capturas posteriores.','Pendiente / Corregido y verificado'),
])+'''
## Observaciones de revisión

No se detectó una discrepancia funcional entre la planificación de los doce CA y los casos ejecutados. HR-04 es un defecto de redacción; no se presenta como pérdida de stock ni se borra su evidencia anterior. HR-02 y HR-03 son límites del proceso académico y no defectos de la aplicación.

La primera preparación de la prueba de regresión tuvo una llamada de aserción inválida del propio test. Ese registro se conserva como regresion-preparacion-error.txt/xml, separado de la regresión válida; no se cuenta como defecto de StockFácil. Tras corregir la llamada, la regresión válida reprodujo tres fallos de mensajes antes del cambio de producción.

## Equipo externo

'''+pending_block())
path='03-inspeccion/registro-acciones-correctivas.md'
write(path,'# Registro de acciones correctivas\n\n'+table(['Acción','Hallazgo','Archivo/artefacto','Resultado anterior','Corrección y resultado posterior','Responsable técnico / humano','Estado'],[
('AC-01','HR-01','Documentación docs/sqa','Identificadores CP ambiguos entre catálogos.','SQA/CP-01 a CP-14 y métodos PHPUnit explícitos; catálogo previo conservado.','Codex / ratificación del equipo [Completar]','Corregido'),
('AC-02','HR-04','app/Http/Requests/MovementRequest.php; tests/Feature/InventoryTest.php','Suite previa: 42/42, 276 aserciones, sin comprobar concordancia. Regresión válida ampliada: 3 fallidas, 5 aprobadas por mensajes min/max.','Mensajes La cantidad para min/max. Suite posterior: 43/43, 286 aserciones. CP-11, CP-12 y REG-MAX aprobados en navegador; stock 3 e historial 3.','Codex / ratificación del equipo [Completar]','Corregido y verificado'),
('AC-03','HR-02','Checklists y actas','Revisión/inspección formales sin acreditación.','Formatos completos preparados; sesión y observaciones oficiales pendientes.','Equipo revisor/pares [Completar]','Pendiente'),
('AC-04','HR-03','Matrices e informes de auditoría','Rúbrica/plan y auditoría formal no aportados.','Preevaluación 12/12 CA; estándares y aprobación independientes pendientes.','Docente o auditor [Completar]','Pendiente'),
])+'\nLa intervención en producción se limita a mensajes de validación. No se modificaron arquitectura, cálculos de stock, rutas ni funcionalidades. Las huellas de integridad muestran solo MovementRequest.php e InventoryTest.php modificados entre los archivos originales inspeccionados. El inventario de desarrollo conserva su huella lógica. Fecha y firma de cierre humano de cada acción: [Completar].\n\nEvidencias: regresion-antes.txt/xml, phpunit-antes.txt/xml, phpunit-salida.txt, phpunit-junit.xml, revalidacion-correccion.json, capturas antes/después e integridad-final.json. El error de preparación del test se archiva por separado, sin atribuirlo al producto.\n')

# Pruebas
path='04-pruebas/casos-prueba.md'
body='''# Casos funcionales ejecutados

Los IDs siguientes pertenecen al catálogo SQA de esta actividad. Los casos de navegador usan una instancia con SQLite temporal, producto SQA-001 y administrador de demostración. Las pruebas PHPUnit crean sus propios datos en SQLite en memoria; sus variantes no comparten el estado secuencial del navegador.

Para probar errores del servidor se activó noValidate en los formularios de pruebas negativas. No se alteró el formulario de la aplicación. El navegador seguía enviando peticiones reales con sesión y token CSRF.
'''
for cp,(objective,precondition,data,steps,expected) in cases.items():
    hu='HU-01' if int(cp[-2:])<=7 else 'HU-02'
    story=stories[hu]
    indices=[i for i,ids in enumerate(story['ca_cases']) if cp in ids]
    methods=sorted({method for i in indices for method in story['ca_tests'][i]})
    body+=f'\n## SQA/{cp}: {objective}\n\n'+table(['Campo','Contenido'],[
        ('Historia',hu),('Objetivo',objective),('Precondiciones',precondition),('Datos de entrada',data),('Pasos',steps),('Resultado esperado',expected),('Resultado obtenido',observed[cp]['obtained']),('Estado','Aprobado'),('Evidencia',evidence(path,observed[cp]['evidence'])+'; '+evidence(path,'resultados-navegador.json')+'; '+evidence(path,'phpunit-junit.xml')),('Prueba automática relacionada','; '.join(methods)),
    ])
body+='''
## Cobertura adicional ejecutada

La suite también verifica hash y sesiones, protección de rutas, ausencia de registro público, SKU en minúsculas, valores fraccionarios, stock inicial cero, rollback del producto, edición sin modificación de stock, conservación de inactivos, paginación, modelo con saldo obsoleto, rollback del movimiento, restricción SQLite, dos salidas concurrentes y seeder repetible. REG-MAX comprueba la cantidad 2147483648 y el mensaje de límite superior.

La prueba HTTP de salida válida usa 10 - 7 = 3; el navegador, en su secuencia, usa 15 - 12 = 3. Ambas son variantes documentadas de CA-02. No se presentan como una única ejecución con datos iguales.
'''
write(path,body)
path='04-pruebas/resultados-pruebas.md'
class_rows=[]
for node in junit.iter('testsuite'):
    if node.get('name','').startswith('Tests\\Feature\\'):
        class_rows.append((node.get('name').split('\\')[-1],node.get('tests'),node.get('assertions'),node.get('failures'),node.get('errors')))
write(path,f'''# Resultados reales de pruebas

Fecha local: {DATE}, America/La_Paz. PHP 8.3.33, PHPUnit 12.5.39, Laravel 13 y SQLite. Los timestamps UTC de los JSON de navegador se conservan sin sustituirlos por fechas de reuniones.

## Ejecuciones

- Suite original: 42 pruebas aprobadas, 276 aserciones; evidencia phpunit-antes.txt/xml.
- Preparación inicial del test ampliado: 3 errores de aserción del test, 5 aprobadas; registro separado regresion-preparacion-error.txt/xml. No es un defecto del producto.
- Regresión válida anterior a HR-04: 3 fallidas, 5 aprobadas; las tres comprueban textos de cantidad mínimo/máximo. Evidencia regresion-antes.txt/xml.
- Suite posterior: **{summary['tests']} aprobadas, {summary['assertions']} aserciones; 0 fallos, 0 errores y 0 omitidas**. Evidencia phpunit-junit.xml y phpunit-salida.txt. Tiempo JUnit: {suite.get('time')} s; el tiempo total mostrado por Artisan incluye su envoltura.
- Navegador: 14 casos de la actividad aprobados; CP-11 y CP-12 reejecutados después del cambio, más REG-MAX. Evidencia resultados-navegador.json y revalidacion-correccion.json.

'''+table(['Clase','Pruebas','Aserciones','Fallos','Errores'],class_rows)+'''
## Resultados por caso

'''+table(['Caso SQA','Historia','Estado','Resultado obtenido'],[(cp,'HU-01' if int(cp[-2:])<=7 else 'HU-02','Aprobado',observed[cp]['obtained']) for cp in cases])+'''
## Protección de datos y coherencia

Los comandos de PHPUnit se ejecutaron con APP_ENV=testing, DB_CONNECTION=sqlite y DB_DATABASE=:memory:, además de phpunit.xml. ConcurrencyTest usa un archivo temporal y lo elimina. Las migraciones/seeders del navegador se ejecutaron solo sobre tmp/sqa/navegador.sqlite, con servidor en el puerto 8003.

integridad-final.json confirma sin cambios la huella lógica del inventario de desarrollo: 12 productos, 24 movimientos, 5 categorías y 184 unidades activas. sqlite-navegador.json comprueba los tres eventos 0 -> 10 -> 15 -> 3, fechas/responsables presentes, integrity_check=ok y sin infracciones de claves foráneas.

## Comandos reales

```powershell
$env:APP_ENV='testing'
$env:DB_CONNECTION='sqlite'
$env:DB_DATABASE=':memory:'
php artisan test --testdox --colors=never --log-junit=docs/sqa/04-pruebas/evidencias/phpunit-junit.xml
php vendor/laravel/pint/builds/pint --test --format=txt
composer validate --strict
```

El script capturar-evidencias.cjs utiliza Playwright ya disponible en el entorno mediante PLAYWRIGHT_MODULE. Debe apuntar únicamente a un servidor de pruebas mediante SQA_URL. No se añade Playwright a las dependencias de StockFácil. verificar-correccion.cjs usa el producto temporal creado por el primer script.

## Limitaciones

No hay casos bloqueados ni no ejecutados entre SQA/CP-01 y CP-14. No se evaluaron hosting, carga de producción, otros navegadores, lectores de pantalla ni una rúbrica de curso no aportada. La aprobación funcional no equivale a revisión externa, inspección formal o auditoría oficial.
''')

# Auditoría preliminar
for hu in stories:
    path=f"05-auditoria/preauditoria-hu{hu[-2:]}.md"
    write(path,f'''# Preevaluación técnica de cumplimiento: {hu}

Fecha de elaboración: {DATE}. Auditoría independiente: pendiente. El responsable de esta evaluación técnica es Codex; no se atribuye al docente ni a otro equipo.

## Objetivo y alcance

{stories[hu]['objective']} Se consideran exclusivamente sus seis CA originales y las comprobaciones técnicas relacionadas. Plan de calidad/rúbrica del curso: no aportados; conformidad oficial con esos estándares: No verificado.

## Referencias y procedimiento

Consigna de la actividad, criterios de planificación, código real, convenciones MVC observadas, pruebas PHPUnit, capturas Chromium y estados SQLite. Se contrastó el requisito con el archivo, se ejecutaron casos válidos/negativos y se comprobó persistencia. Las comprobaciones de forma usan Pint y Composer; no se presentan como una norma del curso.

## Matriz de conformidad

'''+ca_table(path,hu)+f'''
## Porcentaje técnico verificado

({compliance[hu]['compliant']} criterios comprobados que cumplen / 6 criterios aplicables) x 100 = **{compliance[hu]['percent']:.0f}%**.

Criterios no verificados: 0. No aplicables: 0. Pruebas bloqueadas de la actividad: 0. La validación independiente de este porcentaje y la conformidad con la rúbrica son pendientes separados; no se cuentan como CA aprobados por un docente.

## Hallazgos y recomendaciones

HR-01 resuelto con namespace SQA/CP. HR-02 y HR-03 pendientes por proceso/alcance. {'HR-04 corregido: concordancia de mensajes quantity.min/max, con regresión y capturas antes/después.' if hu=='HU-02' else 'No se encontró una no conformidad funcional en los seis CA de registro.'}

Recomendación: repetir los casos sobre una copia de pruebas, contrastar la matriz con la rúbrica real y conservar las evidencias originales antes de firmar. No usar el 100% técnico como una certificación del sistema completo.

## Conclusión preliminar y aprobación oficial

La implementación comprobada cumple los seis CA en el alcance y entorno documentados. La auditoría formal no se ha realizado ni validado en esta preparación.

'''+pending_block()+'\n\n## Artefactos de soporte\n\n'+artifact_table(path,hu))
path='05-auditoria/cumplimiento-global.md'
write(path,'# Cumplimiento técnico global de los criterios evaluados\n\n'+table(['Historia','CA aplicables','CA que cumplen','No verificados','No aplicables','Porcentaje técnico'],[(hu,6,compliance[hu]['compliant'],0,0,f"{compliance[hu]['percent']:.0f}%") for hu in stories])+f'''
Resultado global: ({global_compliant} / {global_applicable}) x 100 = **{global_compliant/global_applicable*100:.0f}%**. Se suman los CA aplicables; no se usa un promedio sin ponderación.

El denominador incluye los doce CA originales de las dos historias. No se excluyó ningún CA como No aplica ni se contó un No verificado como Cumple. El resultado no abarca todos los módulos, estándares del curso, desempeño ni seguridad integral del proyecto. Las tres actividades académicas formales siguen sin validación independiente.

Los valores se generaron desde el JUnit vigente y los resultados de navegador en cumplimiento-calculado.json. La matriz detallada y sus referencias están en preauditoria-hu01.md y preauditoria-hu02.md.
''')
path='05-auditoria/validacion-independiente-pendiente.md'
write(path,'''# Validación independiente pendiente

## Qué debe completar el equipo y el docente

1. Identificar universidad, asignatura, docente y los integrantes reales en los informes.
2. Obtener la revisión técnica de requisitos/diseño por otro equipo; completar checklists, observaciones, fecha e identificación del equipo.
3. Realizar la inspección formal por pares; completar roles, participantes, acuerdos, responsables y firmas de ambas actas.
4. Aportar el plan de calidad o la rúbrica de estándares del curso y registrar su conformidad; esa evaluación está No verificado.
5. Designar al auditor independiente; revisar la evidencia y confirmar o modificar los porcentajes técnicos con justificación.
6. Registrar fecha de auditoría, observaciones oficiales, resultado aprobado y firma o validación. No retrofechar estas actividades a la fecha de elaboración técnica.

## Estado separado por actividad

'''+table(['Actividad','Preparación técnica','Evaluación formal'],[('Revisión','12 aspectos analizados por historia y hallazgos registrados.','Pendiente de otro equipo.'),('Inspección','10 elementos de código/documentación comprobados por historia.','Pendiente de sesión y validación por pares.'),('Auditoría','6/6 CA por historia verificados técnicamente.','Pendiente de auditor designado/docente y rúbrica.')])+'''
## Campos del auditor

'''+pending_block()+'''

No hay firmas, nombres de participantes ni aprobaciones oficiales inventados. Si la verificación humana modifica un resultado, conservar la versión técnica original y emitir una versión validada con fecha, evidencia y motivación.
''')

def academic_fields(hu=None):
    return table(['Dato','Valor'],[('Universidad','[Completar nombre oficial]'),('Asignatura','[Completar]'),('Docente','[Completar]'),('Integrantes','[Completar nombres reales]'),('Proyecto','StockFácil'),('Historia',hu or 'HU-01 y HU-02'),('Fecha de elaboración',DATE),('Estado','Evaluación técnica preliminar; validación independiente pendiente')])

def report(hu):
    story=stories[hu]; suffix=hu[-2:]; path=f'06-informes-finales/informe-sqa-hu{suffix}.md'
    introduction=('El registro de productos es la entrada del inventario: un error en nombre, SKU, precio o cantidad inicial afecta la calidad de los datos posteriores. Se revisaron requisitos, se inspeccionó la implementación y se ejecutaron formularios reales sobre una base de pruebas.' if hu=='HU-01' else 'Cada movimiento cambia un saldo compartido. La evaluación se concentró en los límites de cantidad, la consistencia entre stock e historial y el aviso de reposición. El servicio transaccional y las pruebas concurrentes aportan evidencia adicional a los casos visibles de la interfaz.')
    recommendations=('Mantener la normalización de SKU y la restricción única de SQLite; conservar el registro inicial transaccional; usar la búsqueda o paginación para localizar productos; someter los criterios y la ficha a la revisión del otro equipo.' if hu=='HU-01' else 'Conservar stock e historial dentro de la transacción, la lectura bajo bloqueo de escritura y la actualización condicional; mantener la regresión de mensajes min/max; realizar la inspección formal del manejo concurrente con pares; validar la rúbrica del curso antes de cerrar la auditoría.')
    body=f'# INFORME SQA - {hu.upper()} {story["title"].upper()}\n\n## 1. Datos generales\n\n'+academic_fields(hu)+f'\n## 2. Introducción\n\n{introduction}\n\nEste informe distingue la revisión e inspección técnicas preliminares de las actividades humanas exigidas por la consigna. Las actas y la auditoría quedan listas para su validación; no se acredita una participación externa inexistente.\n\n## 3. Objetivo\n\n{story["objective"]}\n\n## 4. Descripción de la historia\n\n{story["description"]}\n\n### Criterios originales\n\n'
    body+='\n'.join(f'- CA-{i+1:02}: {text}' for i,text in enumerate(story['criteria']))
    body+='\n\n### Alcance complementario\n\n'+('Se comprobó stock inicial trazable, SKU en mayúsculas, edición sin cambio directo de stock y conservación de productos inactivos. El stock cero inicial es válido y no crea un movimiento cero.\n' if hu=='HU-01' else 'Se comprobó cantidad entera, producto activo, responsable autenticado, rollback, saldos obsoletos y dos salidas concurrentes. La alerta usa <= mínimo e incluye el mínimo exacto solicitado.\n')
    body+='\n## 5. Artefactos relacionados\n\n'+artifact_table(path,hu)+'\nDocumentación examinada: README.md; docs/historias-usuario.md; docs/arquitectura.md; docs/casos-prueba.md; docs/verificacion.md; PRODUCT.md y DESIGN.md. No se localizaron mockups previos; las capturas anexas son posteriores a la implementación.\n'
    body+='\n## 6. Evidencia de revisión\n\n'+review_table(hu,False)
    body+='\n### Hallazgos y acciones\n\n'+('HR-01: IDs CP ambiguos entre catálogos; resuelto al usar SQA/CP y vincular métodos reales. HR-02: revisión externa e inspección por pares pendientes. HR-03: rúbrica y auditoría independiente no aportadas. No se encontró un defecto funcional de registro en los seis CA ejecutados.\n' if hu=='HU-01' else 'HR-01: namespace SQA/CP establecido. HR-02/03: actividades formales y rúbrica pendientes. HR-04: el mensaje decía «El cantidad»; se corrigió mediante MovementRequest::messages para min/max. La regresión válida tuvo tres fallos de texto antes del cambio; después, la suite completa y las capturas de cero/negativo/límite aprobaron. La operación inválida ya se rechazaba antes y el saldo se conservó.\n')
    body+='\nEquipo revisor: [Completar]. Integrantes: [Completar]. Fecha externa: [Completar]. Firma/validación: [Completar]. Observaciones adicionales: [Completar].\n'
    body+='\n## 7. Evidencia de inspección\n\n'+inspection_table(hu,False)+'\n### Acta preliminar\n\n'+minutes_body(hu)+'\n\nChecklist completo de ocho columnas: '+doc(path,f'03-inspeccion/checklist-inspeccion-hu{suffix}.md','Anexo de inspección')+'.\n'
    body+='\n## 8. Casos de prueba y resultados reales\n\n'
    for cp in story['cases']:
        objective,precondition,data,steps,expected=cases[cp]
        body+=f'\n### SQA/{cp}: {objective}\n\n'+table(['Campo','Contenido'],[('Precondiciones',precondition),('Entrada y pasos',data+' '+steps),('Resultado esperado',expected),('Resultado obtenido',observed[cp]['obtained']),('Estado y evidencia','Aprobado; '+evidence(path,observed[cp]['evidence']))])
    body+=f'\nSuite completa después de HR-04: {summary["tests"]} pruebas aprobadas y {summary["assertions"]} aserciones, sin errores, fallos ni omitidas. Los 14 casos de actividad se ejecutaron en navegador; siete corresponden a esta historia. Las variantes PHPUnit usan SQLite en memoria y pueden tener datos diferentes a la secuencia de navegador; por ejemplo, salida 10 - 7 en PHPUnit y 15 - 12 en navegador.\n'
    body+='\n## 9. Resultado de auditoría\n\n**Preevaluación técnica, pendiente de auditoría independiente.**\n\n'+ca_table(path,hu,False)+f'\nCumplimiento verificado: ({compliance[hu]["compliant"]}/6) x 100 = **{compliance[hu]["percent"]:.0f}%**. No verificados: 0 CA. No aplicables: 0. Pruebas bloqueadas: 0. El plan/rúbrica del curso y la aprobación oficial son No verificado y quedan fuera de este porcentaje de CA.\n\n'+pending_block()
    body+=f'\n\n## 10. Recomendaciones\n\n{recommendations}\n\nSolicitar revisión de otro equipo, completar roles/firmas de pares y registrar el resultado del auditor independiente con su fecha real.\n'
    conclusion=('Los casos válidos e inválidos demuestran que el catálogo se registra con validación y que el producto queda consultable en SQLite. La entrada inicial conserva trazabilidad y los intentos rechazados no crean registros. El 100% técnico de seis CA se respalda con pruebas y capturas, aunque aún no acredita la revisión externa, la inspección formal ni la aprobación docente.' if hu=='HU-01' else 'Los movimientos comprobados mantuvieron saldos 10 a 15 a 3, rechazaron exceso, cero y negativo, y dejaron tres registros coherentes con una alerta en mínimo 3. El servicio conserva consistencia ante rollback y dos salidas concurrentes. Se corrigió un hallazgo menor de redacción sin alterar las reglas. El 100% técnico de seis CA está pendiente de ratificación independiente.')
    body+=f'\n## 11. Conclusiones\n\n{conclusion}\n\nNo se reinició ni modificó el inventario de desarrollo: la huella lógica antes/después coincide.\n\n## 12. Anexos\n\n'
    body+= '- '+evidence(path,'phpunit-junit.xml','JUnit de ejecución final')+' y '+evidence(path,'phpunit-salida.txt','salida completa')+'.\n'
    body+= '- '+evidence(path,'resultados-navegador.json','casos reales de navegador')+' y '+evidence(path,'sqlite-navegador.json','persistencia en SQLite temporal')+'.\n'
    body+= '- '+evidence(path,'fuentes-inspeccionadas.txt','código con líneas')+', '+evidence(path,'referencias-codigo.json','mapa de referencias')+' y '+evidence(path,'integridad-final.json','integridad de desarrollo')+'.\n'
    body+= '- '+doc(path,'02-revision/hallazgos-revision.md','Registro de hallazgos')+' y '+doc(path,'03-inspeccion/registro-acciones-correctivas.md','acciones correctivas')+'.\n'
    figures=[('hu01-formulario.png','Formulario real de productos, posterior a implementación.'),('hu01-error-nombre.png','Rechazo del nombre vacío en el servidor.'),('hu01-producto-listado.png','Producto persistido visible mediante búsqueda por SKU.')] if hu=='HU-01' else [('hu02-formulario-movimiento.png','Formulario real con entrada 5 y preview 10 a 15.'),('hu02-historial.png','Historial real con tres movimientos del producto temporal.'),('hu02-alerta-minimo.png','Alerta real al llegar a stock 3 y mínimo 3.'),('hu02-error-cero.png','Mensaje de cantidad corregido, saldo sin cambios.')]
    for i,(name,caption) in enumerate(figures,1):
        image_path=os.path.relpath(EV/name,(SQA/path).parent).replace('\\','/')
        body+=f'\n### Figura {i}. {caption}\n\n![{caption}]({image_path})\n\nCaptura real de Chromium sobre SQLite temporal; el archivo original está disponible en '+evidence(path,name)+'.\n'
    if hu=='HU-02': body+='\nEvidencia antes de HR-04: '+evidence(path,'hu02-error-cero-antes.png','captura original de concordancia')+', '+evidence(path,'regresion-antes.xml','regresión válida antes')+' y '+evidence(path,'revalidacion-correccion.json','revalidación después')+'. La preparación inicial errónea del test se conserva por separado; no se clasifica como fallo funcional del producto.\n'
    write(path,body)
for hu in stories: report(hu)

path='06-informes-finales/informe-sqa-general.md'
body='# INFORME GENERAL DE ASEGURAMIENTO DE LA CALIDAD - STOCKFÁCIL\n\n## 1. Portada académica\n\n'+academic_fields()+'''
## 2. Introducción

La actividad aplica controles de calidad a un sistema existente. Se eligieron el registro de productos y los movimientos porque conectan la calidad de los datos del catálogo con la consistencia de las existencias. Se documentan requisitos, implementación y pruebas reales, y se preparan los formatos para las evaluaciones humanas posteriores.

## 3. Descripción del sistema

StockFácil es una aplicación Laravel 13 con Blade, Tailwind CSS, Eloquent y SQLite local. Un administrador consulta el dashboard, registra/edita/desactiva productos, anota entradas/salidas, revisa alertas y consulta el historial. No se creó otro proyecto ni se reconstruyó el sistema para esta actividad.

## 4. Objetivos

- Comprobar los doce criterios originales de HU-01 y HU-02.
- Identificar artefactos reales y vincularlos con casos y evidencia.
- Preparar revisión, inspección y auditoría preliminares sin inventar participación externa.
- Registrar y corregir hallazgos pequeños, conservar antes/después y proteger SQLite de desarrollo.

## 5. Metodología SQA

Se examinó la estructura MVC, modelos/relaciones, migración, rutas, Requests, servicio y vistas, además de las pruebas y documentación. Se guardó la línea base con huellas SHA-256, se ejecutó PHPUnit en SQLite aislado y se capturaron formularios mediante Chromium en una instancia temporal. Se compararon seis CA por historia y se calculó el porcentaje sobre todos los aplicables.

La revisión de otro equipo, la sesión formal por pares y la auditoría independiente no están acreditadas. Sus campos y formatos quedan pendientes para personas reales. No se aportó una rúbrica/plan del curso; no se presupone su cumplimiento.

## 6. Historias seleccionadas

'''+table(['Historia','Descripción','Alcance'],[(hu,story['description'],story['objective']) for hu,story in stories.items()])+'''
## 7. Resumen de revisiones

Se comprobó por historia la claridad del actor/objetivo, seis CA verificables, coherencia de requisitos, correspondencia de diseño, campos, validaciones, errores, flujo y artefactos. Los doce aspectos por historia tienen evidencia técnica identificada. La ratificación por otro equipo continúa pendiente.

HR-01 resolvió la ambigüedad de IDs CP con el namespace SQA/CP; HR-04 identificó concordancia incorrecta en el mensaje de cantidad. HR-02 y HR-03 documentan límites formales, no defectos del software.

## 8. Resumen de inspecciones

HU-01: diez elementos revisados sobre validación, unicidad, persistencia, entrada inicial, listado, errores, autenticación y organización MVC. HU-02: diez elementos sobre aritmética, cantidad, saldo insuficiente, historial, alertas, transacciones y protección del stock. Se prepararon actas con roles sin atribuir nombres, sesiones o firmas.

## 9. Resultados de pruebas funcionales

'''+table(['Ejecución','Resultado','Interpretación'],[('Suite inicial','42 aprobadas, 276 aserciones','Línea base funcional; no comprobaba concordancia.'),('Preparación del test de regresión','3 errores, 5 aprobadas','Error en la llamada de aserción del test; corregido y archivado por separado.'),('Regresión válida anterior a HR-04','3 fallidas, 5 aprobadas','Reprodujo mensajes El cantidad para min/max; rechazo de operación sí funcionaba.'),('Suite final','43 aprobadas, 286 aserciones; 0 fallos/errores/omitidas','Incluye límite superior y aserciones de redacción.'),('Navegador','14/14 casos aprobados; CP-11/12 reejecutados y REG-MAX adicional','Capturas y JSON con resultados observados.')])+'''
Los intentos de creación inválidos no añadieron productos; el producto temporal quedó con movimientos 0 a 10, 10 a 15 y 15 a 3. Stock insuficiente, cero, negativo y exceso de límite conservaron saldo e historial. La prueba concurrente admitió una sola salida de 7 entre dos procesos sobre stock 10, saldo final 3.

## 10. Resultados técnicos preliminares de auditoría

'''+table(['Historia','CA aplicables','Cumplen','No verificados','Técnico'],[(hu,6,compliance[hu]['compliant'],0,f"{compliance[hu]['percent']:.0f}%") for hu in stories])+f'''
Global: ({global_compliant}/{global_applicable}) x 100 = **{100*global_compliant/global_applicable:.0f}%** de los doce CA evaluados. No aplicables: 0. Pruebas bloqueadas de la actividad: 0. Es una preevaluación técnica pendiente de aprobación independiente; no es un porcentaje del sistema completo ni de la rúbrica del curso.

## 11. Comparación de historias

'''+table(['Aspecto','HU-01','HU-02'],[('Riesgo evaluado','Calidad/duplicidad de datos del catálogo.','Consistencia de saldo y trazabilidad.'),('Artefacto central','ProductRequest y createProduct.','MovementRequest y record.'),('Casos de actividad','SQA/CP-01 a CP-07, siete aprobados.','SQA/CP-08 a CP-14, siete aprobados.'),('Persistencia','Producto y entrada inicial.','Entradas/salidas y saldos consecutivos.'),('Hallazgo funcional abierto','Ninguno en los CA ejecutados.','Ninguno en los CA ejecutados; HR-04 corregido.'),('Validación humana','Revisión, inspección y auditoría pendientes.','Revisión, inspección y auditoría pendientes.')])+'''
## 12. Hallazgos principales

'''+table(['ID','Importancia','Descripción','Estado'],[('HR-01','Bajo','IDs CP entre catálogos diferentes.','Corregido documentalmente.'),('HR-02','Medio, proceso','Falta ratificación externa y sesión formal por pares.','Pendiente.'),('HR-03','Medio, alcance','Rúbrica/plan y aprobación independiente no aportados.','Pendiente.'),('HR-04','Bajo, claridad','Concordancia El cantidad en mensajes de rango.','Corregido y verificado; evidencia anterior conservada.')])+'''
## 13. Acciones correctivas

La corrección de producción se limita a MovementRequest::messages para quantity.min/max. InventoryTest añade comprobaciones de texto y el límite superior. No se alteraron reglas de saldo ni arquitectura. El primer intento de preparar la regresión se corrigió antes de usarlo como evidencia del producto. Las pruebas válidas antes/después, capturas y huellas permiten reconstruir la acción.

La ambigüedad de casos se resuelve dentro de docs/sqa, sin reescribir el catálogo previo. Los responsables humanos del cierre académico, los plazos y las firmas son campos pendientes de los equipos reales.

## 14. Recomendaciones

- Entregar los informes, sus fuentes Markdown y la evidencia original; no solo el porcentaje.
- Revisar con otro equipo las fichas y completar observaciones de requisitos/diseño.
- Realizar inspección formal por pares con roles, acuerdos y firmas en las dos actas.
- Facilitar la rúbrica al auditor y registrar un resultado independiente, con fecha real.
- Mantener SQLite aislado y los casos de regresión al modificar catálogo o inventario.

## 15. Conclusiones generales

Los doce CA se comprobaron mediante código, pruebas HTTP y formularios reales. El catálogo valida y persiste; las existencias se actualizan y mantienen historial coherente. Se corrigió un defecto menor de redacción y se conservó la evidencia inicial. La huella lógica del inventario de desarrollo coincide antes y después, con 12 productos, 24 movimientos y 184 unidades activas.

El resultado técnico es 100% de los doce CA aplicables. La actividad académica aún requiere los participantes externos y el docente: este paquete prepara la evaluación formal y no suplanta sus conclusiones.

## 16. Anexos y evidencias

'''
for other,label in [('01-preparacion/historias-usuario.md','Fichas'),('01-preparacion/criterios-aceptacion.md','CA originales'),('01-preparacion/matriz-trazabilidad.md','Trazabilidad'),('02-revision/hallazgos-revision.md','Hallazgos'),('03-inspeccion/registro-acciones-correctivas.md','Acciones'),('04-pruebas/casos-prueba.md','Casos detallados'),('04-pruebas/resultados-pruebas.md','Resultados'),('05-auditoria/validacion-independiente-pendiente.md','Validación pendiente'),('06-informes-finales/informe-sqa-hu01.md','Informe independiente HU-01'),('06-informes-finales/informe-sqa-hu02.md','Informe independiente HU-02')]:body+='- '+doc(path,other,label)+'.\n'
for name in ['phpunit-junit.xml','phpunit-salida.txt','phpunit-antes.xml','regresion-antes.xml','resultados-navegador.json','revalidacion-correccion.json','sqlite-navegador.json','integridad-final.json','referencias-codigo.json','fuentes-inspeccionadas.txt']:body+='- '+evidence(path,name)+'.\n'
for name,caption in [('dashboard.png','Dashboard real de la instancia temporal, antes de los casos.'),('hu01-producto-listado.png','Producto SQA-001 registrado y consultable.'),('hu02-historial.png','Historial coherente de la secuencia ejecutada.')]:
    url=os.path.relpath(EV/name,(SQA/path).parent).replace('\\','/')
    body+=f'\n### Captura: {caption}\n\n![{caption}]({url})\n\nEvidencia original: '+evidence(path,name)+'.\n'
write(path,body)

path='README-SQA.md'
expected=['01-preparacion/historias-usuario.md','01-preparacion/criterios-aceptacion.md','01-preparacion/matriz-trazabilidad.md','02-revision/checklist-hu01.md','02-revision/checklist-hu02.md','02-revision/hallazgos-revision.md','03-inspeccion/checklist-inspeccion-hu01.md','03-inspeccion/checklist-inspeccion-hu02.md','03-inspeccion/acta-inspeccion-hu01.md','03-inspeccion/acta-inspeccion-hu02.md','03-inspeccion/registro-acciones-correctivas.md','04-pruebas/casos-prueba.md','04-pruebas/resultados-pruebas.md','05-auditoria/preauditoria-hu01.md','05-auditoria/preauditoria-hu02.md','05-auditoria/cumplimiento-global.md','05-auditoria/validacion-independiente-pendiente.md','06-informes-finales/informe-sqa-hu01.md','06-informes-finales/informe-sqa-hu02.md','06-informes-finales/informe-sqa-general.md']
body=f'''# Actividad: Aplicando SQA en nuestras historias de usuario

Proyecto StockFácil. Elaboración: {DATE}. Este paquete contiene fuentes Markdown completas y evidencia ejecutada; sus revisiones, inspecciones y auditorías son técnicas preliminares, pendientes de validación por los equipos y el docente.

## Entrega al docente

Entrega los dos informes por historia y el consolidado, acompañados del paquete docs/sqa con matrices, checklists, actas, logs JUnit y capturas. Las versiones PDF se generan en output/pdf desde las fuentes Markdown. El archivo ZIP de entrega reúne la documentación y esas versiones, sin incluir la base de desarrollo, .env ni credenciales privadas.

'''
body+='\n'.join('- '+doc(path,item,item) for item in expected)+'\n'
body+='\n## Versiones finales\n\n'
for name, label in [('informe-sqa-hu01', 'PDF de HU-01'), ('informe-sqa-hu02', 'PDF de HU-02'), ('informe-sqa-general', 'PDF consolidado')]:
    body+='- '+link(path, 'output/pdf/'+name+'.pdf', label)+'.\n'
body+='- '+link(path, 'output/stockfacil-sqa-entrega.zip', 'Paquete de entrega: documentos, PDF, evidencia y fuentes del proyecto')+'.\n'
body+='''
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
'''
write(path,body)
assert all((SQA/item).is_file() for item in expected)
print('Generados 21 documentos Markdown, 12 CA trazados y tres informes finales.')
