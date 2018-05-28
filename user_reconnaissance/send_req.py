"""
This module is responsible for executing the requests for Facebook search or profile access
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys

def send_request(session, config, url: list=None):
    """
    By creating a session object, logging in, and executing the rest of our request through a driver that shares
    the same cookies, we ensure that we will be able to view the results and not get an error due to
    unauthorized requests.
    Facebook loads HTML code through javascript, so we need to load the page with a browser driver
    """

    if url:

        # instantiate a chrome options object so you can set the headless preference (no browser window pop-up)
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        # block popups
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        # you need to add 'chromedriver' (http://chromedriver.chromium.org/downloads) executable to PATH
        driver = webdriver.Chrome(chrome_options=chrome_options)

        # executing a GET to facebook.com in order to define the domain and be able to set the cookies
        driver.get('https://www.facebook.com')

        # copying our existing session's cookies to the driver in order to be authorized for future requests
        cookies_dict = session.cookies.get_dict()
        cookies = [{'name':name, 'value':value} for name, value in cookies_dict.items()]
        for c in cookies:
            driver.add_cookie(c)

        driver.get(url)

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        dots_count = 1

        while True:
            print("Loading contents{0}   \r".format('.'*dots_count), end="\r", flush=True)
            dots_count += 1

            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(int(config['CONSTANTS']['SCROLL_PAUSE_TIME']))

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


        return driver.page_source

    else:
        print('Either define a URL or run the test case (set test=True)')
        return None


