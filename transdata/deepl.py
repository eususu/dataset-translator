from dotenv import load_dotenv
from enum import Enum
import os
from typing import List
import requests

from transdata.color_print import ColorPrint


load_dotenv()


class Lang(Enum):
  EN="en"
  KO="ko"

class DeepL:
  sourceLang:Lang=Lang.EN
  targetLang:Lang=Lang.KO

  cache:dict=None

  def __init__(self, sourceLang:Lang, targetLang:Lang):
    self.sourceLang = sourceLang
    self.targetLang = targetLang

    self.cache = {} # not implemented

  def print_cache(self):
    ColorPrint.print_bold(f'CACHE=[')
    for k,v in self.cache.items():
      ColorPrint.print_bold(f'- {k}={v}')
    ColorPrint.print_bold(f']')

  def _call_deepl(self, req:dict)->List[str]:
    url="https://api-free.deepl.com/v2/translate"
    response = requests.api.post(url,
      headers={
        'Content-Type':'application/json',
        'Authorization': f'DeepL-Auth-Key {os.environ["DEEPL_AUTH_KEY"]}',
        },
      json=req)
    status_code = response.status_code
    response = response.json()
    if status_code != 200:
      print(response)
      return None

    return response['translations']
  def _call_deepl_dummy(self, req:dict)->List[str]:
    outputs = []
    messages = req['text']

    for message in messages:
      if message == 'this is hello':
        tr = '이건 안녕'
      elif message == 'hello world':
        tr = '안녕 세상'
      elif message == 'ttest':
        tr = '테테스트'
      else:
        tr = 'ㅁ도름'
      outputs.append({'text':tr})

    return outputs
    
  def translate(self, messages:List[str]):

    cached_index = []
    source_messages = []
    for index, message in enumerate(messages):
      if message in self.cache:
        cached_index.append(index)
        continue
      source_messages.append(message)

    req = {
      'text': source_messages,
      'source_lang': self.sourceLang.value,
      'target_lang': self.targetLang.value,
    }

    #response = self._call_deepl_dummy(req)
    response = self._call_deepl(req)

    translated = []
    input_length = 0
    output_length = 0
    for index, translation in enumerate(response):
      input_length += len(source_messages[index])
      translation_text = translation['text']
      output_length += len(translation_text)
      translated.append(translation_text)

      self.cache[source_messages[index]] = translation_text # append cache

    for cache_index in cached_index:
      translated.insert(cache_index, self.cache[messages[cache_index]])

    ColorPrint.print_pass(f"DEEPL - translated(from {input_length} chars to {output_length} chars)")

    return translated
      

if __name__ == "__main__":

  deepl = DeepL(Lang.EN, Lang.KO)
  messages = ['this is hello', 'hello world']
  translated = deepl.translate(messages)
  print(translated)
  messages = ['test', 'this is hello', 'ttest', 'hello world']
  translated = deepl.translate(messages)
  print(translated)
  messages = ['this is hello', 'ttest', 'hello world', 'what is your name']
  translated = deepl.translate(messages)
  print(translated)

  deepl.print_cache()
  