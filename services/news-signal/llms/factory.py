from typing import Literal

from .base import BaseNewsSignalExtractor
from .claude import ClaudeNewsSignalExtractor
from .config import AnthropicConfig, OllamaConfig
from .ollama import OllamaNewsSignalExtractor


def get_llm(model_provider: Literal['anthropic', 'ollama']) -> BaseNewsSignalExtractor:
    """
    Returns the LLM we want for the news signal extractor

    Args:
        model_provider: The model provider to use

    Returns:
        The LLM we want for the news signal extractor
    """
    if model_provider == 'anthropic':
        config = AnthropicConfig()

        return ClaudeNewsSignalExtractor(
            model_name=config.model_name,
            api_key=config.api_key,
        )

    elif model_provider == 'ollama':
        config = OllamaConfig()

        return OllamaNewsSignalExtractor(
            model_name=config.model_name,
        )

    else:
        raise ValueError(f'Unsupported model provider: {model_provider}')
