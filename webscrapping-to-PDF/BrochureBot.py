#!/usr/bin/env python3  # Shebang for Python 3 execution

# ==================================================================================
# This Automation Script is a Scrapy spider that crawls a website, saves its HTML content and assets,
# and generates a PDF brochure from the collected HTML files using WeasyPrint.
# Make sure to replace "https://example.com" with the actual URL you want to crawl.
# ==================================================================================

import os  # OS operations for file and directory handling
import scrapy  # Scrapy framework for web crawling
from scrapy.crawler import CrawlerProcess  # CrawlerProcess to run spiders without project
from scrapy.utils.project import get_project_settings  # Get Scrapy project settings
from urllib.parse import urljoin, urlparse  # URL parsing and joining utilities
import logging  # Logging for status and errors
from weasyprint import HTML  # WeasyPrint for PDF generation from HTML

class WebsiteSpider(scrapy.Spider):  # Define the spider class
    name = 'website_crawler'  # Name of the spider
    
    custom_settings = {  # Custom settings for the spider
        "ROBOTSTXT_OBEY": True,     # Respect robots.txt rules
        'DOWNLOAD_DELAY': 1,         # Delay between requests
        'LOG_ENABLED': True, # Enable logging
        'LOG_LEVEL': 'INFO', # Set log level to INFO
        'LOG_FILE': 'crawler.log', # Log output to a file
        'USER_AGENT': 'BrochureBot/1.0 (Content Analysis; mailto:your-email@example.com)', # Custom user agent
    }

    def __init__(self, start_url=None, *args, **kwargs):  # Spider initialization
        super(WebsiteSpider, self).__init__(*args, **kwargs)  # Call parent constructor
        self.start_urls = [start_url] if start_url else ['https://example.com']  # Set start URLs
        self.allowed_domains = urlparse(self.start_urls[0]).netloc  # Restrict to domain
        self.base_dir = "website_content"  # Directory to save website content
        os.makedirs(self.base_dir, exist_ok=True)  # Create base directory if not exists
        self.html_files = []  # keep track of saved HTML for PDF compilation

    def parse(self, response):  # Main parsing method for each response
        # Ensure the bot only stays within domain
        if urlparse(response.url).netloc != self.allowed_domains:  # Skip if not allowed domain
            return

        # File path (mirroring structure)
        path = urlparse(response.url).path  # Get URL path
        if path.endswith('/') or path == '':  # If path is directory or empty
            path = os.path.join(path, 'index.html')  # Use index.html for directories
        file_path = os.path.join(self.base_dir, path.lstrip('/'))  # Full local file path

        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure directory exists

        # Check to make sure we are dealing with HTML content
        content_type = response.headers.get(b"Content-Type", b"").decode("utf-8")  # Get content type

        if "text/html" in content_type:  # Only process HTML content
            html = response.text  # process as HTML
        else: 
            self.logger.info(f"Skipping non-text response: {response.url} ({content_type})")  # Log skipped non-HTML
            return  # don't process further

        # Fix asset links (images, CSS, JS -> local paths)
        for tag, attr in [('img', 'src'), ('link', 'href'), ('script', 'src')]:  # Iterate asset tags
            for asset in response.css(f"{tag}::attr({attr})").getall():  # Get asset URLs
                asset_url = urljoin(response.url, asset)  # Build absolute asset URL
                parsed = urlparse(asset_url)  # Parse asset URL

                if parsed.netloc == self.allowed_domains:  # only download local assets
                    local_path = os.path.join(self.base_dir, parsed.path.lstrip('/'))  # Local asset path
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)  # Ensure asset directory exists

                    yield scrapy.Request(asset_url, callback=self.save_asset, cb_kwargs={'file_path': local_path})  # Download asset
                    # Replace URL with local path
                    rel_path = os.path.relpath(local_path, os.path.dirname(file_path))  # Relative path for HTML
                    html = html.replace(asset, rel_path)  # Update asset link in HTML

        # Save modified HTML
        with open(file_path, "w", encoding="utf-8") as f:  # Open file for writing
            f.write(html)  # Write HTML content

        self.html_files.append(file_path)  # Track saved HTML file

        # Follow links but skip certain file types and external domains non webservers
        
        # Define file extensions to skip
        skip_exts = (".zip", ".exe", ".wav", ".mp3", ".mp4", ".avi", ".mov")  # Extensions to skip

        # crawl valid <a href> links
        for link in response.css("a::attr(href)").getall():  # Iterate all anchor links
            parsed = urlparse(link)  # Parse link

            # only allow http(s) and relative URLs
            if parsed.scheme in ["http", "https"] or link.startswith("/"):  # Check for valid scheme
                # skip unwanted extensions (like pdf, jpg, etc.)
                if not link.lower().endswith(skip_exts):  # Skip unwanted file types
                    yield response.follow(link, self.parse)  # Follow valid link
            else:
                self.logger.info(f"Skipping non-web link: {link}")  # Log skipped link

    def save_asset(self, response, file_path):  # Save downloaded asset to file
        with open(file_path, 'wb') as f:  # Open file for binary writing
            f.write(response.body)  # Write asset content
        logging.info(f"Saved asset: {file_path}")  # Log saved asset

    def closed(self, reason):  # Called when spider finishes
        logging.info("Crawling finished, generating PDF brochure...")  # Log completion

        pdf_path = os.path.join(self.base_dir, "website_brochure.pdf")  # Path for output PDF

        # Combine all HTML files into one big brochure
        combined_html = "<html><head><meta charset='utf-8'></head><body>"  # Start combined HTML
        for html_file in self.html_files:  # Iterate saved HTML files
            with open(html_file, encoding="utf-8") as f:  # Open HTML file
                combined_html += f"<div class='page'>{f.read()}</div><p style='page-break-after:always;'></p>"  # Add to combined HTML
        combined_html += "</body></html>"  # End combined HTML

        HTML(string=combined_html, base_url=self.base_dir).write_pdf(pdf_path)  # Generate PDF from HTML
        logging.info(f"PDF brochure created: {pdf_path}")  # Log PDF creation

# Run the crawler
if __name__ == "__main__":  # Entry point for script execution
    process = CrawlerProcess(get_project_settings())  # Create Scrapy process with settings
    process.crawl(WebsiteSpider, start_url="https://example.com/")  # Start crawling with spider
    process.start()  #
