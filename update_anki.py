"""
Update Anki model templates
"""
from pathlib import Path
import requests

here = Path(__file__).parent
build_dir = here / '_build'

def invoke(action, **params):
  data = {'action': action, 'version': 6}
  if params:
    data['params'] = params
  r = requests.post('http://127.0.0.1:8765', json=data)
  return r.json()

def get_model_templates(model_dir: Path):
  for dir in model_dir.iterdir():
    if not dir.is_dir():
      continue
    front = (dir / 'front.html').read_text()
    back = (dir / 'back.html').read_text()
    yield dir.name, {'Front': front, 'Back': back}

def update_model_template(model_dir: Path):
  model_name = model_dir.name

  model = {
    'name': model_name,
    'templates': dict(get_model_templates(model_dir)),
  }
  result = invoke('updateModelTemplates', model=model)
  if error := result['error']:
    print(error)
  else:
    print(f'Updated template for {model_name}')

update_model_template(build_dir / 'Chinese')
