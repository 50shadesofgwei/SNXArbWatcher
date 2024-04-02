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
            funding_rate = float(opportunity["funding_rate"])
            
            if abs(funding_rate) > max_profit:
                max_profit = funding_rate
                most_profitable = opportunity

        if most_profitable:
            position = "short" if most_profitable["funding_rate"] > 0 else "long"
            logger.info(f"Best opportunity found, suggested position: {position}, details: {most_profitable}")
        else:
            logger.info("No profitable opportunities found.")

        return most_profitable