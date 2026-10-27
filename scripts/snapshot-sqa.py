"""Registra integridad sin copiar datos privados ni valores de .env."""
import hashlib
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]
database = root / 'database/database.sqlite'
snapshot = {'recorded_at_utc': datetime.now(timezone.utc).isoformat()}
snapshot['env_sha256'] = hashlib.sha256((root / '.env').read_bytes()).hexdigest()
with sqlite3.connect(database.as_uri() + '?mode=ro', uri=True) as connection:
    logical = '\n'.join(connection.iterdump()).encode('utf-8')
    snapshot['database_logical_sha256'] = hashlib.sha256(logical).hexdigest()
    snapshot['counts'] = {table: connection.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
                          for table in ['users', 'products', 'movements', 'categories']}
destination = root / 'docs/evidencias' / f'integridad-{sys.argv[1]}.json'
destination.write_text(json.dumps(snapshot, indent=2), encoding='utf-8')
print(destination.name, 'registrado sin exportar datos')
