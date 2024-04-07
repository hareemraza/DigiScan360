import re
import os
import time
import requests
import json
import logging
import random
from argparse import ArgumentParser

from urllib.parse import urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-es,es;q=0.9,en;q=0.8",
    "Referer": "https://www.amazon.es/",
    "Connection": "keep-alive",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "no-cache",
    # Cookie will be added dynamically after the first request
}
# Create a session object
global_session = requests.Session()
global_session.headers.update(headers)

# Setting up basic configuration for logging
logging.basicConfig(
    filename="amazon.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s"
)


# Function to read JSON data from a file
def read_json_file(file_path):
    """
    Reads and returns the JSON data from the specified file.

    Parameters:
    - file_path (str): The path to the file from which to read the JSON data.

    Returns:
    - The JSON data read from the file if successful, otherwise an empty list.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from file: {file_path}")
        print(f"Error decoding JSON from file: {file_path}")
        return []


# Function to write JSON data to a file
def write_json_file(file_path, data):
    """
    Writes the given JSON data to the specified file.

    Parameters:
    - file_path (str): The path to the file where the JSON data will be written.
    - data: The JSON data to write.
    """
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logging.error(f"Error writing JSON to file: {file_path}, Error: {e}")
        print(f"Error writing JSON to file: {file_path}, Error: {e}")


def get_links_from_page(query, url):
    """
    Fetches and returns product and pagination links from a given webpage.

    Parameters:
    - query (str): The search query to use for finding product links.
    - url (str): The URL of the webpage to scrape.

    Returns:
    - A list containing two lists: the first with product links and the second with pagination links.
      Returns None if an error occurs.
    """
    response = global_session.get(url)

    if response.status_code != 200:
        print(f"ERROR: Status code for {url} is {response.status_code}")
        logging.error(f"ERROR: Status code for {url} is {response.status_code}")
        return [], []

    soup = BeautifulSoup(response.text, "lxml")
    main_div = soup.find(
        name="div", attrs={"class": "s-main-slot s-result-list s-search-results sg-row"}
    )
    anchors = main_div.find_all("a", class_="a-link-normal s-no-outline")
    product_links = [anchor.get("href") for anchor in anchors]
    full_product_links = [f"https://www.amazon.es{link}" for link in product_links]
    formatted_links = []

    for link in full_product_links:
        if "sspa" in link or link.startswith("https"):
            formatted_link = link
        else:
            url_obj = urlparse(link)
            formatted_link = f"{url_obj.scheme}://{url_obj.netloc}{url_obj.path}"
        formatted_links.append(formatted_link)

    logging.info(f"Found {len(formatted_links)} links on {url}")
    print(f"Found {len(formatted_links)} links on {url}")
    pagination_links = []
    found_pages = set()
    pagination_element = soup.find("span", class_="s-pagination-strip")
    if pagination_element:
        template = f"https://www.amazon.es/s?k={query}&page="
        for anchor in pagination_element.find_all("a"):
            link = anchor.get("href")
            matched_pattern = re.search("page=(\d)", link)
            if matched_pattern:
                page_number = int(matched_pattern.group(1))
                if page_number not in found_pages:
                    pagination_links.append(f"{template}{page_number}")
                    found_pages.add(page_number)
    return formatted_links, pagination_links


def gather_all_product_links(query, num_visited_pages=5):
    """
    Crawls and gathers all product links based on the specified query and limit on visited pages.

    Parameters:
    - query (str): The search query to use for finding product links.
    - num_visited_pages (int): The maximum number of pages to visit.

    Returns:
    - a list of all product links found
    """
    # replace spaces with '+' for the query
    query = query.replace(" ", "+")
    url = "https://www.amazon.es/s?k=" + query
    # queue of URLs to visit
    visit_queue = [url]
    # set to store all product links
    all_product_links = set()
    # track visited pages
    visited = []
    while visit_queue and len(visited) < num_visited_pages:
        current_url = visit_queue.pop(0)
        # skip if already visited
        if current_url in visited:
            continue
        visited.append(current_url)
        logging.info(f"Crawling {current_url}")
        print(f"Crawling {current_url}")
        # scrape the page for product links
        product_links, pagination_links = get_links_from_page(query, current_url)
        if len(product_links) != 0:
            all_product_links.update(product_links)
            visit_queue.extend(pagination_links)
        else:
            # retry once
            logging.debug(f"Retrying {current_url}")
            print(f"Retrying {current_url}")
            # if no product links found, wait for a minute and try again
            time.sleep(60)
            product_links, pagination_links = get_links_from_page(query, current_url)
            if len(product_links) != 0:
                all_product_links.update(product_links)
                visit_queue.extend(pagination_links)
            else:
                logging.warning(f"No links found for {current_url}")
                print(f"No links found for {current_url}")
        # random delay between requests
        delay = random.randint(3, 10)
        time.sleep(delay)
        # random chance to simulate user pause
        if random.random() < 0.3:
            time.sleep(random.randint(10, 30))
    all_product_links = list(all_product_links)
    with open("amazon_product_links.txt", "w", encoding="utf-8") as f:
        f.writelines([link + "\n" for link in all_product_links])
    return all_product_links


def scrape_product_page(soup):
    title_tag_id = ["productTitle", "title"]
    for tag_id in title_tag_id:
        title = soup.find(id=tag_id)
        if title is not None:
            break
    title = title.get_text().strip()

    try:
        overall_rating_tag_id = "averageCustomerReviews"
        overall_rating = (
            soup.find(id=overall_rating_tag_id)
            .find(class_="a-size-base a-color-base")
            .get_text()
            .strip()
        )
    except:
        overall_rating = None

    img_tag_id = "imgTagWrapperId"
    img_tag = soup.find(id=img_tag_id)
    img_url = img_tag.find("img").get("src")

    seller_tag_id = "bylineInfo"
    seller = soup.find(id=seller_tag_id).get("href")
    if "?" in seller:
        seller = seller[0 : seller.index("?")]
    seller = "https://www.amazon.es" + seller

    try:
        price_tag_id = "corePriceDisplay_desktop_feature_div"
        price = soup.find(id=price_tag_id)
        price = price.find("span", class_="aok-offscreen").get_text().strip()
        price = re.search("\d+([\.,]\d+)?", price).group()
    except:
        price = None

    try:
        num_reviews_tag_id = "acrCustomerReviewText"
        num_reviews_tag = soup.find(id=num_reviews_tag_id).get_text().strip()
        num_reviews = re.search("\d+([\.,]\d+)?", num_reviews_tag).group()
    except:
        num_reviews = None

    try:
        rating_histogram_tag_id = "cm_cr_dp_d_rating_histogram"
        rating_histogram_tag = soup.find(id=rating_histogram_tag_id).find(
            id="histogramTable"
        )
        histogram = {}
        for i, div in enumerate(rating_histogram_tag.find_all("div", class_="a-meter")):
            value = div.get("aria-valuenow")
            histogram[5 - i] = value
    except:
        histogram = None

    try:
        more_reviews_tag = soup.find(string="Ver más opiniones").parent
        more_reviews_link = "https://www.amazon.es" + more_reviews_tag.get("href")
    except:
        more_reviews_link = None

    return {
        "title": title,
        "rating": overall_rating,
        "img_url": img_url,
        "seller_url": seller,
        "price": price,
        "num_reviews": num_reviews,
        "rating_histogram": histogram,
        "more_reviews": more_reviews_link,
    }


def scrape_products(product_links):
    sessions = [
        requests.Session(),
        requests.Session(),
        requests.Session(),
        requests.Session(),
        requests.Session(),
    ]
    products = read_json_file("amazon_products.json")
    i = len(products)
    n = 0
    for url in tqdm(product_links[i:]):
        while True:
            try:
                logging.info(f"Scraping {url}")
                print(url)
                # rotate sessions
                response = sessions[n % 5].get(url, headers=headers)
                sessions[n % 5].close()
                sessions[n % 5] = requests.Session()
                n += 1

                if response.status_code != 200:
                    logging.error(f"Status code {response.status_code} for {url}")
                    print(response.status_code)
                    raise Exception("Status code 503")

                soup = BeautifulSoup(response.text)
                product_info = scrape_product_page(soup)
                products.append(product_info)
                write_json_file("amazon_products.json", products)
                break
            except:
                # retry
                time.sleep(30)
        # random delay between requests
        time.sleep(random.randint(3, 10))
        # random chance to simulate user pause
        if random.random() < 0.3:
            time.sleep(random.randint(10, 30))

    return products


def extract_review_information(review_tag):
    rating_tag = (
        review_tag.find("i", attrs={"data-hook": "review-star-rating"})
        .get_text()
        .strip()
    )
    rating = re.match("\d(,\d)?", rating_tag).group()

    title_tag = review_tag.select(".review-title-content span")
    title = title_tag[-1].get_text().strip()

    review_date_tag = review_tag.find("span", attrs={"data-hook": "review-date"})
    review_date = review_date_tag.get_text().strip()

    review_body_tag = review_tag.find("span", attrs={"data-hook": "review-body"})
    if review_body_tag:
        review_body = review_body_tag.get_text().strip()
    else:
        review_body = None

    helpful_tag = review_tag.find("span", attrs={"data-hook": "helpful-vote-statement"})
    if helpful_tag:
        num_helpful = helpful_tag.get_text().strip()
        num_helpful = re.search("\d+", num_helpful)
        if num_helpful:
            # more than 1 found this helpful
            num_helpful = num_helpful.group()
        else:
            # A person found this helpful
            num_helpful = 1
    else:
        # nobody found it helpful
        num_helpful = 0

    return {
        "rating": rating,
        "title": title,
        "date": review_date,
        "body": review_body,
        "num_helpful": num_helpful,
    }


def scrape_reviews(products):
    sessions = [
        requests.Session(),
        requests.Session(),
        requests.Session(),
        requests.Session(),
        requests.Session(),
    ]

    reviews = read_json_file("amazon_reviews.json")
    i = len(reviews)
    n = 0

    for product in tqdm(products[i:]):
        while True:
            url = product["more_reviews"]
            if url is None:
                break
            review_list = {"url": url, "reviews": []}
            logging.info(f"Scraping {url}")
            print(url)

            try:
                response = sessions[n % 5].get(url, headers=headers)
                sessions[n % 5].close()
                sessions[n % 5] = requests.Session()
                n += 1

                if response.status_code != 200:
                    logging.error(f"Status code {response.status_code} for {url}")
                    raise Exception("Status code 503")

                soup = BeautifulSoup(response.text)
                review_tags = soup.find_all(
                    "div",
                    attrs={"data-hook": "review"},
                    class_="a-section review aok-relative",
                )
                if "valoraciones de Espa" in soup.get_text():
                    reviews.append(review_list)
                    write_json_file("reviews.json", reviews)
                elif len(review_tags) == 0:
                    continue
                else:
                    for review_tag in review_tags:
                        if soup.find("span", class_="cr-translated-review-content"):
                            continue
                        review_info = extract_review_information(review_tag)
                        review_list["reviews"].append(review_info)
                    reviews.append(review_list)
                    write_json_file("amazon_reviews.json", reviews)
                break
            except:
                # retry
                time.sleep(30)
        # random delay between requests
        time.sleep(random.randint(3, 10))
        # random chance to simulate user pause
        if random.random() < 0.3:
            time.sleep(random.randint(10, 30))

    return reviews


def crawl_and_scrape_amazon(query):
    all_product_links = gather_all_product_links(query)
    logging.info(f"Total links gathered: {len(all_product_links)}")
    products = scrape_products(all_product_links)
    logging.info(f"Total products scraped: {len(products)}")
    reviews = scrape_reviews(products)
    logging.info(f"Total reviews scraped: {len(reviews)}")

    return all_product_links, products, reviews


if __name__ == "__main__":
    # parse search query from command line argument
    parser = ArgumentParser(description="Amazon Web Scraper")
    parser.add_argument(
        "query", type=str, help="Search query to scrape Amazon for product links"
    )
    args = parser.parse_args()

    crawl_and_scrape_amazon(args.query)
    global_session.close()
