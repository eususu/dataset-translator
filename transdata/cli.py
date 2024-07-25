
from typing import List
from .translator import Translator


def test():
  name="yettiesoft/kaai_qa"
  name="Flowrite/formatted-ragtruth-qa"

  def extractDict(source:dict)->List[str]:
    l = []
    l.append(source['inputs'][0][0]['content'])
    l.append(source['inputs'][1][0]['content'])
    l.append(source['output']['content'])
    return l

  def mergeDict(d:dict, translated:List[str]):
    d['inputs'][0][0]['content'] = translated[0]
    d['inputs'][1][0]['content'] = translated[1]
    d['output']['content'] = translated[2]
    
  translator = Translator(
    path=name,
    output_path='out.jsonl',
    extractDict=extractDict,
    mergeDict=mergeDict,
    split='dev',
    max_iterations=500,
    test_mode=False)
  translator.translate()

if __name__ == "__main__":
  test()