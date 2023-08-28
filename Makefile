install:
	pip install --requirement requirements.txt

install_anki:
	python -m venv pyenv && pyenv/bin/pip install --upgrade pip && pyenv/bin/pip install --upgrade --pre 'aqt[qt6]'

anki:
	QTWEBENGINE_REMOTE_DEBUGGING=8080 pyenv/bin/anki

download_svg:
	git clone --depth 1 git@github.com:skishore/makemeahanzi

publish:
	python publish.py

serve:
	python -m http.server
