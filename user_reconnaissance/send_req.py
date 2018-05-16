"""
This module is responsible for executing the requests for Facebook search or profile access
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def send_request(session, url: list=None):
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

        return driver.page_source

    else:
        print('Either define a URL or run the test case (set test=True)')
        return None


