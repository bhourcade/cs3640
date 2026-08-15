import asyncio
import argparse
import hashlib
import json
import csv
import re
import logging
from urllib.parse import urljoin
from tldextract import extract
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Utility functions
def clean_url(url):
    """Generate a clean filename-safe hash for a URL."""
    return hashlib.md5(url.encode("utf-8")).hexdigest()

def extract_domain(url):
    """Extract the main domain of a URL."""
    parsed = extract(url)
    return ".".join(filter(None, [parsed.domain, parsed.suffix]))

def extract_plain_text(html_content):
    """Extract main body text from HTML using BeautifulSoup."""
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Prioritize extracting content from <main>, <article>, or similar tags
    main_content = None
    for tag_name in ["main", "article", "section"]:
        main_content = soup.find(tag_name)
        if main_content:
            break
    
    # If no <main>, <article>, or <section> is found, fall back to the largest <div>
    if not main_content:
        divs = soup.find_all("div")
        main_content = max(divs, key=lambda div: len(div.get_text(strip=True)), default=None)
    
    if main_content:
        # Remove unwanted tags inside the main content
        for tag in main_content(["script", "style", "header", "footer", "nav", "aside"]):
            tag.decompose()
        
        # Get clean text from the main content
        text = main_content.get_text(separator=" ", strip=True)
    else:
        # Fallback: Get plain text from the entire page if no main content is identified
        text = soup.get_text(separator=" ", strip=True)
    
    # Remove excessive whitespace or newlines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return " ".join(lines)

async def scrape_url_with_semaphore(semaphore, playwright, url):
    """Scrape URL with concurrency control using a semaphore."""
    async with semaphore:
        return await scrape_url(playwright, url)

async def scrape_url(playwright, university):
    homepage_url = university["url"]
    """Scrape the given URL to find privacy policies and DNSMPI links."""
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()

    result = {
        "url": homepage_url,
        "class": university["type"],
        "status": False,
        "privacy_policy": None,
        "privacy_policy_text": "",
        "dnsmpi": None,
        "dnsmpi_text": None,
        "errors": []
    }
    try:
        await page.goto(homepage_url, timeout=60000)
        logger.info(f"Visiting: {homepage_url}")

        privacy_keywords = ['privacy policy', 'privacy notice', 'privacy']
        # Heuristics to find privacy policy links
        known_privacy_links = []
        for keys in privacy_keywords:
            links = await page.locator(f"a:has-text('{keys}')").all()
            for link in links:
                href = await link.get_attribute("href") or ""
                # Check for privacy policy link
                privacy_link_url = urljoin(homepage_url, href)
                if keys == 'privacy':
                    if result.get('privacy_policy') is None:
                        result['privacy_policy'] = privacy_link_url
                else:
                    result['privacy_policy'] = privacy_link_url

                if privacy_link_url not in known_privacy_links:
                    # Visit the privacy policy link and extract its content
                    await page.goto(privacy_link_url, timeout=300000)
                    html_content = await page.content()
                    privacy_content = extract_plain_text(html_content)    
                    if keys == 'privacy' and result["privacy_policy_text"] == "":
                        result["privacy_policy_text"] = privacy_content
                    elif privacy_content not in result["privacy_policy_text"]:
                        result["privacy_policy_text"] += privacy_content
                        known_privacy_links.append(privacy_link_url)
                    if result["privacy_policy_text"] == "":
                        result["status"] = False
                    else:
                        result["status"] = True
                    break

    except Exception as e:
        logger.error(f"Error while processing {homepage_url}: {e}")
        result["errors"].append(str(e))

    try:
        dnsmpi_keyword = [
            "California Privacy Rights",
            "dnsmpi",
            "do not sell",
            "do not share",
        ]
        
        await page.goto(homepage_url, timeout=60000)
        logger.info(f"Revisiting: {homepage_url}")
        known_dnsmpi_links = []
        for keys in dnsmpi_keyword:
            links = await page.locator(f"a:has-text('{keys}')").all()
            if True == True:
                for link in links:
                    href = await link.get_attribute("href") or ""
                    dnsmpi_url = urljoin(homepage_url, href)
                    logger.info(f"Found DNSMPI link: {dnsmpi_url}")
                    result["dnsmpi"] = dnsmpi_url
                    if dnsmpi_url not in known_dnsmpi_links:
                        await page.goto(dnsmpi_url, timeout=60000)
                        html_content = await page.content()
                        dnsmpi_extracted_text = extract_plain_text(html_content)
                        result["dnsmpi_text"] = dnsmpi_extracted_text
                        known_dnsmpi_links.append(dnsmpi_url)
                        break
    except Exception as e:
        logger.error(f"Error while processing {homepage_url}: {e}")
        result["errors"].append(str(e))

    finally:
        await page.close()
        await context.close()
        await browser.close()

    return result


async def main(input_file, output_file, max_concurrent_tasks=5):
    """Main function to scrape all URLs with limited concurrency."""
    semaphore = asyncio.Semaphore(max_concurrent_tasks)  # Limit the number of concurrent tasks

    universities = []

    with open(input_file, "r", encoding="utf-8") as f:
        #urls = [line.strip() for line in f.readlines() if line.strip()]
        csv_reader = csv.reader(f)
        for row in csv_reader:
            university = {
                "url": row[0],
                "type": row[1],
            }
            universities.append(university)
                 
    async with async_playwright() as playwright:
        tasks = [scrape_url_with_semaphore(semaphore, playwright, uni) for uni in universities]
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)

    results = []

    for result in raw_results:
        if isinstance(result, Exception):
            results.append({"error": str(result)})
        else:
            results.append(result)
    # Save all results to a single JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)\
    

    logger.info(f"All results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape websites for privacy policies and DNSMPI links.")
    parser.add_argument("input_file", help="Path to file containing URLs (one URL per line).")
    parser.add_argument("output_file", help="Path to output JSON file.")
    parser.add_argument("--max_concurrent_tasks", type=int, default=5, help="Maximum number of concurrent tasks.")
    args = parser.parse_args()

    # Run the async main function
    asyncio.run(main(args.input_file, args.output_file, args.max_concurrent_tasks))
