from pathlib import Path
import db

words_file = Path('words.txt')
word_cards_file = Path('cards.txt')

def get_words():
  with words_file.open('r', encoding='utf8') as fp:
    for line in fp:
      yield line.strip()

def get_word_card_lines():
  for entry in db.get_entries_for_words(get_words()):
    pinyin = entry.pinyin.replace(' ', '').replace('5', '')
    yield ';'.join((
      'Chinese',
      entry.simp,
      '',  # Back is always empty
      pinyin,
      entry.gloss))

def generate_word_cards():
  with word_cards_file.open('a', encoding='utf8') as fp:
    for line in get_word_card_lines():
      fp.write(line + '\n')
  print(f'Generated {word_cards_file}')

if __name__ == '__main__':
  generate_word_cards()
