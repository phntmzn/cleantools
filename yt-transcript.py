import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

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

# Function to download transcripts from youtubetotranscript.com
async def auto_download_transcripts(video_urls, browser):
    context = await browser.new_context()
    page = await context.new_page()

    for url in video_urls:
        print(f"Processing: {url}")
        # 1) Navigate to the new site
        await page.goto("https://youtubetotranscript.com")
        await asyncio.sleep(2)

        try:
            # 2) Wait for and fill the YouTube URL input
            await page.wait_for_selector('input[name="youtube_url"]', timeout=10000)
            await page.fill('input[name="youtube_url"]', url)
            await page.keyboard.press("Enter")
            await asyncio.sleep(2)

            # 3) Click the “Get Free Transcript” button
            await page.wait_for_selector('button.btn.btn-secondary.btn-rounded[type="submit"]', timeout=10000)
            await page.click('button.btn.btn-secondary.btn-rounded[type="submit"]')
            await asyncio.sleep(5)
        except Exception as e:
            print("Transcript-fetch button not found:", e)

        try:
            # 4) Click the “Copy Transcript” button instead of a download link
            await page.wait_for_selector('#copy-transcript', timeout=10000)
            await page.click('#copy-transcript')
            await asyncio.sleep(3)
            # Extract transcript text
            transcript = await page.eval_on_selector('#transcript-text', 'el => el.value')
            # Parse video ID from URL
            video_id = parse_qs(urlparse(url).query)['v'][0]
            # Write transcript to file
            with open(f'{video_id}.txt', 'w', encoding='utf-8') as f:
                f.write(transcript)
            print(f'Transcript saved to {video_id}.txt')
        except Exception as e:
            print("Copy-Transcript button not found:", e)

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
