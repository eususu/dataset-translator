from typing import Callable, List
from transdata.deepl import DeepL, Lang
from transdata.color_print import ColorPrint
from transdata.data_loader import DataLoader

import jq
import json


class Translator:
  data_loader=None
  test_mode=False
  deepl:DeepL
  extractDict:Callable[[dict],List[str]]=None
  mergeDict:Callable[[dict, List[str]], None]=None
  output_path:str
  split:str

  def __init__(
    self,
    path:str,
    output_path:str,
    extractDict:Callable[[dict], List[str]],
    mergeDict:Callable[[dict, List[str]], None],
    split:str=None,
    test_mode=False
    ):

    self.output_path = output_path
    self.data_loader = DataLoader(path)
    self.test_mode = test_mode
    self.deepl = DeepL(Lang.EN, Lang.KO)
    self.extractDict = extractDict
    self.mergeDict = mergeDict
    self.split = split

  def _single_translate(self, item:dict)->None:
    messages = self.extractDict(item)

    translated = []
    if not self.test_mode:
      translated = self.deepl.translate(messages)
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
      output_lines = []
      output_name = f'{split}-{self.output_path}'
      begin_index = 0
      write_mode = "new"
      with open(output_name, 'r') as fp:
        lines = fp.readlines()
        begin_index = len(lines)
        write_mode = "continue"
      
      ColorPrint.print_bold(f'Output file is ({output_name})')
      ColorPrint.print_bold(f'Output mode is ({write_mode})')
      for item_index, item in enumerate(dataset):
        if item_index < begin_index: # pass already translated data
          continue

        self._single_translate(item)
        output_lines.append(json.dumps(item, ensure_ascii=False))

        if item_index >= 2+begin_index:
          break# for test
      
      if self.test_mode:
        ColorPrint.print_warn('In test_mode, does not append output.')
        continue

      with open(output_name, 'a') as fp:
        fp.writelines(line + '\n' for line in output_lines)

      
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

