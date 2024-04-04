from GlobalUtils.logger import *
from pubsub import pub
from APICaller.master.MasterCaller import MasterCaller
from MatchingEngine.MatchingEngine import matchingEngine
from MatchingEngine.profitabilityChecks.checkProfitability import ProfitabilityChecker
from TradeDatabase.database import Database
from GlobalUtils.globalUtils import *
from datetime import datetime
import threading


class Main:
    def __init__(self):
        setup_topics()
        self.caller = MasterCaller()
        self.matching_engine = matchingEngine()
        self.profitability_checker = ProfitabilityChecker()
        self.database = Database()
    
    @log_function_call
    def search_for_opportunities(self):
        try:
            timestamp = datetime.now().timestamp()
            funding_rates = self.caller.get_funding_rates()
            opportunities = self.matching_engine.find_delta_neutral_arbitrage_opportunities(funding_rates)
            most_profitable_opportunity = self.profitability_checker.find_most_profitable_opportunity(opportunities)

            for opportunity in opportunities:
                if opportunity is not None:
                    opportunity['timestamp'] = timestamp
                    pub.sendMessage(eventsDirectory.FUNDING_RATE_DATA.value, opportunity=opportunity)
                else:
                    logger.info("MainClass - Error while searching for opportunity.")
        except Exception as e:
            logger.error(f"MainClass - An error occurred during search_for_opportunities: {e}", exc_info=True)
            

    @log_function_call
    def start_search(self):
        self.search_for_opportunities()
        threading.Timer(30, self.start_search).start()
