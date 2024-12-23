import pandas as pd
from loguru import logger
from xgboost import XGBRegressor


class XGBoostModel:
    """
    Encapsulates the training logic with or without hyperparameter tuning using an
    XGBRegressor.
    """

    def __init__(self):
        self.model = XGBRegressor(
            objective='reg:absoluteerror',
            eval_metric=['mae'],
        )

    def get_model_object(self):
        """
        Returns the model object.
        """
        return self.model

    def fit(self, X: pd.DataFrame, y: pd.Series, hyperparameter_tuning: bool = False):
        if not hyperparameter_tuning:
            logger.info('Fitting XGBoost model without hyperparameter tuning')
            self.model.fit(X, y)
        else:
            # TODO: Implement hyperparameter tuning
            logger.info('Fitting XGBoost model with hyperparameter tuning')
            raise NotImplementedError('Hyperparameter tuning is not implemented')

            # TODO: On Wednesday we will implement hyperparameter tuning using Optuna.

    def predict(self, X: pd.DataFrame) -> pd.Series:
        return self.model.predict(X)
