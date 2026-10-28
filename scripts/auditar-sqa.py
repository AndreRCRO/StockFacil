"""Comprueba evidencia, integridad y secretos reconocibles sin imprimir valores."""
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]
evidence = root / 'docs/evidencias'
before = json.loads((evidence / 'integridad-antes.json').read_text())
after = json.loads((evidence / 'integridad-despues.json').read_text())
patterns = {
    'private_key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'github_token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b'),
    'aws_access_key': re.compile(r'\bAKIA[A-Z0-9]{16}\b'),
    'openai_key': re.compile(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{40,}\b'),
}
tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode('utf-8').split('\0')
additional = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard', '-z'], cwd=root).decode('utf-8').split('\0')
files = sorted(set(x for x in tracked + additional if x))
findings = []
scanned = 0
for name in files:
    path = root / name
    if not path.is_file() or path.suffix.lower() in {'.png', '.jpg', '.docx', '.pdf', '.zip', '.ico'}:
        continue
    try:
        source = path.read_text(encoding='utf-8-sig')
    except UnicodeDecodeError:
        continue
    scanned += 1
    for kind, pattern in patterns.items():
        if pattern.search(source):
            findings.append({'file': name, 'kind': kind})
ignored = {name: subprocess.run(['git', 'check-ignore', '--quiet', name], cwd=root).returncode == 0
           for name in ['.env', 'database/database.sqlite', 'tmp/sqa-e2e/prueba.sqlite']}
result = {
    'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
    'env_unchanged': before['env_sha256'] == after['env_sha256'],
    'database_unchanged': before['database_logical_sha256'] == after['database_logical_sha256'],
    'sensitive_paths_ignored': ignored, 'text_files_scanned': scanned,
    'secret_pattern_findings': findings,
    'limitation': 'Búsqueda de patrones conocidos; no demuestra ausencia absoluta de secretos ni auditoría de seguridad exhaustiva.',
}
(evidence / 'auditoria-verificacion.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
manifest = {str(path.relative_to(root)).replace('\\', '/'): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(evidence.rglob('*')) if path.is_file() and path.name != 'manifiesto-sha256.json'}
(evidence / 'manifiesto-sha256.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
assert result['env_unchanged'] and result['database_unchanged']
assert all(ignored.values()) and not findings
