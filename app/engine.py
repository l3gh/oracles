"""Adapter for the supplied detector. No console or terminal interaction."""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def resources():
    return Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[1])) / 'original'


def input_devices():
    import sounddevice as sd
    # Legacy detector uses PortAudio host API 0 (MME), with global device IDs.
    devices = sd.query_devices()
    return [(i, d['name']) for i, d in enumerate(devices)
            if d['hostapi'] == 0 and d['max_input_channels'] > 0]


class Engine:
    def __init__(self, source=None):
        self.source = Path(source) if source else resources()
        self.process = None
        self.folder = None
        self.log = None

    def start(self, encounter, device):
        if encounter not in ('templar', 'atheon'):
            raise ValueError('Choose Templar or Atheon.')
        if not isinstance(device, int) or device < 0:
            raise ValueError('Choose an audio input.')
        if self.process is not None:
            raise RuntimeError('Stop the current session first.')
        if not (self.source / 'prophet.exe').is_file():
            raise FileNotFoundError('The bundled Prophet detector is missing.')
        self.folder = Path(tempfile.mkdtemp(prefix='oracles-'))
        try:
            shutil.copytree(self.source / 'samples', self.folder / 'samples')
            for name in ('templar.json', 'atheon.json'):
                shutil.copy2(self.source / name, self.folder / name)
            (self.folder / 'device.txt').write_text(str(device), encoding='ascii')
            self.log = open(self.folder / 'detector.log', 'w+b')
            # A frozen parent must not pass its PyInstaller extraction identity
            # to this independently frozen legacy application.
            env = {k: v for k, v in os.environ.items()
                   if not k.startswith('_PYI') and k != '_MEIPASS2'}
            self.process = subprocess.Popen(
                [str(self.source / 'prophet.exe')], cwd=self.folder,
                stdin=subprocess.PIPE, stdout=self.log, stderr=self.log,
                creationflags=subprocess.CREATE_NO_WINDOW, env=env)
            self.process.stdin.write((encounter + '\n').encode('ascii'))
            self.process.stdin.close()
        except Exception:
            self.stop()
            raise

    def sequence(self):
        if self.folder is None:
            return []
        try:
            text = (self.folder / 'sequence.txt').read_text().strip()
            parts = text.split('-')
            return parts if parts and all(p in '1234567' and len(p) == 1 for p in parts) else []
        except (OSError, UnicodeError):
            return []

    def error(self):
        if self.folder is None:
            return ''
        try:
            return (self.folder / 'detector.log').read_text(errors='replace')[-4000:]
        except OSError:
            return ''

    def stop(self):
        if self.process is not None:
            # The legacy one-file executable has a bootloader AND child process.
            if self.process.poll() is None:
                subprocess.run(['taskkill', '/PID', str(self.process.pid), '/T', '/F'],
                               capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.process.wait(timeout=10)
            self.process = None
        if self.log:
            self.log.close()
            self.log = None
        if self.folder:
            shutil.rmtree(self.folder, ignore_errors=True)
            self.folder = None
