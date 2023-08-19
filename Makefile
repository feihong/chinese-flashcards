install:
	pip install --requirement requirements.txt

download_svg:
	git clone --depth 1 git@github.com:skishore/makemeahanzi

publish:
	python publish.py

serve:
	python -m http.server
