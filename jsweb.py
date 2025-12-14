from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://the-internet.herokuapp.com/")
    h1 = page.locator("h1").inner_text()

    print(h1)

    browser.close()
