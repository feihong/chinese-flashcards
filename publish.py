import subprocess
import shutil
from pathlib import Path
import urllib.parse

output_dir = Path('public')
if not output_dir.exists():
  output_dir.mkdir()

shutil.copy('content/bookmarklet.html', output_dir)
shutil.copy('content/asciimath-playground.html', output_dir)

js = 'javascript:' + urllib.parse.quote(Path('content/asciimath-preview.js').read_text().strip())

html = f"""\
<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8" >
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AnkiWeb AsciiMath Preview Bookmarklet</title>
</head>
<body>
<h1>AnkiWeb AsciiMath Preview Bookmarklet</h1>

<a href="{js}">AsciiMath preview</a>
</body>
</html>
"""

Path(output_dir / 'index.html').write_text(html)

cmd = [
  'ghp-import',
  '--no-jekyll',
  '--push',
  '--no-history',
  output_dir]
subprocess.run(cmd)

print(f'Deployed to https://feihong.github.io/chinese-flashcards/')
