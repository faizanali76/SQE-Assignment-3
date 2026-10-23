"""Show real setup commands and their output for a captioned screen recording.

Run with a system Python that includes Tk. Creates an isolated tmp/setup-venv.
"""
from pathlib import Path
import queue
import subprocess
import sys
import threading
import time
import tkinter as tk

ROOT = Path(__file__).resolve().parents[1]
events = queue.Queue()
root = tk.Tk()
root.title('SQE Assignment 3 - Validators setup demonstration')
root.configure(bg='#F5F3ED')
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.bind('<Escape>', lambda e: root.destroy())
tk.Label(root, text='SQE Assignment 3  |  Validators', bg='#F5F3ED', fg='#202020',
         font=('Arial', 24, 'bold')).pack(anchor='w', padx=36, pady=(24, 8))
caption = tk.StringVar(value='Faizan and Usman - environment setup and unit test execution')
tk.Label(root, textvariable=caption, bg='#F5F3ED', fg='#333333',
         font=('Arial', 16), wraplength=1450, justify='left').pack(anchor='w', padx=36, pady=8)
text = tk.Text(root, bg='#171B1D', fg='#EDEDE8', font=('Consolas', 15),
               wrap='word', padx=20, pady=16, borderwidth=0)
text.pack(fill='both', expand=True, padx=36, pady=(12, 28))
text.insert('end', 'Python project: python-validators/validators\nPinned source: 22786cc6e7283a0fa452c179797e447f798db9f0\n\n'
            'Scope: email, length and ip_address (IPv4 + IPv6)\n80 CSV-driven cases. No network services required.\n\n'
            'This recording shows commands actually executed on this machine.\nThe temporary environment is created separately from the working environment.\n')


def run(command, label):
    events.put(('caption', label))
    events.put(('clear', None))
    visible = 'python' if command[0] == sys.executable else 'demo-venv/python'
    events.put(('line', '$ ' + ' '.join([visible, *command[1:]]) + '\n\n'))
    time.sleep(3)
    with subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True,
                          encoding='utf-8', errors='replace') as process:
        for line in process.stdout:
            # Keep the display readable, including pip's detailed output.
            events.put(('line', line))
            time.sleep(0.05)
    events.put(('line', f'\nExit code: {process.returncode}\n'))
    if process.returncode:
        raise RuntimeError('Command failed; see output')
    time.sleep(5)


def demonstrate():
    try:
        (ROOT / 'tmp/demo-start.txt').write_text(str(time.time()), encoding='utf-8')
        time.sleep(10)
        run([sys.executable, '--version'], '1. Check Python. This project requires Python 3.11 or later.')
        run([sys.executable, '-m', 'venv', 'tmp/setup-venv'], '2. Create a separate virtual environment.')
        executable = str(ROOT / ('tmp/setup-venv/Scripts/python.exe' if sys.platform == 'win32' else 'tmp/setup-venv/bin/python'))
        run([executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            '3. Install the pinned test tools and the local, unchanged Validators source.')
        run([executable, '-m', 'pytest', '-m', 'smoke', '-v'],
            '4. Run the smoke group. Eight CSV rows cover one valid and one invalid input per function.')
        run([executable, 'scripts/run_tests.py'],
            '5. Run all cases in order: email, length, IPv4, then IPv6.')
        run([executable, 'scripts/run_tests.py', '--parallel'],
            '6. Run all cases on two workers. Parallel completion order is intentionally unrestricted.')
        events.put(('clear', None))
        events.put(('caption', 'Setup and execution finished. Each command above completed successfully.'))
        events.put(('line', 'The CSV contains 80 cases across three modules and four public functions.\n\n'
                    'Use --suite boundary for BVA cases.\nUse --suite negative for invalid-input cases.\n'
                    'Use --suite faizan or --suite usman for the allocated review blocks.\n\n'
                    'Serial run: fixed function-group order.\nParallel run: two independent worker processes.\n\n'
                    'Excel register: outputs/submission/Test_Cases.xlsx\n'
                    'Report: output/pdf/Summary_Report.pdf\n'
                    'Design notes: docs/test_design.md\n\n'
                    'Recording: OBS Studio. On-screen captions; no spoken narration.\n'))
        (ROOT / 'tmp/demo-complete.txt').write_text('success', encoding='utf-8')
    except Exception as exc:
        events.put(('line', str(exc)))
        (ROOT / 'tmp/demo-complete.txt').write_text('failed', encoding='utf-8')


def poll():
    while not events.empty():
        kind, value = events.get()
        if kind == 'caption':
            caption.set(value)
        elif kind == 'clear':
            text.delete('1.0', 'end')
        else:
            text.insert('end', value)
            text.see('end')
    root.after(100, poll)


if __name__ == '__main__':
    threading.Thread(target=demonstrate, daemon=True).start()
    poll()
    root.mainloop()
