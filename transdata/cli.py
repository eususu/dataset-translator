
import logging
from typing import List

from .interfaces import LLMTranslatorOptions, Lang
from .translator import Translator

logging.basicConfig(level=5)


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
    translator_options=LLMTranslatorOptions(from_lang=Lang.EN, to_lang=Lang.KO, llm_type='openai'),
    split='dev',
    max_iterations=500,
    test_mode=False)
  translator.translate()

if __name__ == "__main__":
  test()