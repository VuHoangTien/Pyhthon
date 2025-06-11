# login_app.spec
# -*- mode: python ; coding: utf-8 -*-

import os
block_cipher = None

a = Analysis(
    ['GUI_LogIn.py'],
    pathex=[os.path.abspath('.')],  # thêm đường dẫn hiện tại
    binaries=[],
    datas=[
        ('background_form_login.png', '.'),    # ảnh nền
        ('google_icon-icons.com_62736.ico', '.'),  # icon gmail
        ('final_model.pkl', '.'),         # thêm mô hình chính
        ('scaler.pkl', '.'),
        ('nurst.png', '.'),
    ],
    hiddenimports=['sklearn', 'sklearn.ensemble'],
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
    name='Nhiem_trung_huyet_v20',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='icon1_exe.ico' 
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='sepsis'
)
