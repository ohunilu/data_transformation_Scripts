# 📄 BrochureBot 1.0 - The Web-to-PDF Archivist

[![Python](https://img.shields.io/badge/Made%20with-Python%203-1f425f.svg)](https://www.python.org/)
[![Scrapy](https://img.shields.io/badge/Built%20with-Scrapy%20Framework-639b0c.svg)](https://scrapy.org/)
[![WeasyPrint](https://img.shields.io/badge/PDF%20by-WeasyPrint-9d0d0d.svg)](https://weasyprint.org/)

> **From countless web pages to a single, sleek document.**
> BrochureBot is your automated archivist, tirelessly crawling websites and compiling their essence into a handy PDF brochure for offline reading and review.

## 🧠 The "Aha!" Moment

My journey into automation started with the simple `requests` package. The magic of pulling a website's content with a few lines of code was exhilarating! But then a thought struck me:

> _"What if I could pull an_ entire _website? Not just one page, but all its subpages... and turn it all into a neat, printable brochure you could review at a glance?"_

That spark of curiosity ignited a deep dive into the powerful worlds of **Scrapy** for crawling and **WeasyPrint** for beautiful PDF generation. This bot is the first fruit of that labor.

**Psst:** This is very much a work-in-progress passion project. Version 1.0 is the foundation—a proof of concept that works! Future versions will dress it up with smart templates and layouts to create a truly fine, ready-to-print brochure. (Let me not get ahead of myself... but the future is bright! ✨)

---

## 🧰 Under the Hood: The Tech Stack

This bot is powered by a robust combination of Python packages, each playing a critical role:

- **`scrapy`**: The industrial-strength web crawling framework that does the heavy lifting of discovering and scraping all the pages on a site.
- **`weasyprint`**: The magical tool that transforms raw HTML into a clean, styled PDF document. It's like a print driver for the web.
- **`logging`**: The bot's black box, meticulously recording its journey so we can trace its steps and debug any hiccups.
- **`urllib.parse`**: The savvy navigator, helping the bot correctly handle and join URLs to avoid getting lost on the web.
- **`os`**: The reliable file manager, ensuring all the generated brochures are saved right where they should be.

---

## 🚀 How to Unleash the Bot

Getting BrochureBot to work for you is a simple three-step ritual.

### Prerequisites

Ensure you have Python and `pip` installed on your machine. Then, install the required champions:

```bash
# Navigate to the BrochureBot directory
cd path/to/webscrapping-to-PDF

# Create and activate a virtual environment (Highly Recommended)
python -m venv env_custom
source env_custom/bin/activate  # On Windows: .\venv\Scripts\activate

# Install the dream team of packages
pip install -r requirements.txt
```

## 🚀 Running the Script

1.  **Open the script** `BrochureBot.py` in your favorite code editor.
2.  **Find the target**: Look for the `start_urls` list in the process.crawl(WebsiteSpider, start_url="https://example.com/") at the end of the script.This is where you tell the bot which website to explore.

    ```python
    if __name__ == "__main__":
        process = CrawlerProcess(get_project_settings())
        process.crawl(WebsiteSpider, start_url="https://example.com/") # And this to the starting URL
        process.start()
    ```

3.  **Run the command**: Fire up your terminal, activate your virtual environment, make the file executable and run:

    ```bash
    ./BrochureBot.py
    ```

4.  **Grab your brochure**: Sit back and watch the logs fly by! Once finished, your brand-new PDF will be waiting for you in the "website_content" folder.

---

## 🗺️ For the Curious: Code Map & Learning

I've filled the code with inline comments—not to bore you, but to explain the "why" behind the "what." It's as much for my future self as it is for you!

- **The Spider Brain (`WebsiteSpider` class)**: This is where the crawling logic lives. It's built following the [official Scrapy Spider documentation](https://docs.scrapy.org/en/latest/topics/spiders.html). It defines how to parse pages and follow links.
- **The PDF Factory (`HTML` from `weasyprint`)**: After scraping, this module takes the HTML and works its magic. Learn more from the [WeasyPrint Documentation](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html).

---

## 📋 Version History

- **Version 1.0 (Current)**: The Pioneer. Successfully performs a deep scrape of a website and compiles all the text content into a basic, functional PDF document. It works, and that's a fantastic start!

---

## ⚠️ Important Disclaimer & Ethical Use

**The BrochureBot is a tool for learning, efficiency, and ethical archiving.**

It is **NOT** intended for:

- Scraping websites without permission against their `robots.txt` rules.
- Stealing or republishing content maliciously.
- Spamming or any other unethical activity.

**Please use it responsibly.** The goal is to demonstrate how automation can save hours of manual browsing for **personal, educational review**, not to infringe on the rights of content creators. Always respect website terms of service.

---

Happy scraping and (automated) brochure making! I hope this bot inspires you to think about what else you can automate.
