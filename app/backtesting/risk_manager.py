from dataclasses import dataclass


@dataclass
class RiskConfig:
    """
    Configuration for risk management.
    """

    risk_per_trade: float = 0.01      # 1% risk
    risk_reward_ratio: float = 2.0    # 1:2 RR
    max_position_size: int = 10000
    min_position_size: int = 1


class RiskManager:

    def __init__(self, config: RiskConfig = RiskConfig()):
        self.config = config

    def calculate_position_size(
        self,
        capital: float,
        entry_price: float,
        stop_loss: float,
    ) -> int:
        """
        Calculate quantity based on risk.
        """

        risk_amount = capital * self.config.risk_per_trade

        stop_distance = abs(entry_price - stop_loss)

        if stop_distance <= 0:
            return 0

        quantity = int(risk_amount / stop_distance)

        quantity = max(quantity, self.config.min_position_size)
        quantity = min(quantity, self.config.max_position_size)

        return quantity

    def calculate_stop_loss(
        self,
        entry_price: float,
        atr: float,
        direction: str = "LONG",
        multiplier: float = 1.0,
    ) -> float:

        if direction == "LONG":
            return entry_price - atr * multiplier

        return entry_price + atr * multiplier

    def calculate_target(
        self,
        entry_price: float,
        stop_loss: float,
        direction: str = "LONG",
    ) -> float:

        risk = abs(entry_price - stop_loss)

        reward = risk * self.config.risk_reward_ratio

        if direction == "LONG":
            return entry_price + reward

        return entry_price - reward