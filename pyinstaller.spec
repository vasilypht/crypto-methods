# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

datas = [
    ("app/gui", "gui"),
    ("app/crypto", "crypto"),
    ("app/resources", "resources")
]
    
hiddenimports = [
    "scipy",
    "numpy",
    "sympy",
    "pyqtgraph",
    "pyqtgraph.graphicsItems.ViewBox.axisCtrlTemplate_pyqt6",
    "pyqtgraph.graphicsItems.PlotItem.plotConfigTemplate_pyqt6",
    "pyqtgraph.imageview.ImageViewTemplate_pyqt6"
]

a = Analysis(['app\\__main__.py'],
             pathex=[],
             binaries=[],
             datas=datas,
             hiddenimports=hiddenimports,
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='Crypto-methods',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='crypto-methods')
