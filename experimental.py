from src.tool import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()

class DateTime(BaseModel):
    format:str=Field(...,description="The format of the date and time.",example=['%Y-%m-%d %H:%M:%S'])

@tool("DateTime Tool",args_schema=DateTime)
def datetime_tool(format:str):
    '''
    Retrieves the current date and time in the specified format.
    '''
    from datetime import datetime
    try:
        current_datetime=datetime.now()
        formatted_datetime=current_datetime.strftime(format)
    except Exception as err:
        return f"Error: {err}"
    return formatted_datetime

class FinancialDataSource(BaseModel):
    source_type:str=Field(...,description="The type of financial data source.",example=['stock', 'forex', 'crypto'])

@tool("Financial Data Source Tool",args_schema=FinancialDataSource)
def financial_data_source_tool(source_type:str):
    """
    Provides information on reliable financial data sources and instructions on how to access them.
    """
    from typing import Dict

    financial_data_sources:Dict[str,Dict[str,str]]={
        'stock':{
            'yahoo_finance':'https://finance.yahoo.com/',
            'google_finance':'https://finance.google.com/',
            'nasdaq':'https://www.nasdaq.com/'
        },
        'forex':{
            'xignite':'https://www.xignite.com/',
            'oanda':'https://www.oanda.com/',
            'forex.com':'https://www.forex.com/'
        },
        'crypto':{
            'coinmarketcap':'https://coinmarketcap.com/',
            'coingecko':'https://www.coingecko.com/',
            'cryptocompare':'https://www.cryptocompare.com/'
        }
    }

    try:
        if source_type in financial_data_sources:
            return f"Financial data sources for {source_type} are:\n" + '\n'.join([f"{key}: {value}" for key, value in financial_data_sources[source_type].items()])
        else:
            return f"No financial data sources found for {source_type}."
    except Exception as err:
        return f"Error: {err}"

class YahooFinanceWebScraper(BaseModel):
    stock_symbol:str=Field(...,description="The stock symbol to be searched.",example=['AAPL'])

@tool("Yahoo Finance Web Scraper Tool",args_schema=YahooFinanceWebScraper)
def yahoo_finance_web_scraper_tool(stock_symbol:str):
    '''
    Retrieves the current stock price of the given stock symbol from Yahoo Finance.
    '''
    import requests
    from bs4 import BeautifulSoup
    import os
    try:
        url = f'https://finance.yahoo.com/quote/{stock_symbol}'
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        current_price = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'}).text
        return f'The current stock price of {stock_symbol} is {current_price}.'
    except Exception as err:
        return f'Error: {err}'

