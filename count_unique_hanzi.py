"""
Count the number of unique hanzi in Chinese notes
"""
import requests

def invoke(action, **params):
  data = {'action': action, 'version': 6}
  if params:
    data['params'] = params
  r = requests.post('http://127.0.0.1:8765', json=data)
  return r.json()

def get_chinese_notes():
  note_ids = invoke('findNotes', query='note:Chinese')['result']
  print(f'Found {len(note_ids)} Chinese notes')
  return invoke('notesInfo', notes=note_ids)['result']

def get_chars(notes):
  for note in notes:
    yield from note['fields']['Front']['value']

notes = get_chinese_notes()
chars = set(get_chars(notes))
print(f'Unique hanzi:\n{", ".join(chars)}')
print(f'Your Chinese flashcards contain {len(chars)} unique hanzi')
