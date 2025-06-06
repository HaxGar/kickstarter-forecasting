from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions


def main():
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = Firefox(options=options)

    url = "https://www.kickstarter.com/projects/ankermake/eufymake-e1-the-first-personal-3d-textured-uv-printer?ref=discovery_category&total_hits=54706&category_id=334"

    # response = requests.get(url)
    # body = response.text

    driver.get(url)

    body = driver.page_source

    driver.quit()

    with open("test.html", "w") as file:
        file.write(body)

if __name__ == "__main__":
    main()