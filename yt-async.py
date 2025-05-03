import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# Function to fetch all video links from a YouTube search page
async def get_all_hrefs(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Launch browser in headless mode
        page = await browser.new_page()
        await page.goto(url)  # Navigate to the given URL

        # Scroll down the page multiple times to load dynamic content
        for _ in range(30):
            await page.mouse.wheel(0, 10000)
            await asyncio.sleep(1)

        # Get the full HTML content after scrolling
        content = await page.content()
        await browser.close()  # Close the browser

        # Parse HTML using BeautifulSoup and extract video links
        soup = BeautifulSoup(content, 'html.parser')
        hrefs = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/watch?v=')]
        return hrefs

# Optional function to retry the search with different keywords (not currently used)
async def retry_search_query(url, keywords):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        # Scroll to load dynamic content again
        for _ in range(30):
            await page.mouse.wheel(0, 10000)
            await asyncio.sleep(1)

        content = await page.content()
        await browser.close()

        soup = BeautifulSoup(content, 'html.parser')
        hrefs = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/watch?v=')]
        return hrefs

# Optional function to retry the search with different keywords (not currently used)
async def retry_search_query(url, keywords):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        # Scroll to load dynamic content again
        for _ in range(30):
            await page.mouse.wheel(0, 10000)
            await asyncio.sleep(1)

        content = await page.content()
        await browser.close()

        soup = BeautifulSoup(content, 'html.parser')
        hrefs = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/watch?v=')]
        return hrefs
    
# Define the search URL
url = "https://www.youtube.com/results?search_query=open+heart+surgey"

# Run the script and print all video URLs
hrefs = asyncio.run(get_all_hrefs(url))
for href in hrefs:
    print(f"https://www.youtube.com{href}")
