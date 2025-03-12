help:
	just --list

install:
	pip install --requirement requirements.txt

anki:
	QTWEBENGINE_REMOTE_DEBUGGING=8080 open -a Anki

download_svg:
	git clone --depth 1 git@github.com:skishore/makemeahanzi

serve:
	python -m http.server

build:
	python build.py

clean:
	rm -rf _build/*

update: build
	python update_anki.py

count:
	python count_unique_hanzi.py

sloppy:
  python list_sloppy_cards.py

story:
	python generate_story_prompt.py

sentence:
  python generate_sentences_prompt.py
