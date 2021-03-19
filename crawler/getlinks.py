from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions
import time

def getlinks(keyword, num_of_news, output_path):

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('/Users/ryan/Documents/GitHub/cbc-news-crawler-for-nlp/crawler/chromedriver', options=options)
    
    driver.get("https://www.cbc.ca/search?q={}&section=news&sortOrder=relevance".format(keyword))
    time.sleep(15)
    num = 1
    limit = 0

    while (limit < 435):
        try:
            # press load more button
            element = driver.find_element_by_xpath(
                "//div[@class='contentList sclt-contentlist']/button[contains(text(), 'Load More')]")
            actions = ActionChains(driver)
            actions.move_to_element(element)
            actions.click(element).perform()
            print('Loaded {} time(s)\n'.format(str(num)))
            num += 1
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            limit += 1

        except Exception as e:
            try:
                print(e)
                print('Trying Again')
                element = driver.find_element_by_xpath(
                "//div[@class='contentList sclt-contentlist']/button[contains(text(), 'Load More')]")
                actions = ActionChains(driver)
                actions.move_to_element(element)
                actions.click(element).perform()
                print('Loaded {} time(s)\n'.format(str(num)))
                num += 1
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                limit += 1
            except Exception as e:
                print(e)
                break
            
    print('Loading Complete')
    # extracting links
    print('Begin extracting links...\n')
    f = open(output_path, "w+")
    for i in range(num_of_news - 1):
        try:
            link = driver.find_element_by_xpath(
                "//div[@class='contentListCards']/a[@class='card cardListing rightImage sclt-contentlistcard{}']".format(str(i))).get_attribute('href')
            print("Wrote link #{}: {}\n".format(i+1, str(link)))
            f.write('{}\n'.format(str(link)))
        except exceptions.StaleElementReferenceException as e:
            link = driver.find_element_by_xpath(
                "//div[@class='contentListCards']/a[@class='card cardListing rightImage sclt-contentlistcard{}']".format(str(i))).get_attribute('href')
            print("Wrote link #{}: {}\n".format(i+1, str(link)))
            f.write('{}\n'.format(str(link)))

if __name__ == "__main__":
    print("Testing...")
    getlinks('Apple', 100, 'links.txt')