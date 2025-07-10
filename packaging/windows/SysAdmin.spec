# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

a = Analysis([
    'app_new_ui.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('commands.json', 'commands.json'),
        ('favorites.json', 'favorites.json'),
        ('plugins', 'plugins'),
        ('models', 'models'),
        ('db', 'db'),
        ('logs', 'logs'),
        ('data', 'data')
    ],
    hiddenimports=collect_submodules('plugins'),
    hookspath=[],
    runtime_hooks=[],
    excludes=['tkinter', 'tests', 'unittest', 'email', 'http', 'xml', 'xmlrpc', 'asyncio'],
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
          name='SysAdminAssistant',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='icon.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='SysAdminAssistant')

