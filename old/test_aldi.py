# -*- coding: utf-8 -*-
# @Time    : 2025/03/09 18:18
# @Author  : Claire
# @file : test_aldi.py
from playwright.sync_api import sync_playwright


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(
            "https://www.aldi-nord.de/angebote/aktion-mo-10-03/kleine-speisekartoffeln-drillinge-6115-0-0.article.html")

        try:
            # Handling aldi Cookie Permission Mask
            page.wait_for_selector('[data-testid="uc-accept-all-button"]', timeout=5000)
            page.click('[data-testid="uc-accept-all-button"]')  # Click "Accept All Cookies"
            print("Aldi: Cookie License mask is off")
        except:
            print("Aldi: No cookie consent button found, skipping")

        # Wait and get the text of price__wrapper
        try:
            page.wait_for_selector('.price__wrapper', timeout=10000)
            price_text = page.locator('.price__wrapper').nth(0).inner_text()  # Get the text of price__wrapper, only the 0th value
            print(f"The value of price__wrapper is: {price_text}")
        except Exception as e:
            print(f"error information: {e}")

        browser.close()


run()