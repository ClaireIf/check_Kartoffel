# -*- coding: utf-8 -*-
# @Time    : 2025/03/09 18:28
# @Author  : Claire
# @file : test_aldi_lidl.py

from playwright.sync_api import sync_playwright


def handle_cookie_consent(page, cookie_button_selector, timeout=5000):
    """Handle Cookie Consent Popups"""
    try:
        page.wait_for_selector(cookie_button_selector, timeout=timeout)
        page.click(cookie_button_selector)
        print(f"Cookie License mask is off (button: {cookie_button_selector})")
    except Exception as e:
        print(f"No cookie consent button found (button: {cookie_button_selector}), skipping. Error: {e}")


def get_price_text(page, price_selector, timeout=10000):
    """Retrieve the price text from the page"""
    try:
        page.wait_for_selector(price_selector, timeout=timeout)
        price_text = page.locator(price_selector).nth(0).inner_text()  # Get the first price
        return price_text
    except Exception as e:
        print(f"Error while fetching price from {price_selector}: {e}")
        return None


def visit_and_get_price(page, url, cookie_button_selector, price_selector):
    """Visit the specified URL, handle cookie consent, and retrieve the price"""
    page.goto(url)  # Navigate to the URL

    # Handle Cookie Consent Popup
    handle_cookie_consent(page, cookie_button_selector)

    # Get the price information
    price_text = get_price_text(page, price_selector)
    if price_text:
        return price_text
    return "Price not found"


def run():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)  # headless=False makes the browser visible
        page = browser.new_page()

        # Handling Aldi website
        aldi_url = "https://www.aldi-nord.de/angebote/aktion-mo-10-03/kleine-speisekartoffeln-drillinge-6115-0-0.article.html"
        aldi_cookie_button = '[data-testid="uc-accept-all-button"]'
        aldi_price_selector = '.price__wrapper'
        aldi_price = visit_and_get_price(page, aldi_url, aldi_cookie_button, aldi_price_selector)
        print(f"Aldi Price: {aldi_price}")

        # Handling Lidl website
        lidl_url = "https://www.lidl.de/p/bioland-speisekartoffeln/p8490050"
        lidl_cookie_button = "button#onetrust-accept-btn-handler"
        lidl_price_selector = '.badge__text'
        lidl_price = visit_and_get_price(page, lidl_url, lidl_cookie_button, lidl_price_selector)
        print(f"Lidl Price: {lidl_price}")

        # Close the browser
        browser.close()


# Execute the script
run()
