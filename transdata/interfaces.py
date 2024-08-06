from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel


class Lang(Enum):
  EN={"short":"en", "full": "english"}
  KO={"short":"ko", "full": "korean"}

  @property
  def short(self):
    """
    return short value of selected language
    """
    return self.value['short']

  @property
  def full(self):
    """
    return full value of selected language
    """
    return self.value['full']

class TranslatorOptions(BaseModel):
  from_lang:Lang
  to_lang:Lang

class DeepLTranslatorOptions(TranslatorOptions):
  pass

class LLMTranslatorOptions(TranslatorOptions):
  llm_type:Literal["openai", "anthropic", "gemini"]
  llm_model:Optional[str]=None
  system_prompt:Optional[str]=None

  
class TranslateEngine(ABC):
  @abstractmethod
  def translate(self, messages:List[str]):
    raise NotImplementedError()