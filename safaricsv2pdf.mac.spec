# -*- mode: python -*-
import os

block_cipher = None
workdir = os.getcwd()
libdir = os.path.join(workdir, 'lib')

a = Analysis(['safaricsv2pdf.py'],
             pathex=[workdir],
             binaries=None,
             datas=[(libdir, 'lib')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='SafariCSV2PDF',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='safaricsv2pdf.icns')
