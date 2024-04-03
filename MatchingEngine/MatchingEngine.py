from MatchingEngine.MatchingEngineUtils import *
from GlobalUtils.logger import *

class matchingEngine:
    def __init__(self):
        pass

    @log_function_call
    def find_arbitrage_opportunities_for_symbol(self, sorted_rates):
        synthetix_rates = [rate for rate in sorted_rates if rate['exchange'] == 'Synthetix']
        binance_rates = [rate for rate in sorted_rates if rate['exchange'] == 'Binance']

        arbitrage_opportunities = []
        for synthetix_rate in synthetix_rates:
            symbol = normalize_symbol(synthetix_rate['symbol'])
            funding_rate_synthetix = float(synthetix_rate['funding_rate'])

            corresponding_binance_rate = next((rate for rate in binance_rates if normalize_symbol(rate['symbol']) == symbol), None)
            if corresponding_binance_rate is None:
                continue 

            funding_rate_binance = float(corresponding_binance_rate['funding_rate'])

            if funding_rate_synthetix > funding_rate_binance:
                long_exchange = 'Synthetix'
                short_exchange = 'Binance'
                synthetix_rate_8hr = funding_rate_synthetix
                binance_rate_8hr = funding_rate_binance
            else:
                long_exchange = 'Binance'
                short_exchange = 'Synthetix'
                synthetix_rate_8hr = funding_rate_binance
                binance_rate_8hr = funding_rate_synthetix

            arbitrage_opportunity = {
                'long_exchange': long_exchange,
                'short_exchange': short_exchange,
                'symbol': symbol,
                'binance_rate_8hr': binance_rate_8hr,
                'synthetix_rate_8hr': synthetix_rate_8hr
            }
            arbitrage_opportunities.append(arbitrage_opportunity)

        return arbitrage_opportunities


    @log_function_call
    def find_delta_neutral_arbitrage_opportunities(self, funding_rates):
        opportunities = []
        rates_by_symbol = group_by_symbol(funding_rates)
        for symbol, rates in rates_by_symbol.items():
            sorted_rates = sort_funding_rates_by_value(rates)
            opportunities.extend(self.find_arbitrage_opportunities_for_symbol(sorted_rates))
        return opportunities