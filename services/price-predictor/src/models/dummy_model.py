from typing import Optional

import pandas as pd


class DummyModel:
    """
    A dummy model that predict the price at X moment.
    """

    def __init__(self, from_feature: Optional[str] = 'close'):
        """
        We can predict base on close price or any of the
        features we calculate, for instance moving average
        """
        self.from_feature = from_feature

    def predict(self, data: pd.DataFrame):
        try:
            return data[self.from_feature]
        except ValueError as e:
            raise ValueError(
                f'feature not found in dataframe {self.from_feature}'
            ) from e

    # you could also return a moving average, using for instance
