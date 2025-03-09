# -*- coding: utf-8 -*-
# @Time    : 2025/03/09 14:36
# @Author  : Claire
# @file : check_potato_prices.py

from playwright.sync_api import sync_playwright
import pandas as pd

# Define the supermarket and its search URL
SUPERMARKETS = {
    "Lidl": "https://www.lidl.de/",
    "Kaufland": "https://www.kaufland.de/",
    "Aldi": "https://www.aldi-nord.de/",
    "Netto": "https://www.netto-online.de/",
}

# key word（Kartoffeln）
SEARCH_TERM = "Kartoffeln"

# Result storage
results = []

def scrape_supermarket(name, url, playwright):
    # browser = playwright.chromium.launch(headless=True)
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)
    if "lidl" in url:
        try:
            # Handling Lidl's Cookie Permission Mask
            page.wait_for_selector("button#onetrust-accept-btn-handler", timeout=5000)
            page.click("button#onetrust-accept-btn-handler")  # Click "Accept All Cookies"
            print("Lidl: Cookie License mask is off")
        except:
            print("Lidl: No cookie consent button found, skipping")
        page.fill("input[id='s-search-input-field']", SEARCH_TERM)  # Lidl search box
    elif "kaufland" in url:
        try:
            # Handling kaufland Cookie Permission Mask
            page.wait_for_selector("#onetrust-accept-btn-handler", timeout=5000)
            page.click("#onetrust-accept-btn-handler")  # Click "Accept All Cookies"
            print("Kaufland: Cookie License mask is off")
        except:
            print("Kaufland: No cookie consent button found, skipping")
        try:
            page.wait_for_selector('#cb-i', timeout=5000)
            page.locator('#cb-i').check()
        except:
            print("not checkbox")
        page.fill("input[id='searchInput']", SEARCH_TERM)  # Kaufland search box
    elif "aldi" in url:
        try:
            # Handling aldi Cookie Permission Mask
            page.wait_for_selector('[data-testid="uc-accept-all-button"]', timeout=5000)
            page.click('[data-testid="uc-accept-all-button"]')  # Click "Accept All Cookies"
            print("Aldi: Cookie License mask is off")
        except:
            print("Aldi: No cookie consent button found, skipping")
        page.fill("input[id='autocomplete-1-input']", SEARCH_TERM)  # Aldi search box
    elif "netto" in url:
        try:
            # Handling netto Cookie Permission Mask
            page.wait_for_selector("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll", timeout=5000)
            page.click("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")  # Click "Accept All Cookies"
            page.wait_for_timeout(5000)
            print("Netto: Cookie License mask is off")
        except:
            print("Netto: No cookie consent button found, skipping")
        page.fill("input[name='SearchTerm']", SEARCH_TERM)  # Aldi search box
    page.keyboard.press("Enter")  # Simulate pressing the Enter key
    page.wait_for_timeout(5000)

    # Only aldi has potato prices, all not done.
    prices = page.locator("price").all_text_contents()
    if prices:
        results.append({"Supermarket": name, "Price": prices[0]})
    else:
        results.append({"Supermarket": name, "Price": "Not found"})

    browser.close()

# run
with sync_playwright() as p:
    for market, url in SUPERMARKETS.items():
        scrape_supermarket(market, url, p)

# Save results to Excel
df = pd.DataFrame(results)
df.to_excel("potato_prices.xlsx", index=False)

print("The potato price crawling is complete and has been saved to potato_prices.xlsx")