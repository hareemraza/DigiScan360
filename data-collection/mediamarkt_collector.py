import requests
import json
from bs4 import BeautifulSoup
import time
import logging  

logging.basicConfig(filename='mediamarkt.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Accept-Language": "es;q=1.0, en-US;q=0.9, en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Referer": "https://www.google.com/",
    "DNT": "1", 
}

def get_product_info(soup):
    """
    Extracts product information from the given soup

    Parameters:
    soup: Parsed HTML of the product page.
    
    Returns:
    dict: Product details including title, brand, rating, rating count, price, description, and image URL. Missing elements are None.
    """
    title_text, brand, rating, rating_count, price, description, img_url = (None,) * 7

    title_element = soup.find(name="h1", class_="sc-3f2da4f5-0 fzAxvp")
    if title_element:
        title_text = title_element.get_text().strip()

    brand_elements = soup.find_all(name="p", class_="sc-3f2da4f5-0 bQjqPs")
    if brand_elements and len(brand_elements) > 2:
        brand = brand_elements[2].get_text().strip()

    rating_element = soup.find(name="span", class_="sc-3f2da4f5-0 hTIzMV sc-2b40af13-0 brGkHH sc-456624cd-0 emcpVY")
    if rating_element:
        rating = rating_element.get_text()

    ratingcount_element = soup.find(name="span", class_="sc-3f2da4f5-0 dvVzKv")
    if ratingcount_element:
        rating_count = ratingcount_element.get_text().strip('()')

    price_element = soup.find(name="span", class_="sc-e0c7d9f7-0 bPkjPs")
    if price_element:
        price = price_element.get_text().strip(",").replace("\u20ac", "")

    description_element = soup.find(name="div", class_="sc-3f2da4f5-0 cBePzJ sc-b292c3cd-0 eXcgpL")
    if description_element:
        description = description_element.get_text().strip()

    image_element = soup.find(name="div", class_="sc-8bc4a1a5-1 heVipb pdp-gallery-image") 
    if image_element and image_element.find('img'):
        img_url = image_element.find('img')['src']

    return {
        "title": title_text,
        "brand": brand,
        "rating": rating,
        "rating_count": rating_count,
        "price": price,
        "img_url": img_url,
        "description": description
    }

def get_product_reviews(soup):
    """
    Extracts a list of product reviews the given soup.
    Each review includes the review's title, rating (as a count of filled star elements), date, and body text. 
    These elements are identified by specific HTML classes.

    Parameters:
    soup: Parsed HTML of the review section of the page.
    
    Returns:
    list of dict: A list of dictionaries, each representing a product review with title, rating, date, and review body.
                  Missing elements are represented as None for strings and 0 for numeric values.
    """
    review_elements = soup.find_all(name="div", class_="sc-ab96a29f-0 dNyAQG")
    review_list = []
    for review_element in review_elements:
        date_elements = review_element.find_all(name="span", class_="sc-3f2da4f5-0 bQjqPs")
        date = date_elements[-1].get_text() if date_elements else None

        title_element = review_element.find(name="p", class_="sc-3f2da4f5-0 iishlg")
        title_text = title_element.get_text().strip() if title_element else None

        reviewtext_element = review_element.find(name="p", class_="sc-3f2da4f5-0 cBePzJ")
        review_text = reviewtext_element.get_text().strip() if reviewtext_element else None

        rating_elements = review_element.find_all('div', class_='sc-4651df48-0 jMikJy')
        rating = len(rating_elements) if rating_elements else 0

        review = {
            "title_text": title_text,
            "rating": rating,
            "date": date,
            "review_body": review_text
        }
        review_list.append(review)

    return review_list

def get_rating_info(soup):
    """
    Gathers rating distribution from the rating section of the page.

    Parameters:
    soup: The parsed HTML of the page.
    
    Returns:
    dict: Keys are rating values (e.g., "5 stars"), values are the counts of such ratings.
    """
    rating_element = soup.find_all(name="div", class_="sc-c5b05e03-0 dLSnrv sc-a2d72622-0 keLsKG")

    ratings = {}
    for elements in rating_element:
        rating_value, rating_count = elements.get_text().strip('()').split('(')
        ratings[rating_value] = rating_count

    return ratings

def visit_product_pages(url):
    """
    Extracts product page links from the given HTML content.

    Parameters:
    url (str): HTML content of the webpage.
    
    Returns:
    list: A list of URLs (as strings) found within the specified container on the page.
    """
    soup = BeautifulSoup(url,  'html.parser')
    parent_container = soup.find(name="div", class_="sc-5d392fc9-0 fceyFV")
    links = []
    if parent_container:
        for child_div in parent_container.find_all('div', recursive=False):  
            a_tag = child_div.find('div').find('div').find('div').find('a')
            if a_tag and a_tag.has_attr('href'):
                links.append(a_tag['href'])

    return links

def fetch_product_links(base_link, end_page):
    """
    Collects product links from multiple pages on a website.

    Iterates over a range of pages from a base URL, making requests to each and gathering product links via 
    `visit_product_pages`. Stops and reports error if any page request fails.

    Parameters:
    - base_link (str): Starting URL for product listings.
    - end_page (int): Final page number to include.
    
    Returns:
    list: List of all product URLs found.
    """
    links = []
    pages_to_fetch = [base_link] + [f"{base_link}&page={page}" for page in range(2, end_page + 1)]

    for listings_url in pages_to_fetch:
        response = requests.get(listings_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to get the page: {listings_url}")
            return
        links += visit_product_pages(response.text)

    return links

if __name__ == "__main__":
    # List of relevant pages to be scraped
    urls_and_pages = [
        ("https://www.mediamarkt.es/es/search.html?query=wireless%20headphones", 4),
        ("https://www.mediamarkt.es/es/brand/jbl/auriculares", 8),
        ("https://www.mediamarkt.es/es/brand/sony/auriculares", 8),
        ("https://www.mediamarkt.es/es/brand/xiaomi/moviles-redmi/auriculares", 4),
    ]

    links = []
    for url, pages in urls_and_pages:
        print(f"Fetching product links from: {url} for {pages} pages")
        # Fetch the product links for each URL and number of pages, and add them to the links list
        fetched_links = fetch_product_links(url, pages)
        links += fetched_links
        print(f"Fetched {len(fetched_links)} links from {url}")
        logging.info(f"Fetched {len(fetched_links)} links from {url}")
        time.sleep(3)  
    
    print(f"Total number of product links fetched: {len(links)}")
    logging.info(f"Total number of product links fetched: {len(links)}")

    information = []
    for idx, link in enumerate(links, start=1):
        url_path = "https://www.mediamarkt.es" + link
        print(f"Processing product {idx}/{len(links)}: {url_path}")
        logging.info(f"Processing product {idx}/{len(links)}: {url_path}")

        response = requests.get(url_path, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            product_info = get_product_info(soup)
            rating_info = get_rating_info(soup)
            reviews = get_product_reviews(soup)

            information.append({
                "url": url_path,
                "info": product_info,
                "reviews": reviews,
                "rating_info": rating_info
            })
        else:
            print(f"Failed to get the page for link: {link}, status code: {response.status_code}")
            logging.error(f"Failed to get the page for link: {link}, status code: {response.status_code}")
    print("Scraping completed. Writing data to file.")
    logging.info("Scraping completed. Writing data to file.")

    with open("mediamarkt_products.json", "w", encoding='utf-8') as f:
        json.dump(information, f, ensure_ascii=False, indent=4)
        
    print("Data written to mediamarkt_products.json successfully.")
    logging.info("Data written to mediamarkt_products.json successfully.")