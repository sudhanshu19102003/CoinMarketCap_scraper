from celery import shared_task
from .scraper import CoinMarketCap

@shared_task
def start_scraping(coin_list):
    result = {"tasks": []}
    for coin in coin_list:
        try:
            # Create an instance of CoinMarketCap class
            coin_market_cap = CoinMarketCap(f"https://coinmarketcap.com/currencies/{coin}/", "coin-metrics")
            
            # Retrieve HTML content
            html_content = coin_market_cap.retrieve_data()
            
            if html_content:
                # Extract data
                coin_data = coin_market_cap.data_extraction(html_content, coin)
                result["tasks"].append(coin_data)
            else:
                raise Exception(f"Failed to retrieve data for {coin}")
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Error processing {coin}: {str(e)}")
    return result
