from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


def getlinks(keyword, num_of_news, output_path):

    driver = webdriver.Chrome('/Users/ryan/Documents/GitHub/cbc-news-crawler-for-nlp/crawler/chromedriver')
    driver.get("https://www.cbc.ca/search?q={}&section=news&sortOrder=relevance".format(keyword))
    time.sleep(15)
    num = 1

    while (True):
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

        except Exception as e:
            print(e)
            print('Loading Complete')
            break

    # extracting links
    print('Begin extracting links...\n')
    f = open(output_path, "w+")
    for i in range(num_of_news - 1):
        link = driver.find_element_by_xpath(
            "//div[@class='contentListCards']/a[@class='card cardListing rightImage sclt-contentlistcard{}']".format(str(i))).get_attribute('href')
        print("Wrote link #{}: {}\n".format(i+1, str(link)))
        f.write('{}\n'.format(str(link)))

if __name__ == "__main__":
    
    getlinks('Petition to close schools', 10, 'links.txt')