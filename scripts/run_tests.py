"""Run named suites in serial order or independently on two workers."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SUITES = ('all', 'smoke', 'boundary', 'negative', 'email', 'length', 'ip', 'faizan', 'usman')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite', choices=SUITES, default='all')
    parser.add_argument('--parallel', action='store_true')
    args = parser.parse_args()
    reports = ROOT / 'reports'
    reports.mkdir(exist_ok=True)
    mode = 'parallel' if args.parallel else 'ordered'
    stem = f'latest-{args.suite}-{mode}'
    command = [sys.executable, '-m', 'pytest', '-v', '--json-report',
               f'--json-report-file=reports/{stem}.json',
               f'--junitxml=reports/{stem}.xml']
    if args.suite != 'all':
        command += ['-m', args.suite]
    if args.parallel:
        # xdist schedules groups independently; it cannot promise global order.
        command += ['-n', '2', '--dist', 'loadgroup']
    else:
        command += ['--order-scope=session']
    print('Running:', ' '.join(command), flush=True)
    result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True)
    print(result.stdout, end='')
    (reports / f'{stem}.txt').write_text(result.stdout, encoding='utf-8')
    sys.exit(result.returncode)
