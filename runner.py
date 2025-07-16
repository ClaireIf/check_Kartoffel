# -*- coding: utf-8 -*-
# @Time    : 2025/07/16 11:41
# @Author  : Claire
# @file : runner.py

from playwright.sync_api import sync_playwright
from config import SUPERMARKETS, SEARCH_TERM
from utils import accept_cookie, check_optional_checkbox
import pandas as pd
import os

results = []

def scrape_supermarket(name, config, playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(config["url"])
    page.wait_for_load_state("domcontentloaded")

    # Step 1: Cookie
    accept_cookie(page, config["cookie_selector"], name)

    # Step 2: checkbox（liek: Kaufland）
    if "checkbox_selector" in config:
        check_optional_checkbox(page, config["checkbox_selector"])

    # Step 3: Fill in the keywords and press Enter
    try:
        page.fill(config["search_box"], SEARCH_TERM)
        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)
    except Exception as e:
        print(f"{name}: Search failed: {e}")
        browser.close()
        results.append({"Supermarket": name, "Price": "Search failed"})
        return

    # Take a screenshot of the entire page
    try:
        screenshot_dir = "results/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{name}.png")
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"{name}: Full page screenshot saved to {screenshot_path}")
    except Exception as e:
        print(f"{name}: Screenshot failed: {e}")

    # Step 4: Grab the first price (using all_text_contents)
    try:
        prices = page.locator(config["price_selector"]).all_text_contents()
        price = prices[0] if prices else "Not found"
    except Exception as e:
        price = f"Error: {e}"

    results.append({"Supermarket": name, "Price": price})
    browser.close()

def run():
    with sync_playwright() as p:
        for market, config in SUPERMARKETS.items():
            print(f"\n🛒 Checking {market}")
            scrape_supermarket(market, config, p)

    # Save the results
    os.makedirs("results", exist_ok=True)
    df = pd.DataFrame(results)
    df.to_excel("results/potato_prices.xlsx", index=False)
    print("\n✅ Prices saved to results/potato_prices.xlsx")


if __name__ == "__main__":
    run()
