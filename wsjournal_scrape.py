import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# incomplete: only scrapes for one month
def wsj_scrape():
    base_url = "https://www.wsj.com/news/archive/years"
    browser = webdriver.Firefox()
    browser.get(base_url)

    headline_dicts = []  # list of dicts

    year_containers = browser.find_elements(By.CLASS_NAME, "WSJTheme--year-contain--ChIUCO3R ")
    for year_c in year_containers:
        container_texts = year_c.get_attribute("innerText").split()  # first element is year; other elements are months
        print(container_texts)
        # get month elements
        month_elements = year_c.find_elements(By.CLASS_NAME, "WSJTheme--month-link--1N8tTFWa ")
        browser.implicitly_wait(2)
        for month in month_elements:
            month_href = month.get_attribute("href")
            month.click()  # go to month href
            dates = browser.find_elements(By.CLASS_NAME, "WSJTheme--day-link--19pByDpZ ")
            dates_href_dict = {date.get_attribute("innerText"): date.get_attribute("href") for date in dates}
            browser.implicitly_wait(2)
            for date, href in dates_href_dict.items():
                print("date: ", date)
                browser.get(href)

                headlines_outer = browser.find_elements(By.CLASS_NAME, "WSJTheme--headline--7VCzo7Ay ")
                browser.implicitly_wait(2)
                for headline in headlines_outer:
                    headline_text = headline.get_attribute("innerText")

                    headline_dict = dict()
                    headline_dict["Year"] = container_texts[0]
                    headline_dict["Date"] = date
                    headline_dict["Headline"] = headline_text
                    headline_dicts.append(headline_dict)

                browser.get(month_href)
            break
        break
    browser.close()
    df = pd.json_normalize(headline_dicts)
    return df


