# Setup file for cx_Freeze.
# Run "python setup.py build".
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [
    "sys",
    "twitter",
    "json",
    "urllib.parse",
    "copy",
    "tkinter",
    "numbers",
    "webbrowser",
], excludes = [], include_msvcr = True, include_files=[
    "gui_classes.py",
    "woeid.py",
    "server_code.py",
])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('tabs.py', base=base, targetName = 'tabs.exe')
]

setup(name='tabs',
      version = '1.0',
      options = dict(build_exe = buildOptions),
      executables = executables)
