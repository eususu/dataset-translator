import logging
from typing import Callable, List

from .interfaces import DeepLTranslatorOptions, LLMTranslatorOptions, TranslateEngine, TranslatorOptions
from ._llm import LLM
from .deepl import DeepL, Lang
from .color_print import ColorPrint
from .data_loader import DataLoader

import json


class Translator:
  data_loader=None
  test_mode=False
  engine:TranslateEngine
  extractDict:Callable[[dict],List[str]]=None
  mergeDict:Callable[[dict, List[str]], None]=None
  translator_options:TranslatorOptions
  output_path:str
  split:str
  max_iterations:int

  def __init__(
    self,
    path:str,
    output_path:str,
    extractDict:Callable[[dict], List[str]],
    mergeDict:Callable[[dict, List[str]], None],
    translator_options:TranslatorOptions,
    split:str=None,
    max_iterations:int=10,
    test_mode=False,
    ):

    self.data_loader = DataLoader(path)

    target_class = None
    if isinstance(translator_options, LLMTranslatorOptions):
      target_class = LLM
    elif isinstance(translator_options, DeepLTranslatorOptions):
      target_class = DeepL
    else:
      raise NotImplementedError(f'unsupported options:{translator_options}')
    self.engine = target_class(translator_options=translator_options)

    self.output_path = output_path
    self.extractDict = extractDict
    self.mergeDict = mergeDict
    self.translator_options = translator_options
    self.split = split
    self.max_iterations = max_iterations
    self.test_mode = test_mode

  def _single_translate(self, item:dict)->None:
    messages = self.extractDict(item)

    translated = []
    if not self.test_mode:
      translated = self.engine.translate(messages)
      if len(messages) != len(translated):
        ColorPrint.print_fail(f"messages: {len(messages)}")
        logging.debug(messages)
        ColorPrint.print_fail(f"translated: {len(translated)}")
        logging.debug(translated)

      input_length = 0
      output_length = 0
      for index, m in enumerate(messages):
        input_length += len(m)
        output_length += len(translated[index])
      
      ColorPrint.print_pass(f"ENGINE - translated(from {input_length} chars to {output_length} chars)")
    else:
      for message in messages:
        translated.append(f'### TRANSLATED DATA #{message} ###')

    self.mergeDict(item, translated)

  def translate(self):
    datasets = self.data_loader.items()

    for split, dataset in datasets.items():
      if self.split and (self.split != split):
        ColorPrint.print_warn(f'pass this split({split}) target split({self.split}) ')
        continue
        
      ColorPrint.print_pass(f'Dataset: {split}, len: {len(dataset)}')
      output_name = f'{split}-{self.output_path}'
      begin_index = 0
      write_mode = "new"
      with open(output_name, 'r') as fp:
        lines = fp.readlines()
        begin_index = len(lines)
        write_mode = "continue"
      
      ColorPrint.print_bold(f'OUTPUT file({output_name}) mode({write_mode}) index({begin_index} max_iterations({self.max_iterations}))')
      for item_index, item in enumerate(dataset):
        if item_index >= self.max_iterations + begin_index:
          break# for test

        if item_index < begin_index: # pass already translated data
          continue

        self._single_translate(item)
        output_line = json.dumps(item, ensure_ascii=False)
      
        if self.test_mode:
          ColorPrint.print_warn('In test_mode, does not append output.')
          continue

        with open(output_name, 'a') as fp:
          """
          번역 속도가 매우 빠르다면, fd를 열어두고 쓰면 되는데, 거의 초단위로 번역되니까, 항상 쓰는게 나을듯..
          """
          fp.write('\n')
          fp.write(output_line)

      
    """
    # jq로 데이터를 업데이트까지 해주면 좋은데, 아직은 그게 안되는 듯.
    # jq는 jq 유틸리티의 bind api라서 성능도 그닥일듯..

    for index, jq_pattern in enumerate(jq_patterns):
      res = iter(jq.all(jq_pattern, item))
      ColorPrint.print_pass(f'CONTENTS OF JQ_PATTERN #{index}({jq_pattern}) [')
      while(True):
        r = next(res, None)
        if r == None:
          break
        print(f'{r}')
      ColorPrint.print_pass(f']')

      r = jq.compile(f'{jq_pattern}').input_value(item).first()
      print('\n\n')
      print(r)
      print('\n\n')

      translated = []
      for index, s in enumerate(res):
        translated.append(f'##{s}##')
      ColorPrint.print_pass(f'TARGET [')
      print(f'{translated}')
      ColorPrint.print_pass(f']')
    """

