from GlobalUtils.globalUtils import *
from GlobalUtils.logger import *

class ProfitabilityChecker:

    def __init__(self):
        pass
    
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
