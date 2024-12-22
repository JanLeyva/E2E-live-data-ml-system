from typing import Literal, Optional

from llama_index.core.prompts import PromptTemplate
from llama_index.llms.ollama import Ollama

from .base import BaseNewsSignalExtractor, NewsSignal


class OllamaNewsSignalExtractor(BaseNewsSignalExtractor):
    def __init__(
        self,
        model_name: str,
        temperature: Optional[float] = 0,
    ):
        self.llm = Ollama(
            model=model_name,
            temperature=temperature,
        )

        self.prompt_template = PromptTemplate(
            template="""
            You are an expert crypto financial analyst with deep knowledge of market dynamics and sentiment analysis.
            Analyze the following news story and determine its potential impact on crypto asset prices.
            Focus on both direct mentions and indirect implications for each asset.

            Do not output data for a given coin if the news is not relevant to it.

            ## Example input
            "Goldman Sachs wants to invest in Bitcoin and Ethereum, but not in XRP"

            ## Example output
            [
                {"coin": "BTC", "signal": 1},
                {"coin": "ETH", "signal": 1},
                {"coin": "XRP", "signal": -1},
            ]

            News story to analyze:
            {news_story}
            """
        )

        self.model_name = model_name

    def get_signal(
        self,
        text: str,
        output_format: Literal['dict', 'NewsSignal'] = 'NewsSignal',
    ) -> dict | NewsSignal:
        """
        Get the news signal from the given `text`

        Args:
            text: The news article to get the signal from
            output_format: The format of the output

        Returns:
            The news signal
        """
        response: NewsSignal = self.llm.structured_predict(
            NewsSignal,
            prompt=self.prompt_template,
            news_story=text,
        )

        # keep only news signals with non-zero signal
        response = [
            news_signal
            for news_signal in response.news_signals
            if news_signal.signal != 0
        ]

        if output_format == 'dict':
            return response.to_dict()
        else:
            return response
