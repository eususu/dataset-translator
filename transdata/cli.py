
from .translator import Translator


def test():
  name="yettiesoft/kaai_qa"
  name="Flowrite/formatted-ragtruth-qa"
  translator = Translator(path=name, jq_patterns=[".inputs[][].content", ".output.content"])
  print(translator)

if __name__ == "__main__":
  test()