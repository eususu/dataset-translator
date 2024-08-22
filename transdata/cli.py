
import logging
from typing import List

from .interfaces import DeepLTranslatorOptions, LLMTranslatorOptions, Lang, TranslatorOptions
from .translator import Translator

logging.basicConfig(level=5)
logging.getLogger("filelock").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def test_ragtruth():
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
    translator_options=LLMTranslatorOptions(from_lang=Lang.EN, to_lang=Lang.KO, llm_type='anthropic'),
    split='dev',
    max_iterations=500,
    test_mode=False)
  translator.translate()

def test_drop():
  name="yettiesoft/kaai_qa"
  name="Flowrite/formatted-ragtruth-qa"
  name="ucinlp/drop"

  def extractDict(source:dict)->List[str]:
    l = []
    l.append(source['passage'])
    l.append(source['question'])
    return l

  def mergeDict(d:dict, translated:List[str]):
    d['passage'] = translated[0]
    d['question'] = translated[1]
    
  
  to:TranslatorOptions = None
  to=LLMTranslatorOptions(from_lang=Lang.EN, to_lang=Lang.KO, llm_type='anthropic')
  to=DeepLTranslatorOptions(from_lang=Lang.EN, to_lang=Lang.KO,)
  translator = Translator(
    path=name,
    output_path='out.jsonl',
    extractDict=extractDict,
    mergeDict=mergeDict,
    translator_options=to,
    split='train',
    max_iterations=5,
    test_mode=False)
  translator.translate()

if __name__ == "__main__":
  #test_ragtruth()
  test_drop()