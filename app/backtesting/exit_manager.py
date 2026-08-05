class ExitManager:

    def should_exit(self, position, candle):
        """
        Decide whether a position should be exited.

        Returns:
            (should_exit, exit_price, reason)
        """

        # LONG position
        if position.direction == "LONG":

            # Stop Loss
            if candle.low <= position.stop_loss:
                return True, position.stop_loss, "STOP_LOSS"

            # Target
            if candle.high >= position.target:
                return True, position.target, "TARGET"

            # Strategy Exit
            if candle.signal == -1:
                return True, candle.close, "SIGNAL"

        # SHORT position (future support)
        else:

            if candle.high >= position.stop_loss:
                return True, position.stop_loss, "STOP_LOSS"

            if candle.low <= position.target:
                return True, position.target, "TARGET"

            if candle.signal == 1:
                return True, candle.close, "SIGNAL"

        return False, None, None