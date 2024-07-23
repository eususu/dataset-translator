from typing import List
from transdata.color_print import ColorPrint
from transdata.data_loader import DataLoader

import jq
import json


class Translator:
  data_loader=None

  def __init__(self, path:str, jq_patterns:List[str]):

    #self.data_loader = DataLoader(path)
    #item = self.data_loader.item()
    item = {'inputs': [[{'content': 'butcher shop phone number', 'name': 'question', 'type': 'user_input'}], [{'content': 'passage 1:Butcher Shop - Hayward 826 B Street, Hayward CA 94541 Phone Number: (510) 889-8690\n\npassage 2:Butcher Shop - Lakefield 212 Main Street, Lakefield MN 56150 Phone Number: (507) 662-6281\n\npassage 3:Some More Phone Numbers Related To The Butcher Shop The Local Butcher Shop phone number : (510) 845-6328 Boones Butcher Shop phone number : (502) 348-3668 Ye Ole Butcher Shop phone number : (972) 423-1848 J Ms Butcher Shop phone number : (865) 483-9228\n\n', 'name': 'passages', 'type': 'context'}]], 'output': {'content': "The phone numbers for several butcher shops are mentioned in the passages. Butcher Shop in Hayward can be reached at (510) 889-8690. Butcher Shop in Lakefield can be contacted at (507) 662-6281. The Local Butcher Shop's number is (510) 845-6328, Boones Butcher Shop can be reached at (502) 348-3668, Ye Ole Butcher Shop's number is (972) 423-1848, and J Ms Butcher Shop's phone number is (865) 483-9228.", 'name': 'answer', 'type': 'response'}, 'score': 0}

    j = json.dumps(item)
    print(j)

    for index, jq_pattern in enumerate(jq_patterns):
      res = jq.all(jq_pattern, item)
      ColorPrint.print_pass(f'CONTENTS OF JQ_PATTERN #{index}({jq_pattern}) [')
      print(f'{res}')
      ColorPrint.print_pass(f']')
