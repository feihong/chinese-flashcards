"""
Go through all .html files (except index.html) and merge their linked .js files into a single inline script tag
"""
from pathlib import Path
import re
import secrets


here = Path(__file__).parent
source_dir = here / 'Chinese'
output_dir = here / '_build'


def main():
  for html_file in source_dir.glob('**/*.html'):
    if html_file.name != 'index.html':
      output_file = output_dir / html_file.relative_to(here)
      print(output_file)

      output_file.parent.mkdir(parents=True, exist_ok=True)
      compiler = Compiler(html_file, output_file)
      compiler.build()

  file = output_dir / 'Chinese/pinyin to handwriting/back.html'
  new_text = file.read_text().replace('YOUR-SERVER.COM', secrets.server)
  file.write_text(new_text)


class Compiler:
  def __init__(self, input_file, output_file):
    self.input_file = input_file
    self.output_file = output_file

  def build(self):
    with self.output_file.open('w') as fp:
      for line in self.get_lines():
        fp.write(line)

  def get_lines(self):
    script_files = []

    with self.input_file.open() as fp:
      for line in fp:
        if m := re.match(r'<script src=\"(.*)\"></script>', line.strip()):
          script_file = self.input_file.parent / m.group(1)
          script_files.append(script_file)
        else:
          yield line

      if len(script_files) > 0:
        inline_script = '\n\n'.join(p.read_text() for p in script_files)
        yield '<script>\n{\n\n' + inline_script + '\n\n}\n</script>'


if __name__ == '__main__':
  main()
