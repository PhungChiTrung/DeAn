# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Process.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\1_hoc_tap\\python\\QuanLyThuVien\\\\books.json', '.'), ('D:\\1_hoc_tap\\python\\QuanLyThuVien\\\\users.json', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Process',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
