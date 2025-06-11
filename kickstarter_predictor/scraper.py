from urllib.parse import urlparse, urljoin
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 2px solid red;")
    sleep(3)
    apply_style(original_style)



def main():
    options = FirefoxOptions()
    # options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--width=2560')
    options.add_argument('--height=1440')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    # options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')
    driver = Firefox(options=options)

    print("Driver loaded")


    raw_url = urlparse("https://www.kickstarter.com/projects/zettlab/zettlab-ai-nas-personal-cloud-for-smart-data-management/")
    project_url = raw_url._replace(query="").geturl()
    project_comments_url = urlparse(f"{project_url}/comments")
    url = project_comments_url.geturl()

    print("Fetching url")
    driver.get(url)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    print("On page !")


    # Navigating to the comments page
    # print("Searching for element...")
    # comment_button = driver.find_element(By.ID, "comments-emoji")

    # print("... Found ! Navigating to the comments page...")
    # comment_button.click()

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "react-project-comments"))
    )

    # Closes the cookie box
    try:
        driver.find_element(By.CSS_SELECTOR, "button[class*='absolute t2 r2 pointer block py0 bg-transparent']").click()
    except Exception as error:
        print(f"An error occured while trying to close the cookie box : {error}")

    # Attempt at displaying all comments
    print("Expanding comments")
    for i in range(1,10):
        # Expand comments
        try:
            web_element = "//span[text()='Load more']/.."
            # web_element = "//button[.//span[text()='Load more']]"
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, web_element))
            )
            # load_more_button = driver.find_element(By.XPATH, "//button[.//span[text()='Load more']]")
            load_more_button = driver.find_element(By.XPATH, web_element)
            WebDriverWait(driver, 30).until(
                EC.visibility_of(load_more_button)
            )
            # load_more_button = driver.find_element(By.XPATH, "//button[.//span[text()='Load more']]")
            driver.execute_script('arguments[0].scrollIntoView();', load_more_button)
            driver.execute_script("arguments[0].style.transform='scale(1)';", load_more_button)
            ActionChains(driver).move_to_element(load_more_button).click(load_more_button).perform()

            load_more_button.click()
            load_more_button.send_keys(Keys.ENTER)

            highlight(load_more_button)

            # driver.execute_script("return arguments[0].click()", load_more_button)
            # load_more_button.click()
            # ActionChains(driver).move_to_element(load_more_button).click().perform()
            print("Load more clicked")
        except Exception as error:
            print(f"Error while loading more comments : {error}")
            break

    for i in range(50):
        # Expand comments
        try:
            previous_comment_buttons = driver.find_elements(By.XPATH, "//span[text()='Load previous replies']/..")
            for button in previous_comment_buttons: 
                button.click()
            # previous_comment_button.click()
            print("Load previous clicked")
        except Exception as error:
            print(f"Error expanding comments : {error}")
            break
    

    # print("Scraping comments")
    # all_comments = driver.find_elements(By.CSS_SELECTOR, "div[class*='border-box relative break-word border border-grey-400 px3 pt3 pb2 o100p transition-all transition-delay-1000 bg-white']")
    all_comments = driver.find_elements(By.CSS_SELECTOR, "li[class*='mb2']")

    # # Retrieve comments
    user_comments = []
    for index, comment in enumerate(all_comments):

        subcomments = comment.find_elements(By.CSS_SELECTOR, "div[class*='border-box relative break-word border border-grey-400 px3 pt3 pb2 o100p transition-all transition-delay-1000 bg-white']")
        print(f"Thread {index} : {len(subcomments)} comments")
        for comment in subcomments:
            user_comments.append(" ".join(comment.text.split("\n")))

    with open("comments.txt", "w") as comment_file:
        comment_file.write(
            "\n".join(comment for comment in user_comments)
        )

    driver.quit()

    print("Exiting driver")


    # print(project_amount.text)

if __name__ == "__main__":
    main()