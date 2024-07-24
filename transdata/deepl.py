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

  def translate(self, messages:List[str]):
    url="https://api-free.deepl.com/v2/translate"

    req = {
      'text': messages,
      'source_lang': self.sourceLang.value,
      'target_lang': self.targetLang.value,
    }

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
      return []

    translated = []
    input_length = 0
    output_length = 0
    for index, response_item in enumerate(response['translations']):
      input_length += len(messages[index])
      output_length += len(response_item['text'])
      translated.append(response_item['text'])

    ColorPrint.print_pass(f"DEEPL - translated(from {input_length} chars to {output_length} chars)")

    return translated
      