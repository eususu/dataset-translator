from typing import List

from lite_llm_client import LiteLLMClient, LLMMessage, LLMMessageRole, InferenceOptions, OpenAIConfig, AnthropicConfig
import json

from transdata.interfaces import LLMTranslatorOptions, Lang, TranslateEngine, TranslatorOptions
from transdata.color_print import ColorPrint


class LLM(TranslateEngine):
  llc:LiteLLMClient=None
  translator_options:LLMTranslatorOptions

  def __init__(self, translator_options:LLMTranslatorOptions):
    self.translator_options = translator_options
    #self.llc = LiteLLMClient(OpenAIConfig())
    self.llc = LiteLLMClient(AnthropicConfig())


  
  def _get_messages(self, json_messages:str)->List[LLMMessage]:
    opt = self.translator_options

    if opt.llm_type == 'openai':
      return [
      LLMMessage(role=LLMMessageRole.SYSTEM, content=f"""you are professional language translator.
translate the below texts to {opt.to_lang} and output in JSON array format without any extra message."""),
LLMMessage(role=LLMMessageRole.USER, content=f"{json_messages}"),
    ]
    elif opt.llm_type == 'anthropic':
      return [
      LLMMessage(role=LLMMessageRole.SYSTEM, content=f"""you are professional language translator.
translate input texts to {opt.to_lang} and output in JSON array format without any extra message."""),
LLMMessage(role=LLMMessageRole.USER, content=f"""json message is {json_messages}"""),
    ]
    elif opt.llm_type == 'gemini':
      raise NotImplementedError(f'unsupported llm_type:{opt.llm_type}')
    else:
      raise NotImplementedError(f'unsupported llm_type:{opt.llm_type}')
    
  def translate(self, messages:List[str]):

    json_messages = json.dumps(messages, ensure_ascii=False)
    _messages = self._get_messages(json_messages=json_messages)
    
    answer = self.llc.chat_completions(messages=_messages, options=InferenceOptions(temperature=0.0, max_tokens=4096))

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