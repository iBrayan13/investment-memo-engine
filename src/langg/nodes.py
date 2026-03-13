import logging

from src.langg.state import MemoState
from src.services.pchain.chainable import MinimalChainable
from src.core.settings import DevelopmentSettings as Settings
from src.services.pchain.chain_prompt_manager import ChainPromptManager
from src.langg.models import (
   ExceptionDict
)

logger = logging.getLogger(__name__)


class Nodes:
   def __init__(
      self,
      settings: Settings,
      minimal_chainable: MinimalChainable,
      prompt_manager: ChainPromptManager
   ) -> None:
      self.settings = settings
      self.minimal_chainable = minimal_chainable
      self.prompt_manager = prompt_manager