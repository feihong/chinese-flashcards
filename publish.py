import subprocess
import shutil
from pathlib import Path
import urllib.parse

content_dir = Path('content')

output_dir = Path('public')
if not output_dir.exists():
  output_dir.mkdir()

files = ['bookmarklet.html', 'asciimath-playground.html', 'speak-playground.html', 'listen-playground.html',
         'asciimath2latex.js', 'asciimath-preview.js', 'index.html']
for file in files:
  shutil.copy(content_dir / file, output_dir)

cmd = [
  'ghp-import',
  '--no-jekyll',
  '--push',
  '--no-history',
  output_dir]
subprocess.run(cmd)

print(f'Deployed to https://feihong.github.io/chinese-flashcards/')
