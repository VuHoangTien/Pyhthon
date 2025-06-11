# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['GUI_LogIn.py'],
    pathex=[],
    binaries=[],
    datas=[('background_form_login.png', '.'), ('google_icon-icons.com_62736.ico', '.'), ('final_model.pkl', '.'), ('scaler.pkl', '.'), ('patients.json', '.'), ('staffs.json', '.'), ('account.json', '.')],
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
    name='nhiem_trung_huyet_v4',
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
    icon=['icon1_exe.ico'],
)
