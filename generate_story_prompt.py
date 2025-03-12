"""
Generate an AI prompt to compose a short story containing words from gloss cards practiced within the past week.
"""
import requests

def invoke(action, **params):
  data = {'action': action, 'version': 6}
  if params:
    data['params'] = params
  r = requests.post('http://127.0.0.1:8765', json=data)
  return r.json()

def get_cards():
  card_ids = invoke('findCards', query='note:Chinese card:4 rated:7')['result']
  print(f'Found {len(card_ids)} Chinese gloss cards studied within the last week')
  return invoke('cardsInfo', cards=card_ids)['result']

cards = sorted(get_cards(), key=lambda c: c['interval'])
words = [c['fields']['Front']['value'] for c in cards]

print(f'\nUse this word list to compose a short story in Chinese: {", ".join(words)}. It is OK to use words not in the list if it makes the story more coherent. The reading level should be about HSK level 1. If a word from the list is not in HSK level 1, it should still be used.')
