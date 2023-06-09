# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
datas = collect_data_files("dateutil")
#^ this will fail without setting data=datas below! Oops!

block_cipher = None

a = Analysis(
    ['ingest_ics.py'],
    pathex=[],
    binaries=[],
    #datas=[],
    #datas=[('C:/ProgramData/anaconda3/Lib/site-packages/dateutil/zoneinfo','dateutil/zoneinfo')#HORRIBLE timezone bugs otherwise!
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ingest_ics',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ingest_ics',
)
