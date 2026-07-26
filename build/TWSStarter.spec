# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

PROJ_ROOT = Path(SPECPATH).parent
SRC_ROOT  = PROJ_ROOT / 'src'

a = Analysis(
    [str(SRC_ROOT / 'twsstarter' / 'main.py')],
    pathex=[str(SRC_ROOT)],
    binaries=[],
    datas=[],
    hiddenimports=[
        'twsstarter',
        'twsstarter.i18n',
        'twsstarter.i18n.strings',
        'twsstarter.resources',
        'twsstarter.resources.icon',
        'twsstarter.resources.flags',
        'twsstarter.resources.help_images',
        'twsstarter.ui',
        'twsstarter.ui.theme',
        'twsstarter.ui.main_window',
        'twsstarter.ui.connection_card',
        'twsstarter.ui.connection_dialog',
        'twsstarter.ui.disclaimer_dialog',
        'twsstarter.ui.settings_dialog',
        'twsstarter.ui.about_dialog',
        'twsstarter.ui.help_dialog',
        'twsstarter.ui.help_browser',
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'cryptography',
        'cryptography.fernet',
        'cryptography.hazmat.primitives',
        'cryptography.hazmat.primitives.hashes',
        'cryptography.hazmat.primitives.kdf.pbkdf2',
        'cryptography.hazmat.backends',
        'cryptography.hazmat.backends.openssl',
        'win32gui',
        'win32con',
        'win32api',
        'win32clipboard',
        'win32process',
        'pywintypes',
        'pywinauto',
        'pyautogui',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'pandas', 'scipy'],
    noarchive=False,
    optimize=1,
)

pyz = PYZ(a.pure)

# One-dir build (not one-file): the app runs from its own folder, so there is
# no per-run _MEI temp extraction/cleanup. This avoids the Windows "Failed to
# remove temporary directory" warning on exit (a lingering worker thread could
# hold a file in _MEI) and makes startup faster. The Inno Setup installer bundles
# the whole dist/TWSStarter/ folder.
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TWSStarter',
    icon=str(PROJ_ROOT / 'build' / 'TWSStarter.ico'),
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TWSStarter',
)
