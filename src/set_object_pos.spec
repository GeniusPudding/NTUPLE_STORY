from kivy.deps import sdl2, glew
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal,hookspath
from PyInstaller.utils.hooks import collect_submodules
block_cipher = None

excludekivy = get_deps_minimal(video=None, window=True, audio=['gstplayer', 'ffpyplayer', 'sdl2'], spelling='enchant',camera=None)['excludes']
a = Analysis(['object_allocator.py'],
             pathex=['C:\\Users\\user\\Desktop\\NTUPLE_STORY\\src'],
             binaries=[],
             datas=[],
             hiddenimports=(collect_submodules('kivy')+collect_submodules('kivy.garden')+collect_submodules('pygame')),
             hookspath=[],
             runtime_hooks=[],
             excludes=excludekivy,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='object',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True, 
          icon= 'C:\\Users\\user\\Desktop\\NTUPLE_STORY\\src\\China.ico')
