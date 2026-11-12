import sys

from PyInstaller.utils.hooks import collect_all


wx_datas, wx_binaries, wx_hiddenimports = collect_all("wx")

a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=wx_binaries,
    datas=wx_datas + [
        ("ui/assets", "ui/assets"),
        ("examples", "examples"),
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
    icon="packaging/app-icon.ico" if sys.platform == "win32" else None,
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
        icon="packaging/app-icon.icns",
        bundle_identifier="org.addy.drawio.codegen",
    )
