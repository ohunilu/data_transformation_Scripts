import os
import asyncio
from weasyprint import HTML
from playwright.async_api import async_playwright


async def generate_pdf_async(metadata: dict) -> str:
    pdf_path = os.path.join(metadata['base_dir'], "website_brochure.pdf")

    if metadata['is_dynamic']:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(metadata['start_url'], wait_until="networkidle")
            await page.pdf(path=pdf_path, format="A4", print_background=True)
            await browser.close()
    else:
        combined_html = "<html><body>"
        for html_file in metadata.get("html_files", []):
            with open(html_file, encoding="utf-8") as f:
                combined_html += f.read()
        combined_html += "</body></html>"

        HTML(string=combined_html).write_pdf(pdf_path)

    return pdf_path


def generate_pdf(metadata: dict) -> bool:
    try:
        asyncio.run(generate_pdf_async(metadata))
        return True
    except Exception as e:
        print(f"PDF generation error: {e}")
        return False