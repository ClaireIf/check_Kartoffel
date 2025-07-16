# -*- coding: utf-8 -*-
# @Time    : 2025/07/16 11:41
# @Author  : Claire
# @file : utils.py

def accept_cookie(page, selector, name):
    try:
        page.wait_for_selector(selector, timeout=5000)
        page.click(selector)
        print(f"{name}: Cookie License mask is off")
    except:
        print(f"{name}: No cookie consent button found, skipping")

def check_optional_checkbox(page, selector):
    try:
        page.wait_for_selector(selector, timeout=3000)
        page.locator(selector).check()
    except:
        pass  # skip silently if not found
