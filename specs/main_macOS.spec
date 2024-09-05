# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../src/main.py'],  # Path to the main.py script
    pathex=['..'],  # Ensure the path is correct relative to the spec file
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    cipher=block_cipher,
    optimize=2,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,  # Ensure binaries are included
    name='ExerciseDashboard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

app = BUNDLE(
    exe,  # EXE instance passed here
    name='ExerciseDashboard.app',
    icon=None,
    bundle_identifier=None,
)

coll = COLLECT(
    app,  # BUNDLE instance passed here
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='ExerciseDashboard_macOS',
)