from bs4 import BeautifulSoup
import requests
import time
from models.product import Product
from database.local_db import DatabaseHandler
from notification.notificationService import NotificationService
from notification.observer import SlackNotifier, EmailNotifier
from cache.redis import RedisCache
from config.config_loader import load_config
import logging

class ScraperService:
    def __init__(self):
        self.configs = load_config()
        self.products = []
        self.db_handler = DatabaseHandler(self.configs)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Adding dummy observers for notification
        self.notification_service = NotificationService()
        slack_notifier = SlackNotifier()
        slack_notifier.add_recipient("Abc singh")
        slack_notifier.add_recipient("Efg Kumar")

        email_notifier = EmailNotifier()
        email_notifier.add_recipient("abc@example.com")
        email_notifier.add_recipient("efg@example.com")

        self.notification_service.subscribe(slack_notifier)
        self.notification_service.subscribe(email_notifier)
        
        # caching 
        self.redisClient = RedisCache(self.configs, self.logger)
        self.base_url = self.configs["TARGET_URL"]
    
    def run(self, start_page: int, end_page: int): 
        scraped_pages = 0
        error_pages = []
        
        for page in range(start_page, end_page + 1):
            try:
                self.scrape(page)
                scraped_pages += 1
            except Exception as e:
                self.logger.error(f"Error scraping page {page}: {e}")
                error_pages.append(page)
        
        
        # save product in db
        self.db_handler.save_product_data(self.products, self.redisClient)
        
        # notify all recepients
        notification_content = {
            "message": "Scraping completed",
            "pages_scraped": scraped_pages,
            "errors": f"Errors in scraping pages: {', '.join(map(str, error_pages))}" if error_pages else "null",
            "total_products": len(self.products)
        }
        
        self.notification_service.notify(notification_content, self.logger)
        
        return notification_content
    
    def scrape(self, page: int):
        retries = 3
        retry_delay = 2
        
        for attempt in range(1, retries + 1):
            try: 
                html_content = self.scrape_page(page)
                if isinstance(html_content, Exception):
                    self.logger.error(f"Error returned from scrape_page: {html_content}")
                    raise html_content
                
                soup = BeautifulSoup(html_content, "html.parser")
                
                product_list_container = soup.find("ul", class_="products columns-4")

                if product_list_container:
                    # Find all product items (li tags) inside the <ul>
                    product_items = product_list_container.find_all("li", class_="product")
                    
                    for item in product_items:
                        # Extract product title from <img title="...">
                        title_tag = item.find("img", title=True)
                        product_title = title_tag["title"] if title_tag else "N/A"
                        product_title = product_title.replace(" - Dentalstall India", "")

                        # Extract product image URL from <img src="...">
                        product_image = title_tag["src"] if title_tag else "N/A"

                        # Extract product price from the first <bdi> tag
                        price_tag = item.find("bdi")
                        if price_tag:
                            # Get only the number part (excluding the span for the currency symbol)
                            product_price_text = price_tag.get_text(strip=True)  # Get text without child tags
                            product_price_text = product_price_text.replace('₹', '').replace(',', '').strip()
                            product_price = float(product_price_text.replace(",", "").strip())
                        else:
                            product_price = 0.0

                        # Create a Product object and append it to the list
                        product = Product(
                            product_title=product_title,
                            product_price=product_price,
                            path_to_image=product_image
                        )
                        self.products.append(product)
                else:
                    self.logger.warning(f"No product list found on page {page}.")
                    
                self.logger.info(f"Total products scraped so far: {len(self.products)}")
                break
            
            except Exception as e:
                self.logger.error(f"Attempt {attempt} failed for page {page}: {e}")
                if attempt < retries:
                    self.logger.info(f"Retrying page {page} in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    self.logger.error(f"All retries failed for page {page}")
                    raise e


    def scrape_page(self, page: int):
        url = f"{self.base_url}/page/{page}/"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            self.logger.info(f"Successfully retrieved content for page {page}")
            return response.text
        except requests.HTTPError as http_err:
            return Exception(f"HTTP error occurred for page {page}: {http_err}")
        except requests.RequestException as req_err:
            return Exception(f"Request error occurred for page {page}: {req_err}")
        except Exception as e:
            return Exception(f"Unexpected error occurred for page {page}: {e}")