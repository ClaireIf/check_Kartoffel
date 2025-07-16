# -*- coding: utf-8 -*-
# @Time    : 2025/07/16 11:40
# @Author  : Claire
# @file : config.py


SEARCH_TERM = "Kartoffeln"

SUPERMARKETS = {
    "Lidl": {
        "url": "https://www.lidl.de/",
        "cookie_selector": "button#onetrust-accept-btn-handler",
        "search_box": "input[id='s-search-input-field']",
        "price_selector": ".badge__text"
    },
    "Kaufland": {
        "url": "https://www.kaufland.de/",
        "cookie_selector": "#onetrust-accept-btn-handler",
        "search_box": "input[id='searchInput']",
        "price_selector": ".product-tile-price__price",
        "checkbox_selector": "#cb-i"
    },
    "Aldi": {
        "url": "https://www.aldi-nord.de/",
        "cookie_selector": '[data-testid="uc-accept-all-button"]',
        "search_box": "input[id='autocomplete-1-input']",
        "price_selector": ".price__wrapper"
    },
    "Netto": {
        "url": "https://www.netto-online.de/",
        "cookie_selector": "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
        "search_box": "input[name='SearchTerm']",
        "price_selector": ".product-box__price"
    }
}
