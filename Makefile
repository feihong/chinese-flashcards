install:
	pip install --requirement requirements.txt

anki:
	QTWEBENGINE_REMOTE_DEBUGGING=8080 open -a Anki

download_svg:
	git clone --depth 1 git@github.com:skishore/makemeahanzi

publish:
	python publish.py

serve:
	python -m http.server
