import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
import json

# Configure logging
logging.basicConfig(filename='activity_log.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_rating(review_url):
    try:
        response = requests.get(review_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        rating_element = soup.select_one('div[data-cy="reviewRating"]')
        if rating_element:
            rating = rating_element.text.strip().split('/')[0]
            logging.info(f"Successfully retrieved rating from {review_url}")
            return rating
    except Exception as e:
        logging.error(f"Failed to get rating from {review_url}: {e}")
    return None

urls = [
    "https://www.cnet.com/tech/mobile/best-wireless-earbuds/",
    "https://www.cnet.com/tech/mobile/best-headphones/",
    "https://www.cnet.com/tech/mobile/best-wireless-earbuds-and-bluetooth-headphones-for-making-calls/",
    "https://www.cnet.com/tech/mobile/best-noise-canceling-wireless-earbuds/",
    "https://www.cnet.com/tech/mobile/best-cheap-wireless-earbuds/",
    "https://www.cnet.com/tech/mobile/best-noise-canceling-headphones/",
    "https://www.cnet.com/tech/mobile/best-over-ear-headphones/",
    "https://www.cnet.com/tech/mobile/best-headphones-for-work-at-home/",
    "https://www.cnet.com/tech/mobile/best-sounding-wirele-earbuds/",
    "https://www.cnet.com/tech/mobile/best-wireless-headphones/",
    "https://www.cnet.com/tech/mobile/best-travel-headphones-for-2024/",
    "https://www.cnet.com/tech/mobile/best-wireless-earbuds-and-headphones-for-samsung-phones/",
    "https://www.cnet.com/tech/mobile/best-back-to-school-headphones/",
    "https://www.cnet.com/health/sleep/headphones-for-sleeping/",
    "https://www.cnet.com/tech/mobile/best-sony-headphones-and-earbuds/",
    "https://www.cnet.com/tech/mobile/best-open-wireless-earbuds/",
    "https://www.cnet.com/tech/mobile/best-open-wireless-earbuds/",
    "https://www.cnet.com/tech/mobile/best-cheap-earbuds-and-headphones/",
    "https://www.cnet.com/tech/mobile/best-workout-headphones/",
    "https://www.cnet.com/tech/mobile/best-running-headphones/",
    "https://www.cnet.com/tech/mobile/best-multipoint-bluetooth-headphones-and-earbuds/",
    "https://www.cnet.com/tech/gaming/best-xbox-gaming-headset/",
    "https://www.cnet.com/tech/mobile/best-on-ear-headphones/",
    "https://www.cnet.com/tech/mobile/best-noise-canceling-headphones-under-100/",
    "https://www.cnet.com/tech/mobile/best-kids-headphones/" 
]

product_info = []

for url in urls:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        products = soup.select('div.c-bestListProductListing_content')
        for product in products:
            name = product.select_one('h4.c-bestListProductListing_hed').text.strip()
            description = product.select_one('div.c-bestListProductListing_description').text.strip()
            review_link_element = product.select_one('div.c-bestListProductRail_section a[href^="http"]')
            pros_cons_section = product.select('div.c-bestListProductRail_section')
            pros, cons = '', ''
            for section in pros_cons_section:
                attribute = section.select_one('span.c-bestListProductRail_attribute')
                if attribute and attribute.text.strip() == "Pros":
                    pros = ', '.join([li.text.strip() for li in section.select('li')])
                elif attribute and attribute.text.strip() == "Cons":
                    cons = ', '.join([li.text.strip() for li in section.select('li')])
            rating = None
            if review_link_element:
                review_url = review_link_element['href']
                rating = get_rating(review_url)

            product_info.append({
                'Product Name': name,
                'Product Description': description,
                'Pros': pros,
                'Cons': cons,
                'Rating': rating
            })

            logging.info(f"Processed product: {name}")
            time.sleep(1)
    except Exception as e:
        logging.error(f"Failed to process URL {url}: {e}")


with open('expert_reviews.json', 'w', encoding='utf-8') as f:
    json.dump(product_info, f, ensure_ascii=False, indent=4)

logging.info("All products have been successfully processed and saved to expert_reviews.json.")

