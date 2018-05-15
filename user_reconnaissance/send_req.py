"""
This module is responsible for executing the requests for Facebook search or profile access
"""

def send_request(session, url: list=None):
    """
    By creating a session object, logging in, and executing the rest of our request through the same
    session object, we ensure that we will be able to view the results and not get an error due to
    unauthorized requests
    """

    print("Retrieving HTML data...")
    if url:
        # Facebook loads HTML code through javascript, so we need to load the page with a driver. Pure Selenium
        # implementation did not work out because cookies couldn't be loaded. TODO try with Selenium & PhantomJS
        response = session.get(url)
        return response.text

    else:
        print('Either define a URL or run the test case (set test=True)')
        return None


