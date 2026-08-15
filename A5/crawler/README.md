## Description

This project is an asynchronous Python script designed to scrape websites for privacy policies and DNSMPI (Do Not Sell My Personal Information) links. The script uses Playwright to automate browser actions and BeautifulSoup for extracting text content from HTML pages. The output is a structured JSON file containing the results.

## Features

- Extracts Privacy Policy links and their text content.
- Identifies and extracts DNSMPI (Do Not Sell My Personal Information) links and text.
- Supports concurrent scraping with a configurable task limit.
- Handles errors gracefully and logs detailed information about failures.
- Saves the results in a JSON file with structured data for further analysis.

## Methodology

1. Input: A CSV file containing URLs and their classifications (e.g., university, organization, etc.).
2. Concurrency: The script uses an asyncio semaphore to limit the number of concurrent browser instances.
3. Scraping Process:
   a. Launch a headless browser using Playwright.
   b. Navigate to the homepage of each URL.
   c. Search for links matching privacy-related keywords such as "Privacy Policy" or "Do Not Sell".
   d. Visit these links and extract text content using BeautifulSoup.
   e. Store the extracted text and metadata in the output JSON file.
4. Output: A JSON file containing:
   a. URL and classification.
   b. Privacy policy link and text content (if available).
   c. DNSMPI link and text content (if available).
   d. Errors encountered during the process.

## Install dependencies for crawler

Required Dependencies:

1. playwright
2. beautifulsoup4
3. asyncio
4. tldextract

Install Pip If Needed
`apt install python3-pip`

Install Playwright and Playwright Depenedencies
`pip install playwright`
`playwright install`

Install BeautifulSoup4 If Needed
`pip install beautifulsoup4`

Install Asyncio If Needed
`pip install asyncio`

Install Tldextract If Needed
`pip install tldextract`

## Important information

To view lengthy privacy policy texts in common editors, max Tokenization must be increased to 2,000.000. Below are instructions for our selected text editor VSCode:
File --> Preferences --> Settings --> Search `Max Tokenization` set to `2,000,000`

## How to Use

Below are the steps to use the file

### Prepare the input file

The program takes a CSV file with the following columns:

1. URL - Link to website homepage
2. Category - Tag to categories the results

### Run the script

`python scraper.py input.csv output.json`

- Additional Flags: `--max_concurrent_tasks` is used to set the amount of asychronous processes. We recommmend using the default value of 5. However, this can be increased or decreased depending on the capabilities of your machine.

## Disclaimer

Based on developer analysis, the crawler has a 91% success rate but limitations exists. Due to HTML specific and heuristic limitations, the crawler isn't always able to identify privacy policy and dnsmpi links.

## Contributions

## Logan Martin (logmartin)

Logan created the `crawler.py` to analyze websites for privacy policy and dnsmpi statements. The `websites.csv` file was formatted to be taken as an input and the output was formatted to the schema required for the analysis tools.

## Carlo Velarde (cvelarde)

Carlo created a list of university websites within the defined groups.
