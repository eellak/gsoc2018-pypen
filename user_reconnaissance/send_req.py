'''This module is responsible for executing the requests for Facebook search or profile access'''

# custom modules import
from fb_login import fb_login

def send_request(session, url=None, test=False):
    '''By creating a session object, logging in, and executing the rest of our request through the same
    session object, we ensure that we will be able to view the results and not get an error due to
    unauthorized requests'''

    try:
        if not fb_login(session):
            raise Exception('FB Login Failed')

    except Exception as e:
        print(e)
        return None

    if test:
        # Andreas Hutchison liked pages
        return session.get('https://www.facebook.com/search/100026027770190/pages-liked/intersect').text

    elif url:
        return session.get(url).text

    else:
        print('Either define a URL or run the test case (set test=True)')
        return None


