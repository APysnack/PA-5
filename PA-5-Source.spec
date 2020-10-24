# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['PA-5-Source.py'],
             pathex=['C:\\Users\\purle\\PycharmProjects\\PA-5'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
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
 	  [('W ignore', None, 'OPTION')],
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='PA-5-Source',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
