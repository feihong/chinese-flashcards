import shutil
from pathlib import Path

download_dir = Path('~/Downloads').expanduser()

HERE = Path(__file__).parent
test_dir = HERE / '_test'
if not test_dir.exists():
    test_dir.mkdir()

try:
    listening_file = next(download_dir.glob('*_Listening.mp3'))
    shutil.move(listening_file, test_dir / 'listening.mp3')
except:
    print('Listening file not found')

try:
    questions_file = next(download_dir.glob('*_Real Test Questions.pdf'))
    shutil.move(questions_file, test_dir / 'questions.pdf')
except:
    print('Questions file not found')

INDEX_HTML = """\
<!doctype html>
<html>
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HSK Mock Exam</title>
</head>
<body>
    <a href="questions.pdf">Questions PDF</a>
    <div>
        <audio controls src="listening.mp3" style="width: 100%">
    </div>
</body>
</html>
"""

with (test_dir / 'index.html').open('w') as fp:
    fp.write(INDEX_HTML)
