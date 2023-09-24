"""
Copy files from src to _build

And add secrets to one particular file
"""
from pathlib import Path
import shutil
import secrets

here = Path(__file__).parent
src_dir = here / 'src'
build_dir = here / '_build'

if build_dir.exists():
  shutil.rmtree(build_dir)
build_dir.mkdir()

for dir in src_dir.iterdir():
  if dir.is_dir():
    dst_dir = build_dir / dir.name
    print(f'Copying {dir} to {dst_dir}')
    shutil.copytree(dir, dst_dir)

file = build_dir / 'Chinese/pinyin to handwriting/back.html'
new_text = file.read_text().replace('YOUR-SERVER.COM', secrets.server)
file.write_text(new_text)
