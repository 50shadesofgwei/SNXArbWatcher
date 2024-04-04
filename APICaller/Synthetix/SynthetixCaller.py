from synthetix import *
from APICaller.Synthetix.SynthetixUtils import *
from GlobalUtils.logger import *

class SynthetixCaller:
    def __init__(self):
        self.client = get_synthetix_client()

    @log_function_call
    def get_funding_rates(self, symbols: list):
        try:
            _, markets_by_name = self.client.perps.get_markets()
            return self._filter_market_data(markets_by_name, symbols)
        except Exception as e:
            logger.error(f"SynthetixAPICaller - Error fetching market data: {e}")
            return []

    @log_function_call
    def _filter_market_data(self, markets_by_name, symbols):
        market_funding_rates = []
        for symbol in symbols:
            if symbol in markets_by_name:
                try:
                    market_data = markets_by_name[symbol]
                    funding_rate_24 = market_data['current_funding_rate']
                    skew = market_data['skew']
                    open_interest = market_data['size']
                    max_open_interest = market_data['max_open_interest']
                    asset_price = market_data['asset_price']
                    velocity = market_data['current_funding_velocity']
                    funding_rate = funding_rate_24 / 3
                    
                    market_funding_rates.append({
                        'exchange': 'Synthetix', 
                        'symbol': symbol,
                        'funding_rate': funding_rate,
                        'skew': skew,
                        'open_interest': open_interest,
                        'max_open_interest': max_open_interest,
                        'velocity': velocity,
                        'asset_price': asset_price
                    })
                except KeyError as e:
                    logger.error(f"SynthetixAPICaller - Error processing market data for {symbol}: {e}")
        return market_funding_rates


