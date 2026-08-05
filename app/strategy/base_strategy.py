from abc import ABC, abstractmethod
import pandas as pd


class BaseStrategy(ABC):
    """
    Base class for every trading strategy.
    """

    # Human-readable strategy name
    name: str = "Base Strategy"

    # Short description
    description: str = ""

    # Parameters available for optimization
    parameter_space: dict = {}

    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals.

        Returns
        -------
        DataFrame
            Must contain a 'signal' column.

            signal:
                1  -> Buy
               -1  -> Sell
                0  -> Hold
        """
        raise NotImplementedError

    def get_parameters(self) -> dict:
        """
        Returns the current parameter values of the strategy.
        """
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        }