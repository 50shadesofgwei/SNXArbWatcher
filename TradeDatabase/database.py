import sqlite3
from datetime import datetime
from GlobalUtils.logger import *
from GlobalUtils.globalUtils import *
from pubsub import pub
import uuid

class TradeLogger:
    def __init__(self, db_path='trades.db'):
        self.db_path = db_path
        pub.subscribe(self.write_rates_to_database, eventsDirectory.FUNDING_RATE_DATA.value)
        try:
            self.conn = self.create_or_access_database()
        except Exception as e:
            logger.error(f"TradeLogger - Error accessing the database: {e}")
            raise e

    @log_function_call
    def create_or_access_database(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute('''CREATE TABLE IF NOT EXISTS historical_rates (
                        timestamp DATETIME NOT NULL
                        symbol TEXT NOT NULL,
                        long_exchange TEXT NOT NULL,
                        short_exchange TEXT NOT NULL,
                        long_rate_8hr REAL NOT NULL,
                        short_rate_8hr REAL NOT NULL,
                        differential REAL NOT NULL
                    );''')
            logger.info("TradeLogger - Database accessed successfully.")
            return conn
        except sqlite3.Error as e:
            logger.error(f"TradeLogger - Error creating/accessing the database: {e}")
            raise e

    @log_function_call
    def write_rates_to_database(self, opportunity):
        try:
            symbol = opportunity['symbol']
            long_exchange = opportunity['long_exchange']
            short_exchange = opportunity['short_exchange']
            long_rate_8hr = opportunity['long_rate_8hr'] 
            short_rate_8hr = opportunity['short_rate_8hr']
            differential = opportunity['differential']
            
            with sqlite3.connect(self.db_path) as conn:
                timestamp = datetime.now().timestamp()
                conn.execute('''INSERT INTO historical_rates (identifier, timestamp, symbol, long_exchange, short_exchange, long_rate_8hr, short_rate_8hr, differential)
                                VALUES (?, ?, ?, ?, ?, ?, ?);''', 
                            (timestamp, symbol, long_exchange, short_exchange, long_rate_8hr, short_rate_8hr, differential))
                logger.info(f"TradeLogger - Logged arbitrage details for opportunity: {opportunity}")
        except sqlite3.Error as e:
            logger.error(f"TradeLogger - Error logging arbitrage details for opportunity: {opportunity}. Error: {e}")

