# Publicación y revisión en GitHub

Repositorio proporcionado por Andre: https://github.com/AndreRCRO/StockFacil.
La carpeta no tenía Git. Se inició el 27 de octubre de 2026 con identidad configurada AndreRCRO y se publicaron main y test/sqa-kanban. El historial previo del sistema se conserva como archivos históricos, sin atribuirles commits retrospectivos. Los cambios SQA se conservan en la rama para revisión. No se agregó ninguna cuenta o colaborador.

## Issues preparados

`docs/Kanban_Tareas.csv` contiene título, descripción, responsable propuesto, prioridad, estado, aceptación y evidencias. Es la fuente local de tareas; no demuestra que existan Issues remotos. El CSV se puede abrir en Excel y usar para crear tarjetas; no se presupone una importación nativa de CSV en GitHub Projects.

Para publicarlos con GitHub CLI:

1. Instala GitHub CLI desde https://cli.github.com.
2. Abre una terminal en la raíz de StockFácil.
3. Ejecuta `gh auth login` y completa personalmente el inicio de sesión con tu cuenta.
4. Ejecuta `powershell -File scripts/publicar-issues.ps1`.
5. Abre **Issues** del repositorio y confirma los títulos K-01 a K-11. El script evita duplicados por título.

El script no agrega colaboradores ni asigna identidades desconocidas. Escribe los responsables propuestos en cada descripción. Andre puede asignarse a @AndreRCRO; la asignación de Santiago requiere su usuario real y su acceso autorizado. No se consultan ni exportan almacenes de credenciales.

## Crear el tablero con cinco estados

1. Abre https://github.com/AndreRCRO?tab=projects.
2. Selecciona **New project**, elige **Board** y escribe **StockFácil SQA Kanban**.
3. En la configuración del campo **Status**, conserva exactamente **Pendiente**, **En desarrollo**, **En pruebas**, **En corrección** y **Terminado**.
4. En **Add item**, selecciona los Issues de AndreRCRO/StockFacil.
5. Ubica cada Issue según la columna Estado del CSV. Si falta la revisión del compañero, conserva **En pruebas**.
6. En la descripción de la vista registra **WIP máximo 2 en En desarrollo**. Comprueba el límite durante cada revisión del tablero.
7. Desde **Projects** del repositorio, vincula el proyecto creado. Copia la URL en el Test Plan y guarda una captura real en docs/evidencias.

Los nombres de algunos controles dependen del idioma de GitHub. Si Projects solicita permisos nuevos de la cuenta, el titular los decide personalmente.

## Pull Request preparado

1. Abre https://github.com/AndreRCRO/StockFacil/compare/main...test/sqa-kanban?expand=1.
2. Confirma base **main** y compare **test/sqa-kanban**.
3. Usa el título **Incorporar plan SQA Kanban y pruebas verificables**.
4. Copia el texto de `docs/Pull_Request_SQA.md` en la descripción y reemplaza K-xx por los números reales de Issues cuando existan.
5. Selecciona **Create draft pull request**. Solicita la revisión real de Santiago desde su cuenta.
6. Conserva enlaces y comentarios de revisión. No autoapruebes en nombre del compañero.

No se declara un PR creado hasta disponer de su URL. main se conserva como base y se integra por PR cuando el equipo lo revise.

## Comprobar GitHub Actions

Ejecución ya verificada: https://github.com/AndreRCRO/StockFacil/actions/runs/40573040837, commit cf285bf, conclusión success. Los pasos PHPUnit, Selenium con Chrome y Cypress aprobaron y se publicó evidencias-sqa-1. La API pública se conserva en docs/evidencias/github-actions*.json.

1. Entra en **Actions** del repositorio después de subir la rama.
2. Abre **Pruebas StockFacil** y selecciona el commit SQA más reciente.
3. Comprueba los pasos PHPUnit, Selenium y Cypress. Descarga **evidencias-sqa-N**.
4. Si no inicia por restricciones de la cuenta, revisa **Settings → Actions → General** como titular. No necesitas secretos para este workflow.
5. Guarda la URL de la ejecución y su resultado real en `docs/Resultados_Pruebas.md`.

El workflow se activa por push, pull_request y workflow_dispatch, instala PHP 8.3 y Node 24, compila Vite y usa SQLite aislado. El resultado local no se presenta como resultado remoto.

## Demostrar participación real

Andre y Santiago realizan sus cambios desde sus propias cuentas e identidades Git. Santiago revisa el PR y puede registrar el resultado manual de la exploración antes de la entrega; Andre revisa esos cambios. Conservar comentarios, commits y capturas reales. La asignación propuesta de tareas y las pruebas asistidas no prueban por sí solas participación de ambos.
