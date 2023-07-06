download:
	curl -o cedict.txt.gz https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.txt.gz

download_svg:
	git clone --depth 1 git@github.com:skishore/makemeahanzi

db:
	python db.py

cards:
	python generate-cards.py
