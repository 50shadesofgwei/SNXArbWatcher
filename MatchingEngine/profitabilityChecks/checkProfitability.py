from GlobalUtils.globalUtils import *
from GlobalUtils.logger import *

class ProfitabilityChecker:
    exchange_fees = {
        "Binance": 0.0004,  # 0.04% fee
        "Synthetix": 0    # gas fees handled elsewhere
    }

    def __init__(self):
        pass

    @log_function_call
    def get_exchange_fee(self, exchange: str) -> float:
        return self.exchange_fees.get(exchange, 0)

    @log_function_call
    def calculate_position_cost(self, fee_rate: float, opportunity) -> float:
        capital = self.get_capital_amount(opportunity)
        return capital * fee_rate
    
    @log_function_call
    def find_most_profitable_opportunity(self, opportunities):
        max_profit = float('-inf')
        most_profitable = None
        for opportunity in opportunities:
            binance_rate = float(opportunity["binance_rate_8hr"])
            synthetix_rate = float(opportunity["synthetix_rate_8hr"])
            differential = abs(synthetix_rate - binance_rate)
            
            if differential > max_profit:
                max_profit = differential
                most_profitable = opportunity

        if most_profitable:
            position = "short" if most_profitable["synthetix_rate_8hr"] > most_profitable["binance_rate_8hr"] else "long"
            logger.info(f"Best opportunity found, suggested position: {position}, details: {most_profitable}")
        else:
            logger.info("No profitable opportunities found.")

        return most_profitable
