"""Save compact measured results without machine-specific pytest metadata."""
import csv
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import platform

ROOT = Path(__file__).resolve().parents[1]

if __name__ == '__main__':
    runs = []
    for filename in sorted((ROOT / 'reports').glob('latest-*.json')):
        report = json.loads(filename.read_text(encoding='utf-8'))
        runs.append({'run': filename.stem.removeprefix('latest-'),
                     'exitcode': report['exitcode'], 'duration_seconds': round(report['duration'], 3),
                     'summary': report['summary'],
                     'cases': [{'id': t['nodeid'].split('[')[-1].rstrip(']'),
                                'outcome': t['outcome']} for t in report['tests']]})
    coverage = json.loads((ROOT / 'tmp/coverage.json').read_text(encoding='utf-8'))
    selected = {Path(k).name: v['summary'] for k, v in coverage['files'].items()
                if Path(k).name in ('email.py', 'length.py', 'ip_address.py')}
    evidence = {'recorded_at': datetime.now(timezone(timedelta(hours=5))).isoformat(),
                'python': platform.python_version(), 'platform': platform.system(),
                'upstream_commit': '22786cc6e7283a0fa452c179797e447f798db9f0',
                'runs': runs, 'selected_module_statement_coverage': selected}
    (ROOT / 'reports/verification.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
    with (ROOT / 'data/validation_cases.csv').open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
    ordered = next(r for r in runs if r['run'] == 'all-ordered')
    actual = {r['id']: r['outcome'] for r in ordered['cases']}
    for row in rows:
        row['status'] = actual[row['id']]
    (ROOT / 'tmp/cases.json').write_text(json.dumps(rows, ensure_ascii=False), encoding='utf-8')
    print([(r['run'], r['summary']) for r in runs])
