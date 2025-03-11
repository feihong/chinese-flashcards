"""
Generate a prompt to feed to an AI to write a story containing cards practiced within the past week.
"""
import itertools
import requests

def invoke(action, **params):
  data = {'action': action, 'version': 6}
  if params:
    data['params'] = params
  r = requests.post('http://127.0.0.1:8765', json=data)
  return r.json()

def get_cards():
  card_ids = invoke('findCards', query='note:Chinese card:5 rated:7')['result']
  print(f'Found {len(card_ids)} Chinese writing cards studied within the last week')
  return invoke('cardsInfo', cards=card_ids)['result']

cards = sorted(get_cards(), key=lambda c: c['interval'])
words = (c['fields']['Front']['value'] for c in cards)
print(f'Generate a short story in Chinese that uses these words: {", ".join(words)}. You are allowed to use words not in the list to make the story more coherent. The reading level should be about HSK level 1. Words in the list that are not at HSK level 1 should still be used.')
