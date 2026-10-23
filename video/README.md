# Setup demonstration

`setup_demo.mp4` records actual commands executed on this machine using OBS Studio. It uses on-screen captions and has no audio track.

The recording checks Python, creates a separate virtual environment, installs the requirements and the local Validators snapshot, then runs the smoke, ordered full and two-worker full suites. The temporary environment is under `tmp/setup-venv`; the ordinary setup commands are in the main README.

To repeat the captioned demonstration, run `python scripts/setup_demo.py` with a system Python that includes Tkinter, then record the displayed window with OBS. Press Escape to close the demonstration window after it finishes. The script executes real subprocesses and displays their output; it does not replay saved test results.
