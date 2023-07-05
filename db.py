import sys
import os
import gzip
import re
from dataclasses import dataclass
from pathlib import Path
import sqlite3

input_file = 'cedict.txt.gz'
db_file = Path('cedict.sqlite3')

@dataclass
class Entry:
  trad: str
  simp: str
  pinyin: str
  gloss: str

def get_entries():
    """
    Return a sequence of dictionary items.
    """
    with gzip.open(input_file, mode='rt', encoding='utf8') as fp:
      for line in fp:
        if not '[' in line:
          continue

        if match := re.match(r'(\w+) (\w+) \[(.*)\] \/(.*)\/', line):
          yield Entry(*match.groups())

def get_tuples():
   for entry in get_entries():
      print(entry)
      yield entry.simp, entry.pinyin, entry.gloss

def get_entries_for_words(words):
   with sqlite3.connect(db_file) as conn:
    for word in words:
      res = conn.execute('SELECT simp, pinyin, gloss FROM entries where simp = ?', (word,))
      row = res.fetchone()
      if row is not None:
        yield Entry(simp=row[0], trad=None, pinyin=row[1], gloss=row[2])

if __name__ == '__main__':
  if db_file.exists():
    os.remove(db_file)

  with sqlite3.connect(db_file) as con:
    con.execute('CREATE TABLE entries (simp TEXT, pinyin TEXT, gloss TEXT);')
    con.executemany('INSERT INTO entries VALUES(?, ?, ?)', get_tuples())
    con.commit()
