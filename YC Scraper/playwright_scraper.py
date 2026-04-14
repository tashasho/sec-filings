import asyncio
import json
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        all_companies = {}
        
        async def response_handler(response):
            if "algolia" in response.url or "queries" in response.url:
                try:
                    data = await response.json()
                    if "results" in data:
                        for result in data["results"]:
                            if "hits" in result:
                                for hit in result["hits"]:
                                    slug = hit.get("slug")
                                    if slug:
                                        batch = hit.get("batch", "Unknown")
                                        # Map from full name to short batch name if necessary
                                        # The directory might return "W25", "S25" etc.
                                        all_companies[slug] = {
                                            "name": hit.get("name", ""),
                                            "slug": slug,
                                            "batch": batch,
                                            "one_liner": hit.get("one_liner", ""),
                                            "long_description": hit.get("long_description", ""),
                                            "website": hit.get("website", ""),
                                            "all_locations": hit.get("all_locations", ""),
                                            "team_size": hit.get("team_size", ""),
                                            "industry": hit.get("industry", ""),
                                            "subindustry": hit.get("subindustry", ""),
                                            "status": hit.get("status", ""),
                                            "stage": hit.get("stage", ""),
                                            "tags": hit.get("tags", []),
                                            "top_company": hit.get("top_company", False),
                                            "isHiring": hit.get("isHiring", False),
                                            "url": f"https://www.ycombinator.com/companies/{slug}",
                                            "logo": hit.get("small_logo_thumb_url", ""),
                                            "founders": []
                                        }
                except Exception as e:
                    pass
        
        page.on("response", response_handler)
        
        # Go to the filtered directory page
        url = "https://www.ycombinator.com/companies?batch=Summer%202026&batch=Spring%202026&batch=Winter%202026&batch=Fall%202025&batch=Summer%202025&batch=Spring%202025&batch=Winter%202025"
        print(f"Loading {url}")
        await page.goto(url, wait_until="networkidle")
        
        # Scroll to bottom repeatedly until no new companies are loaded
        last_count = 0
        scroll_attempts = 0
        
        while True:
            # Scroll down
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1500)
            
            # Check if count increased; wait a bit longer if we might still be loading
            count = len(all_companies)
            print(f"Loaded {count} companies...")
            if count == last_count:
                scroll_attempts += 1
                if scroll_attempts > 3:
                    print("Reached end of list.")
                    break
            else:
                scroll_attempts = 0
                last_count = count
        
        print(f"Total companies extracted from Algolia: {len(all_companies)}")
        
        output_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(output_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        
        with open(os.path.join(data_dir, "playwright_companies.json"), "w") as f:
            json.dump(all_companies, f, indent=2)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
