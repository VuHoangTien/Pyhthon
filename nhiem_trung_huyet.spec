# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['GUI_LogIn.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Thêm các file ảnh và tài nguyên cần thiết
        ('background_form_login.png', '.'),
        ('google_icon-icons.com_62736.ico', '.'),
        ('nurst.png', '.'),  # Nếu có file GUI_xetnghiem.py
        ('final_model.pkl', '.'),  # Nếu có file model
        ('scaler.pkl', '.'),  # Nếu có file scaler
        # Thêm các file Python khác nếu cần
        ('LogIn_Event.py', '.'),
        ('GUI_xetnghiem.py', '.'),  # Nếu có
    ],
    hiddenimports=[
        # Thêm các module có thể bị thiếu
        'PIL._tkinter_finder',
        'PIL.Image',
        'PIL.ImageTk',
        'PIL.ImageOps',
        'customtkinter',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'joblib',  # Nếu sử dụng trong GUI_xetnghiem.py
        'sklearn.ensemble',  # Nếu sử dụng model sklearn
        'sklearn.preprocessing',
        'sklearn.base',
        'sklearn.utils',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='nhiem_trung_huyet',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Đặt True nếu muốn debug
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon_exe.ico',  # Sửa từ list thành string
)