set dotenv-load := true

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
	uv run --env-file .env build.py

clean:
	rm -rf _build/*

# Update templates for custom Anki note types
update: build
	uv run update_anki.py

# Dump Anki-Connect API output to result.json
api_info:
    uv run api_info.py

story:
	python generate_story_prompt.py

sentence:
	python generate_sentences_prompt.py

examples:
	python check_test_examples.py

explore:
    uv run anki_connect_explorer.py

# Generate Anki practice stats report
report:
	uv run --env-file .env generate_report.py

# Upload report to your server
publish_report: report
    rsync -avz index.html $SERVER_DIR

publish_static:
    rsync -avz quiz-prompt.html $SERVER_DIR

publish_test:
    python generate_test_directory.py
    rsync -avz _test/* $SERVER_DIR/test
