from pathlib import Path
import db
import re

words_file = Path('words.txt')
word_cards_file = Path('cards.txt')
examples_file = Path('examples.txt')
example_cards_file = Path('example-cards.txt')

WORDS_HEADER = """\
#separator:semicolon
#html:true
#notetype column: 1
#columns:notetype;Front;Back;pinyin;gloss
"""

EXAMPLES_HEADER = """\
#separator:semicolon
#html:true
#notetype column: 1
#columns:notetype;text
"""

def get_words():
  with words_file.open('r', encoding='utf8') as fp:
    for line in fp:
      yield line.strip()

def get_word_card_lines():
  for entry in db.get_entries_for_words(get_words()):
    pinyin = entry.pinyin.replace(' ', '').replace('5', '')
    yield ';'.join(('Chinese', entry.simp, '', pinyin, entry.gloss))

def generate_word_cards():
  with word_cards_file.open('a', encoding='utf8') as fp:
    fp.write(WORDS_HEADER)
    for line in get_word_card_lines():
      fp.write(line + '\n')
  print(f'Generated {word_cards_file}')

class Replacer:
  def __init__(self):
    self.num = 0

  def __call__(self, match):
    self.num += 1
    return '{{c%d::%s}}' % (self.num, match.group(1))

def get_examples():
  with examples_file.open('r', encoding='utf8') as fp:
    for line in fp:
      line = re.sub(r'\{(.*)\}', Replacer(), line.strip())
      yield line

def generate_example_cards():
  with example_cards_file.open('w', encoding='utf8') as fp:
    fp.write(EXAMPLES_HEADER)
    for line in get_examples():
      fp.write(f'Chinese Cloze;{line}\n')
  print(f'Generated {example_cards_file}')

if __name__ == '__main__':
  generate_word_cards()

  # generate_example_cards()
