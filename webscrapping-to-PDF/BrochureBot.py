#!/usr/bin/env python3

# ==================================================================================
# An Automation script that crawls a website, saves HTML/assets, generates PDF brochure.
# Uses WeasyPrint for static sites, Playwright for dynamic sites.
# Replace "https://example.com" with your target URL.
# Version 1.2
# ==================================================================================

import os  # File and directory operations
import scrapy  # Scrapy framework for crawling
import requests  # HTTP requests for site type detection
from scrapy.crawler import CrawlerProcess  # Run Scrapy spiders
from scrapy.utils.project import get_project_settings  # Get Scrapy settings
from urllib.parse import urljoin, urlparse  # Parse and join URLs
import logging  # Logging messages
from weasyprint import HTML  # Convert HTML to PDF
from playwright.async_api import async_playwright  # Playwright for dynamic sites
import sys, itertools, threading, time  # System, spinner, threading, timing
import asyncio  # Async operations
import json  # Read/write JSON files
from threading import Event  # Thread event signaling

class BrochureBot(scrapy.Spider):  # Define spider class
    name = 'brochurebot'  # Spider name

    custom_settings = {  # Scrapy settings for this spider
        "ROBOTSTXT_OBEY": False,  # Ignore robots.txt
        "DOWNLOAD_DELAY": 1,  # Delay between requests
        "LOG_ENABLED": True,  # Enable logging
        "LOG_LEVEL": "INFO",  # Log level
        "LOG_FILE": "crawler.log",  # Log file path
        "USER_AGENT": "BrochureBot/1.2 (Content Analysis; mailto:your-email@example.com)",  # Custom user agent
        # Disable Playwright handlers for Scrapy
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy.core.downloader.handlers.http.HTTPDownloadHandler",
            "https": "scrapy.core.downloader.handlers.http.HTTPDownloadHandler",
        }
    }

    def __init__(self, start_url=None, *args, **kwargs):  # Spider initialization
        super(BrochureBot, self).__init__(*args, **kwargs)  # Call parent constructor
        self.start_urls = [start_url] if start_url else ['https://example.com']  # Set start URL
        self.allowed_domains = [urlparse(self.start_urls[0]).netloc]  # Restrict to domain
        self.base_dir = "website_content"  # Directory for saved files
        os.makedirs(self.base_dir, exist_ok=True)  # Create directory if needed
        self.html_files = []  # List of saved HTML files
        self.is_dynamic = False  # Site type flag
        self.metadata = {  # Metadata for PDF generation
            'start_url': self.start_urls[0],
            'base_dir': self.base_dir,
            'is_dynamic': self.is_dynamic
        }
        self.detect_site_type()  # Check if site is static or dynamic

    def detect_site_type(self):  # Determine if site is static or dynamic
        try:
            resp = requests.get(
                self.start_urls[0],
                headers={"User-Agent": self.custom_settings["USER_AGENT"]},
                timeout=10,
            )
            raw_html = resp.text.lower()  # Get HTML content
            # Check for SPA indicators
            if "<a " not in raw_html and ("<script" in raw_html or "id=\"root\"" in raw_html or "id=\"app\"" in raw_html):
                self.is_dynamic = True  # Mark as dynamic
                self.logger.info("⚡ Detected dynamic/JS-heavy site (SPA). Will use Playwright for PDF.")
            else:
                self.is_dynamic = False  # Mark as static
                self.logger.info("Detected static site. Using WeasyPrint for PDF.")
        except Exception as e:
            self.logger.warning(f"Could not detect site type, defaulting to static: {e}")  # Log error
            self.is_dynamic = False  # Default to static
        self.metadata['is_dynamic'] = self.is_dynamic  # Update metadata

    def start_requests(self):  # Start crawling from URLs
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)  # Request each start URL

    def parse(self, response):  # Parse each crawled page
        if urlparse(response.url).netloc not in self.allowed_domains:  # Skip external domains
            return

        path = urlparse(response.url).path  # Get URL path
        if path.endswith('/') or path == '':  # If directory or root
            path = os.path.join(path, 'index.html')  # Use index.html
        file_path = os.path.join(self.base_dir, path.lstrip('/'))  # Local file path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure directory exists

        content_type = response.headers.get(b"Content-Type", b"").decode("utf-8")  # Get content type

        if "text/html" in content_type:  # Only process HTML
            html = response.text  # Get HTML content
        else:
            self.logger.info(f"Skipping non-text response: {response.url} ({content_type})")  # Log skip
            return

        # Download and fix asset links
        for tag, attr in [('img', 'src'), ('link', 'href'), ('script', 'src')]:
            for asset in response.css(f"{tag}::attr({attr})").getall():  # Find asset URLs
                asset_url = urljoin(response.url, asset)  # Make absolute URL
                parsed = urlparse(asset_url)
                if parsed.netloc == self.allowed_domains[0]:  # Only local assets
                    local_path = os.path.join(self.base_dir, parsed.path.lstrip('/'))  # Local asset path
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)  # Ensure asset dir exists
                    yield scrapy.Request(asset_url, callback=self.save_asset, cb_kwargs={'file_path': local_path})  # Download asset
                    rel_path = os.path.relpath(local_path, os.path.dirname(file_path))  # Relative path for HTML
                    html = html.replace(asset, rel_path)  # Update asset link

        with open(file_path, "w", encoding="utf-8") as f:  # Save HTML file
            f.write(html)
        self.html_files.append(file_path)  # Track saved HTML

        # Only follow links for static sites
        if not self.is_dynamic:
            skip_exts = (".zip", ".exe", ".wav", ".mp3", ".mp4", ".avi", ".mov")  # File types to skip
            for link in response.css("a::attr(href)").getall():  # Find all links
                parsed = urlparse(link)
                if parsed.scheme in ["http", "https"] or link.startswith("/"):  # Valid links
                    if not link.lower().endswith(skip_exts):  # Skip unwanted files
                        yield response.follow(link, self.parse)  # Follow link

    def save_asset(self, response, file_path):  # Save downloaded asset
        with open(file_path, 'wb') as f:
            f.write(response.body)
        logging.info(f"Saved asset: {file_path}")  # Log asset saved

    def closed(self, reason):  # Called when spider finishes
        self.metadata['html_files'] = self.html_files  # Add HTML files to metadata
        metadata_path = os.path.join(self.base_dir, 'metadata.json')  # Metadata file path
        with open(metadata_path, 'w') as f:
            json.dump(self.metadata, f)  # Save metadata as JSON
        logging.info(f"Metadata saved for PDF generation: {metadata_path}")  # Log metadata saved

