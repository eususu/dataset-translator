from typing import List

from lite_llm_client import LiteLLMClient, LLMMessage, LLMMessageRole, InferenceOptions, OpenAIConfig
import json

from transdata.interfaces import Lang, TranslateEngine
from transdata.color_print import ColorPrint


class LLM(TranslateEngine):
  llc:LiteLLMClient=None
  from_lang:str|None
  to_lang:str

  def __init__(self, from_lang:Lang, to_lang:Lang):
    self.from_lang = from_lang.full
    self.to_lang = to_lang.full
    self.llc = LiteLLMClient(OpenAIConfig())

  def translate(self, messages:List[str]):

    json_messages = json.dumps(messages, ensure_ascii=False)
    _messages = [
      LLMMessage(role=LLMMessageRole.SYSTEM, content="you are professional language translator."),
      LLMMessage(role=LLMMessageRole.USER, content=f"""translate given json messages's {self.from_lang} texts to {self.to_lang}.
follow below json output format.
[
  "translated message1",
  "translated message2"
]

"""),
      LLMMessage(role=LLMMessageRole.USER, content=f"json message is {json_messages}"),
    ]
    
    answer = self.llc.chat_completions(messages=_messages, options=InferenceOptions(temperature=0.0))

    try:
      obj = json.loads(answer)
    except ValueError as ve:
      """
      Sometimes LLM does not answer as invalid json format.
      in my cases, markdown json format.
      """
      ColorPrint.print_bold('SOURCE MESSAGES:')
      for m in messages:
        print(f' {m}')

      ColorPrint.print_fail('TRANSLATED MESSAGE BY LLM:')
      print(f' {answer}')
      ColorPrint.print_fail('ERROR REASON:')
      print(ve)
      raise ve
    return obj