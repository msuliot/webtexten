# webtexten - WEB TEXT Extraction Node
import os
import sys
import logging
from config_manager import ConfigManager
from msuliot.base_64 import Base64 # https://github.com/msuliot/package.utils.git
from msuliot.data_loader_manager import DataLoaderManager # https://github.com/msuliot/package.data.loaders.git
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import random
import time

log_filename = 'webify.log'
logging.basicConfig(filename=log_filename,
                    filemode='a',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

converted_files_count = 0
visited_urls = set()
output_dir = '/Users/msuliot/text_output'
sys.setrecursionlimit(4000)

config_manager = ConfigManager()
config = config_manager.config


def save_text(filename, text, output_directory, source_file_path):
    global converted_files_count

    soup = BeautifulSoup(text, 'html.parser')
    text_elements = soup.select('p, h1, h2, h3, h4, h5, h6')
    text_content = ' '.join(element.get_text(separator=" ", strip=True) for element in text_elements)

    try:
        os.makedirs(output_directory, exist_ok=True)
        output_path = os.path.join(output_directory, filename)
        with open(output_path, 'w') as file:
            file.write(text_content)
        converted_files_count += 1 
        logging.info(f"File saved successfully text file: {output_path}") 

    except Exception as e:
        logging.error(f"Error saving text to {output_path}: {e}")

def convert_and_save(file_path, config):
    dlm = DataLoaderManager()
    text_output_directory = config.get('text_output_directory', '.')

    print(".", end="", flush=True)
    
    text = ""
    
    try:
        if file_path.lower().endswith('.pdf'):
            text = dlm.load_data(file_path, 'pdf')
        else:
            text = dlm.load_data(file_path, 'html')
        if text:
            save_text(create_filename(file_path), text, text_output_directory, file_path)
        else:
            logging.error(f"Could not convert file {file_path}")
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")


def check_skip_page(url):
    skip = False
    if url.lower().endswith('.zip'):
        skip = True

    if "?" in url:
        skip = True

    skip_substrings = [] # add substrings to skip here, comma separated
    for substring in skip_substrings:
        if substring in url:
            skip = True
        
    return skip


def crawl(url):
    global visited_urls
    if url in visited_urls:
        return
    
    if check_skip_page(url):
        visited_urls.add(url)
        return

    print(f"Crawling: {url}")
    visited_urls.add(url)

    html_content = fetch_html_from_url(url)
    if html_content:
        save_content(url, html_content)
        for link in extract_links(url, html_content):
            crawl(link)


def fetch_html_from_url(url):
    dlm = DataLoaderManager()
    # Throttle requests to avoid getting blocked
    sleep_time = random.uniform(0, 2)
    print(f"Sleeping for {sleep_time:.2f} seconds before fetching {url}")
    time.sleep(sleep_time)
    
    try:
        if url.lower().endswith('.pdf'):
            text = dlm.load_data(url, 'pdf')
        else:
            text = dlm.load_data(url, 'html')

        return text
        
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None


def extract_links(base_url, html_content):
    global visited_urls
    soup = BeautifulSoup(html_content, 'html.parser')
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(base_url, href)
        if is_same_domain(base_url, full_url) and full_url not in visited_urls:
            yield full_url


def is_same_domain(base_url, url):
    return urlparse(base_url).netloc == urlparse(url).netloc


def save_content(url, html_content):
    global output_dir, converted_files_count

    if url.lower().endswith('.pdf'):
        text_content = html_content
    else:
        soup = BeautifulSoup(html_content, 'html.parser')
        text_elements = soup.select('p, h1, h2, h3, h4, h5, h6')
        text_content = ' '.join(element.get_text(separator=" ", strip=True) for element in text_elements)

    filepath = os.path.join(output_dir, create_filename(url))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text_content)

    converted_files_count += 1
    print(f"Saved text content to: {filepath}")


def create_filename(url):
    if len(url) > 150:
        random_number = random.randint(10000000, 99999999)
        url = f"{url[:150]}_long_{str(random_number)}"

    url_base64 = Base64.encode(url)
    text_filename = f"{url_base64}.txt"
    return text_filename

def main(url):
    global converted_files_count
    parsed_url = urlparse(url)

    if parsed_url.path in ('', '/'):
        crawl(url)
    elif parsed_url.path.lower().endswith(('.pdf', '.html', '.htm')):
        convert_and_save(url, config)
    else:
        return "Other"

    logging.info(f"Total converted files: {converted_files_count}")
    print(f"\nTotal converted files: {converted_files_count}")

if __name__ == "__main__":
    print("\nProcess started:", end=" ")
    url ='https://themarkt.com/'
    main(url)
    print("Webtexten process complete. Check logs for details.")