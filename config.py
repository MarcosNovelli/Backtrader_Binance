from binance.client import Client
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ["api_key"]
api_secret = os.environ["api_secret"]
client = Client(api_key, api_secret)
