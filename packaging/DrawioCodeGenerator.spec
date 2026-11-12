import os
import sys

from PyInstaller.utils.hooks import collect_all


wx_datas, wx_binaries, wx_hiddenimports = collect_all("wx")
project_root = os.path.abspath(os.path.join(SPECPATH, os.pardir))

a = Analysis(
    [os.path.join(project_root, "main.py")],
    pathex=[project_root],
    binaries=wx_binaries,
    datas=wx_datas + [
        (os.path.join(project_root, "ui", "assets"), "ui/assets"),
        (os.path.join(project_root, "examples"), "examples"),
    ],
    hiddenimports=wx_hiddenimports,
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
    [],
    exclude_binaries=True,
    name="DrawioCodeGenerator",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(project_root, "packaging", "app-icon.ico") if sys.platform == "win32" else None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="DrawioCodeGenerator",
)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="DrawioCodeGenerator.app",
        icon=os.path.join(project_root, "packaging", "app-icon.icns"),
        bundle_identifier="org.addy.drawio.codegen",
    )
