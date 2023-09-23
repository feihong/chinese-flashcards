import subprocess
from pathlib import Path

content_dir = Path('content')

cmd = [
  'ghp-import',
  '--no-jekyll',
  '--push',
  '--no-history',
  content_dir
]
subprocess.run(cmd)

print(f'Deployed to https://feihong.github.io/chinese-flashcards/')
