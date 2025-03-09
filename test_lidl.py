# -*- coding: utf-8 -*-
# @Time    : 2025/03/09 18:03
# @Author  : Claire
# @file : test_lidl.py

from playwright.sync_api import sync_playwright


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False makes the browser visible
        page = browser.new_page()

        page.goto("https://www.lidl.de/p/bioland-speisekartoffeln/p8490050")

        try:
            # Wait and click the 'Accept All Cookies' button
            page.wait_for_selector("button#onetrust-accept-btn-handler", timeout=5000)
            page.click("button#onetrust-accept-btn-handler")
            print("Lidl: Cookie License mask is off")
        except:
            print("Lidl: No cookie consent button found, skipping")

        # Wait and get the text of the .badge__text element
        try:
            page.wait_for_selector('.badge__text', timeout=10000)
            badge_text = page.locator('.badge__text').inner_text()
            print(f"The value of badge__text is: {badge_text}")
        except Exception as e:
            print(f"error information: {e}")

        browser.close()


run()
