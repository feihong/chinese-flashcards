"""
Generate an AI prompt to to check the grammar of all examples in the Test deck
"""
import requests

def invoke(action, **params):
  data = {'action': action, 'version': 6}
  if params:
    data['params'] = params
  r = requests.post('http://127.0.0.1:8765', json=data)
  return r.json()

def get_notes():
  note_ids = invoke('findNotes', query='deck:Test note:Chinese')['result']
  print(f'Found {len(note_ids)} Chinese notes in the Test deck')
  return invoke('notesInfo', notes=note_ids)['result']

notes = get_notes()
examples = [note['fields']['example']['value'].strip() for note in notes]
examples = [e for e in examples if len(e) and e != '<br>']

print(f"""
For each of the Chinese sentences below, point out any grammar mistakes or awkward phrasing:

""")
for i, example in enumerate(examples, 1):
  print(f'{i}. {example}')
