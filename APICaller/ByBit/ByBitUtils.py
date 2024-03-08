from pybit.unified_trading import HTTP
from GlobalUtils.logger import logger
import os
from dotenv import load_dotenv
from enum import Enum


load_dotenv()

class ByBitEnvVars(Enum):
    BYBIT_API_KEY = 'BYBIT_API_KEY'
    BYBIT_API_SECRET = 'BYBIT_API_SECRET'
    
    def get_value(self):
        value = os.getenv(self.value)
        if value is None:
            raise ValueError(f"Environment variable for {self.name} not found.")
        return value

def get_ByBit_client() -> HTTP:
    try:
        client = HTTP(
            testnet=False,
            api_key=ByBitEnvVars.BYBIT_API_KEY.get_value(),
            api_secret=ByBitEnvVars.BYBIT_API_SECRET.get_value(),
        )
        return client
    except Exception as e:
        logger.error(f"ByBitAPIUtils - Failed to initialize ByBit client: {e}")
        return None
