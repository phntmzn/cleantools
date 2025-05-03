import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# Function to fetch all video links from a YouTube search page
async def get_all_hrefs(url, browser):
    page = await browser.new_page()
    await page.goto(url)

    for _ in range(30):
        await page.mouse.wheel(0, 10000)
        await asyncio.sleep(1)

    content = await page.content()
    await page.close()

    soup = BeautifulSoup(content, 'html.parser')
    hrefs = [f"https://www.youtube.com{a['href']}" for a in soup.find_all('a', href=True) if a['href'].startswith('/watch?v=')]
    return list(set(hrefs))  # remove duplicates

# Function to download transcripts from tactiq.io
async def auto_download_transcripts(video_urls, browser):
    context = await browser.new_context()
    page = await context.new_page()

    for url in video_urls:
        print(f"Processing: {url}")
        await page.goto("https://tactiq.io/tools/youtube-transcript")
        await asyncio.sleep(2)

        try:
            await page.wait_for_selector('input[type="url"]', timeout=10000)
            await page.fill('input[type="url"]', url)
            await page.keyboard.press("Enter")
            await asyncio.sleep(2)
            await page.wait_for_selector('a.button-primary.small.w-button', timeout=10000)
            await page.click('a.button-primary.small.w-button')
            await asyncio.sleep(5)
        except:
            print("Transcript button not found, continuing...")

        try:
            await page.wait_for_selector('#download', timeout=10000)
            await page.click('#download')
            await asyncio.sleep(3)
        except:
            print("Download button not found, skipping...")

    await context.close()

async def main():
    search_url = "https://www.youtube.com/results?search_query=open+heart+surgey"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        video_urls = await get_all_hrefs(search_url, browser)
        for href in video_urls:
            print(href)
        await auto_download_transcripts(video_urls, browser)
        await browser.close()

asyncio.run(main())
