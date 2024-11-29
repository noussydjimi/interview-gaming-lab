from urllib.parse import urlparse, urljoin
import sys
sys.path.append('/usr/local/lib/python3.11/site-packages')
import requests
from bs4 import BeautifulSoup
import argparse
import json



def validate_url(url):
    """Check if a URL has a valid scheme."""
    parsed = urlparse(url)
    #print(dir(parsed))
    # print(type(parsed))
    ALLOWED_PROTOCOLE = ["http", "https"]
    if parsed.scheme not in ALLOWED_PROTOCOLE:
        print(f"Error: Invalid URL scheme '{parsed.scheme}'. Only 'http' and 'https' are allowed.")
        return False
    print(f"Success: The URL scheme '{parsed.scheme}' is allowed.")
    return parsed.scheme in ALLOWED_PROTOCOLE


def fetch_html(url):
    """Fetch HTML content from a URL."""
    response = requests.get(url, timeout=10)
    #print(dir(response))
    return response.text

def extract_links(html, base_url):
    """Extract all absolute URLs from HTML content."""
    soup = BeautifulSoup(html, "html.parser")
    #print(soup)
    links = set()
    for hyperlinks in soup.find_all("a", href=True):
        absolute_url = urljoin(base_url, hyperlinks["href"])
        links.add(absolute_url)
    return links

def format_output(links, base_url, output_format):
    """Format links as stdout or JSON."""
    if output_format == "stdout":
        for link in links:
            print(link)
    elif output_format == "json":
        domain = f"{urlparse(base_url).scheme}://{urlparse(base_url).netloc}"
        #print(domain)
        relative_links = [urlparse(link).path for link in links]
        #print(relative_links)
        return {domain: relative_links}




def main():
    parser = argparse.ArgumentParser(description="Extract links from web pages.")
    parser.add_argument("-u", "--urls", nargs="+", required=True, help="URLs to process")
    parser.add_argument("-o", "--output", choices=["stdout", "json"], required=True, help="Output format")
    args = parser.parse_args()

    all_links = {}
    for url in args.urls:
        validate_url(url)
        html = fetch_html(url)
        if html:
            links = extract_links(html, url)
            if args.output == "stdout":
                format_output(links, url, "stdout")
            elif args.output == "json":
                all_links.update(format_output(links, url, "json"))

    if args.output == "json":
        print(json.dumps(all_links, indent=4))



if __name__ == "__main__":
    main()


