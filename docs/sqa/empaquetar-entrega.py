"""Crea la entrega académica sin incluir SQLite, .env ni dependencias instaladas."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'docs/sqa/04-pruebas/evidencias'
manifest = [
    {'file': file.name, 'bytes': file.stat().st_size, 'sha256': hashlib.sha256(file.read_bytes()).hexdigest()}
    for file in sorted(EVIDENCE.iterdir())
    if file.is_file() and file.name != 'manifiesto-evidencias.json'
]
(EVIDENCE / 'manifiesto-evidencias.json').write_text(
    json.dumps({'scope': 'Evidencias técnicas originales y posteriores de la actividad', 'files': manifest}, ensure_ascii=False, indent=2),
    encoding='utf-8',
)
files = []
for folder in ['app', 'config', 'routes', 'resources', 'tests', 'lang', 'docs', 'database/migrations', 'database/seeders', 'database/factories']:
    files.extend(file for file in (ROOT / folder).rglob('*') if file.is_file() and file.suffix != '.zip')
for folder in ['bootstrap', 'public']:
    files.extend(file for file in (ROOT / folder).glob('*') if file.is_file())
files.extend((ROOT / 'output/pdf').glob('informe-sqa-*.pdf'))
for name in ['README.md', 'PRODUCT.md', 'DESIGN.md', 'artisan', '.env.example', '.gitignore', 'composer.json', 'composer.lock', 'package.json', 'package-lock.json', 'phpunit.xml', 'vite.config.js']:
    assert (ROOT / name).is_file(), name
    files.append(ROOT / name)
package = ROOT / 'output/stockfacil-sqa-entrega.zip'
with zipfile.ZipFile(package, 'w', zipfile.ZIP_DEFLATED, compresslevel=8) as archive:
    for file in sorted(set(files)):
        relative = file.relative_to(ROOT)
        assert file.name != '.env' and not any(part in ['node_modules', 'vendor'] for part in relative.parts)
        assert not any(extension in file.name for extension in ['.sqlite', '-wal', '-shm'])
        archive.write(file, str(relative).replace('\\', '/'))
with zipfile.ZipFile(package) as archive:
    assert archive.testzip() is None
    names = archive.namelist()
    assert len([name for name in names if name.startswith('docs/sqa/') and name.endswith('.md')]) == 21
    assert len([name for name in names if name.startswith('output/pdf/') and name.endswith('.pdf')]) == 3
print(json.dumps({'package': str(package), 'files': len(names), 'bytes': package.stat().st_size, 'evidence_files': len(manifest), 'sha256': hashlib.sha256(package.read_bytes()).hexdigest()}, ensure_ascii=False))