async def generate_pdf_async(metadata):  # Async PDF generation
        pdf_path = os.path.join(metadata['base_dir'], "website_brochure.pdf")  # PDF output path

        if metadata['is_dynamic']:  # Use Playwright for dynamic sites
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)  # Launch browser
                page = await browser.new_page()  # New browser page
                page.set_default_timeout(120000)  # Set timeout
                print("    Loading page for PDF generation...")
                await page.goto(metadata['start_url'], wait_until="networkidle", timeout=120000)  # Load page
                print("    Generating PDF...")
                await page.pdf(
                    path=pdf_path, 
                    format="A4",
                    print_background=True,
                    margin={"top": "1cm", "right": "1cm", "bottom": "1cm", "left": "1cm"})  # Save as PDF
                await browser.close()  # Close browser
            print(f"    PDF brochure created with Playwright: {pdf_path}")  # Print success
        else:  # Use WeasyPrint for static sites
            print("    Combining HTML files for PDF...")
            combined_html = "<html><head><meta charset='utf-8'></head><body>"  # Start HTML
            for html_file in metadata.get('html_files', []):  # Add each HTML file
                if os.path.exists(html_file):
                    with open(html_file, encoding="utf-8") as f:
                        combined_html += f"<div class='page'>{f.read()}</div><p style='page-break-after:always;'></p>"
            combined_html += "</body></html>"  # End HTML
            print("    Generating PDF with WeasyPrint...")
            HTML(string=combined_html, base_url=metadata['base_dir']).write_pdf(pdf_path)  # Save PDF
            logging.info(f"PDF brochure created with WeasyPrint: {pdf_path}")  # Log success

def generate_pdf(metadata):  # Synchronous PDF generation wrapper
    try:
        asyncio.run(generate_pdf_async(metadata))  # Run async PDF generator
        return True  # Success
    except Exception as e:
        print(f"    Error during PDF generation: {e}")  # Print error
        return False  # Failure

# -------------------------
# Spinner Wrapper
# -------------------------
def spinner_task(done_event, current_status):  # Spinner animation for status
    spinner = itertools.cycle(["|", "/", "-", "\\"])  # Spinner characters

    while not done_event.is_set():  # Loop until done
        sys.stdout.write(f"\r{current_status[0]}... {next(spinner)}")  # Print spinner
        sys.stdout.flush()
        time.sleep(0.2)  # Wait

    sys.stdout.write("\rProcess completed! \n")  # Print completion
    sys.stdout.flush()

if __name__ == "__main__":  # Main script entry
    start_url = "https://example.com/"  # Website to crawl

    current_status = ["Crawling in progress"]  # Status message
    done_event = Event()  # Event for spinner

    spinner_thread = threading.Thread(target=spinner_task, args=(done_event, current_status))  # Spinner thread
    spinner_thread.start()  # Start spinner

    process = CrawlerProcess(get_project_settings())  # Create Scrapy process
    process.crawl(BrochureBot, start_url=start_url)  # Add spider to process

    print("Starting web crawler...")  # Print start message
    process.start()  # Start crawling

    metadata_path = os.path.join("website_content", 'metadata.json')  # Metadata file path
    if os.path.exists(metadata_path):  # If metadata exists
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)  # Load metadata

        current_status[0] = "Generating PDF"  # Update spinner status
        time.sleep(1)  # Pause for spinner

        print("\nStarting PDF generation...")  # Print PDF start
        success = generate_pdf(metadata)  # Generate PDF
        if success:
            print("PDF generation completed successfully!")  # Print success
        else:
            print("PDF generation failed. Check the error above.")  # Print failure
    else:
        print("\nNo metadata found for PDF generation.")  # Print missing metadata
    
    # Signal completion
    done_event.set()
    spinner_thread.join()