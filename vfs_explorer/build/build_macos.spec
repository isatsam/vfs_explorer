# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['../../vfs_explorer.py'],
    pathex=[],
    binaries=[],
    datas=[('../../COPYING', '.'), ('../../README.md', '.'),
        ('../../screenshot_1.0.png', '.'),
        ('../languages/*.qm', 'languages')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VFS Explorer',
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
    contents_directory='vfs_explorer',
    icon="icon.ico"
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='vfs_explorer',
)

app = BUNDLE(exe,
         name='VFS Explorer.app',
         icon="icon.icns",
         bundle_identifier=None,
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
            },
)
