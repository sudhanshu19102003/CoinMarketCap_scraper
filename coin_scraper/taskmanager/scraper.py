from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re


class CoinMarketCap:
    def __init__(self, url, element_class):
        self.url = url
        self.element_class = element_class
    def output(self, element):
        crypto_info = {}

        market_cap_element = element.find(string=re.compile(r'Market cap'))
        market_cap_value = market_cap_element.find_next('dd').text.strip().split('$')
        crypto_info['market_cap'] = int(''.join(market_cap_value[1].split(',')))

        market_cap_rank_element = market_cap_element.find_next(class_='rank-value')
        crypto_info['market_cap_rank'] = int(market_cap_rank_element.text.strip()[1:])

        volume_element = element.find(string=re.compile(r'Volume \(24h\)'))
        volume_value = volume_element.find_next('dd').text.strip().split('$')
        crypto_info['volume'] = int(''.join(volume_value[1].split(',')))

        volume_rank_element = volume_element.find_next(class_='rank-value')
        crypto_info['volume_rank'] = int(volume_rank_element.text.strip()[1:])

        volume_change_element = volume_element.find_next(class_='ihXFUo')
        crypto_info['volume_change'] = float(volume_change_element.text.strip()[:-1])

        circulating_supply_element = element.find(string=re.compile(r'Circulating supply'))
        crypto_info['circulating_supply'] = int(''.join(filter(str.isdigit, circulating_supply_element.find_next('dd').text.strip())))

        total_supply_element = element.find(string=re.compile(r'Total supply'))
        crypto_info['total_supply'] = int(''.join(filter(str.isdigit, total_supply_element.find_next('dd').text.strip())))

        diluted_market_cap_element = element.find(string=re.compile(r'Fully diluted market cap'))
        crypto_info['diluted_market_cap'] = int(''.join(diluted_market_cap_element.find_next('dd').text.strip()[1:].split(',')))

        return crypto_info

    def extract_info(self, element):
        contracts = []
        official_links = []
        socials = []

        contracts_section = element.find('div', string='Contracts')
        if contracts_section:
            contracts_elements = contracts_section.find_next('div', class_='sc-d1ede7e3-0 bwRagp')
            if contracts_elements:
                # Extract contracts if available
                contract_links = contracts_elements.find_all('a', class_='chain-name')
                for contract in contract_links:
                    name_element = contract.find('span', class_='dEZnuB')
                    if name_element:
                        name = name_element.get_text(strip=True).replace(':', '').strip().lower()
                        address = contract['href'].split('/')[-1]
                        contracts.append({"name": name, "address": address})


        # Extract official links
        official_links_element = element.find('div', string='Official links').find_next('div', class_='sc-d1ede7e3-0 bwRagp').find_all('a')
        official_links = {re.sub(r'\W+', '', link.get_text(strip=True).lower(), flags=re.UNICODE): link['href'] for link in official_links_element}

        # Extract socials
        socials_element = element.find('div', string='Socials').find_next('div', class_='sc-d1ede7e3-0 bwRagp').find_all('a')
        socials = {re.sub(r'[^a-zA-Z0-9]+', '', social.get_text(strip=True).lower()): social['href'] for social in socials_element}

        return {'contracts': contracts, 'official_links': official_links, 'socials': socials}

    def price_and_price_changes(self, element):
        output = {'price': None, 'price_change': None}
        price_element = element.find(class_='fsQm')
        if price_element:
            price_text = price_element.text.strip().replace('$', '')
            # Extracting only numeric characters from the string
            price_numeric = ''.join(filter(str.isdigit, price_text))
            output['price'] = float(price_numeric)
        price_change_element = element.find(class_='ihXFUo')
        if price_change_element:
            price_change_text = price_change_element.text.strip()
            # Extracting only numeric characters from the string
            price_change_numeric = ''.join(filter(str.isdigit, price_change_text))
            output['price_change'] = float(price_change_numeric) / 100  # Converting percentage to float
        return output

    def data_extraction(self, html_contain, coin):
        soup = BeautifulSoup(html_contain, "html.parser")
        coin_data = {"coin" : coin.upper(), "output": {}}
        # Extracting relevant elements
        price_selector = soup.find("div", class_="coin-stats-header")
        output_element = soup.find("dl", class_="coin-metrics-table")
        contracts_element = soup.find("div", class_="content_folded")

        # Extracting data
        price_info = self.price_and_price_changes(price_selector)
        output_info = self.output(output_element)
        contracts_info = self.extract_info(contracts_element)

        # Populating coin_data
        coin_data["output"] = {
            "price": price_info["price"] if price_info else "N/A",
            "price_change": price_info["price_change"] if price_info else "N/A",
            "market_cap": output_info["market_cap"] if output_info else "N/A",
            "market_cap_rank": output_info["market_cap_rank"] if output_info else "N/A",
            "volume": output_info["volume"] if output_info else "N/A",
            "volume_rank": output_info["volume_rank"] if output_info else "N/A",
            "volume_change": output_info["volume_change"] if output_info else "N/A",
            "circulating_supply": output_info["circulating_supply"] if output_info else "N/A",
            "total_supply": output_info["total_supply"] if output_info else "N/A",
            "diluted_market_cap": output_info["diluted_market_cap"] if output_info else "N/A",
            "contracts": contracts_info["contracts"] if contracts_info else "N/A",
            "official_links": contracts_info["official_links"] if contracts_info else "N/A",
            "socials": contracts_info["socials"] if contracts_info else "N/A",
        }
        return coin_data


    def retrieve_data(self,url, element_class):
        # Set up the WebDriver (you may need to adjust the path to your specific browser driver)
        options = webdriver.EdgeOptions()
        options.add_argument("--headless")
        driver = webdriver.Edge(options=options)
        # Open the URL
        driver.get(url)

        try:
            # Wait for the elements to load (adjust timeout and conditions as needed)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, element_class))
            )
            # Once elements are loaded, scrape the entire page
            data = driver.page_source

            # Close the WebDriver
            driver.quit()

            return data

        except TimeoutException:
            print("Timed out waiting for page to load")
            driver.quit()
            return None