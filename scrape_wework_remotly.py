# scraper.py
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://weworkremotely.com/remote-jobs"

def scrape_jobs(max_pages=1):
    jobs = []

    for page in range(1, max_pages+1):
        url = BASE_URL
        if page > 1:
            url = f"{BASE_URL}?page={page}"

        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"Failed to fetch page {page}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        job_sections = soup.select("section.jobs")  # main job section

        for section in job_sections:
            category_tag = section.select_one("h2")
            category = category_tag.get_text(strip=True) if category_tag else "N/A"

            job_posts = section.select("li.feature") + section.select("li")  # include normal + featured
            for job in job_posts:
                link_tag = job.select_one("a")
                if not link_tag:
                    continue
                job_url = "https://weworkremotely.com" + link_tag.get("href")
                company_tag = job.select_one(".company")
                company = company_tag.get_text(strip=True) if company_tag else "N/A"
                title_tag = job.select_one(".title")
                title = title_tag.get_text(strip=True) if title_tag else "N/A"
                location_tag = job.select_one(".region")
                location = location_tag.get_text(strip=True) if location_tag else "Worldwide"

                jobs.append({
                    "title": title,
                    "company": company,
                    "category": category,
                    "location": location,
                    "url": job_url                
                })
    
    print(jobs)

    return jobs

if __name__ == "__main__":
    results = scrape_jobs(max_pages=1)
    print(f"Scraped {len(results)} jobs")
    for j in results[:5]:
        print(j)
