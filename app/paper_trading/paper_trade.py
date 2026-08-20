"""Paper-trade wrapper that reuses Falcon's completed Trade model."""

from __future__ import annotations

from dataclasses import dataclass

from app.backtesting.trade import Trade


@dataclass(frozen=True, slots=True)
class PaperTrade:
    """A completed virtual trade associated with a live paper session."""

    session_id: str
    trade: Trade

    def to_dict(self) -> dict[str, object]:
        """Serialize the completed trade for journals and exports."""
        return {"session_id": self.session_id, **self.trade.to_dict()}
