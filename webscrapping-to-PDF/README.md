# BrochureBot 1.2 - The Web-to-PDF Archivist

[![Python](https://img.shields.io/badge/Made%20with-Python%203-1f425f.svg)](https://www.python.org/)
[![Scrapy](https://img.shields.io/badge/Built%20with-Scrapy%20Framework-639b0c.svg)](https://scrapy.org/)
[![WeasyPrint](https://img.shields.io/badge/PDF%20by-WeasyPrint-9d0d0d.svg)](https://weasyprint.org/)

> **From countless web pages to a single, sleek document.**
> BrochureBot is your automated archivist, tirelessly crawling websites and compiling their essence into a handy PDF brochure for offline reading and review.

## The Genesis of the Idea!

My journey into automation started with the simple `requests` package. The magic of pulling a website's content with a few lines of code was exhilarating! But then a thought struck me:

> _"What if I could capture an entire website's essence? Not just one page, but all its interconnected content... and transform it into a beautiful, printable brochure you could review and archive?"_

That spark of curiosity ignited a deep dive into the powerful worlds of **Scrapy** for crawling and **WeasyPrint** for beautiful PDF generation. This bot is the first fruit of that labor.

**The Evolution:** Version 1.0 was a solid foundation, expertly handling traditional static websites. But when faced with modern Single-Page Applications (SPAs) built with React, Angular, or Vue.js, it hit a wall. That's when Playwright entered the scene, giving birth to Version 1.2 - now smart enough to handle both static and dynamic sites with equal finesse!

---

## How BrochureBot Works Its Magic

### Intelligent Website Detection

BrochureBot starts by analyzing your target website to determine its nature:

- Static Sites: Traditional HTML websites are crawled comprehensively page-by-page

- Dynamic Sites (SPAs): JavaScript-heavy applications are captured in their fully-rendered state

### Dual-Engine PDF Generation

- WeasyPrint: For static sites, beautifully combines all crawled pages into a single PDF

- Playwright: For dynamic sites, captures the fully-rendered SPA as it appears in a real browser

### The Complete Workflow

1. Website Analysis: Automatically detects site type (static vs dynamic)

2. Smart Crawling: Adapts crawling strategy based on website technology

3. Asset Preservation: Downloads all images, CSS, and JavaScript files

4. PDF Crafting: Generates a print-perfect brochure using the appropriate engine

5. Organization: Saves everything in a tidy website_content folder

---

## Unleashing the Bot: Your Quick Start Guide

### Prerequisites

Ensure you have Python and `pip` installed, then prepare your environment:

```bash
# Navigate to the BrochureBot directory
cd path/to/webscrapping-to-PDF

# Create and activate a virtual environment (Highly Recommended)
python -m venv env_custom
source env_custom/bin/activate  # On Windows: .\venv\Scripts\activate

# Install the dream team of packages
pip install -r requirements.txt

# Install Playwright browsers (essential for dynamic sites)
playwright install chromium
```

## Running the Script

1.  **Configure your target:** Open BrochureBot.py and set your desired website:
    ```python
    if __name__ == "__main__":  # Main script entry
       start_url = "https://your-target-website.com/"  # Website to crawl
    ```
2.  **Find the target**: Look for the `start_urls` variable assignment towards the end of the script. This is where you tell the bot which website to explore.

3.  **Launch the archivist:** Run the script and watch the magic happen:

    ```bash
    # Make executable (first time only)
    chmod +x BrochureBot.py

    # Run the bot!
    ./BrochureBot.py
    ```

    **Alternatively:** You can also pass the URL as a command-line argument:

        ```bash

    ./BrochureBot.py "https://your-target-website.com/"

    ```

    ```

4.  **Grab your brochure**: Your beautifully crafted PDF will be waiting in the website_content folder, along with all preserved assets.

---

## For the Curious: Code Map & Learning

I've filled the code with inline comments—not to bore you, but to explain the "why" behind the "what." It's as much for my future self as it is for you!

- **The Spider Brain (`WebsiteSpider` class)**: This is where the crawling logic lives. It's built following the [official Scrapy Spider documentation](https://docs.scrapy.org/en/latest/topics/spiders.html). It defines how to parse pages and follow links.
- **The PDF Factory (`HTML` from `weasyprint`)**: After scraping, this module takes the HTML and works its magic. Learn more from the [WeasyPrint Documentation](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html).
- **Playwright**: For dynamic site playwright will perform a much better processing of the PDF than weasyprint. Learn more from the [Playwright Documentation](https://playwright.dev/)

---

## Version History

- **Version 1.0**: The Pioneer. Successfully performs a deep scrape of a website and compiles all the text content into a basic, functional PDF document. It works, and that's a fantastic start!
- **Version 1.2 (Current)**: Introduced intelligent website detection and dual-engine PDF generation. Now handles both static sites and modern JavaScript SPAs with equal precision.

---

## ⚠️ Important Disclaimer & Ethical Use ⚠️

**The BrochureBot is a tool for learning, efficiency, and ethical archiving.**

It is **NOT** intended for:

- Scraping websites without permission against their `robots.txt` rules.
- Stealing or republishing content maliciously.
- Spamming or any other unethical activity.

**Please use it responsibly.** The goal is to demonstrate how automation can save hours of manual browsing for **personal, educational review**, not to infringe on the rights of content creators. Always respect website terms of service.

---

BrochureBot represents more than just a script - it's a gateway to understanding how automation can transform tedious tasks into elegant solutions. Whether you're preserving knowledge, conducting research, or simply satisfying your curiosity, this tool opens doors to new possibilities.
