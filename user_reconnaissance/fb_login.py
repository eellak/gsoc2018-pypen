"""
This module is responsible for logging into Facebook so that we can use the authorization token (cookies) to later
access our search results.
Code partly borrowed & modified from https://gist.github.com/UndergroundLabs/fad38205068ffb904685
"""

import getpass
import os

def fb_login(session):
    """
    Attempt to login to Facebook. Returns user ID, xs token and
    fb_dtsg token. All 3 are required to make requests to
    Facebook endpoints as a logged in user. Returns False if
    login failed.
    """

    # fb_credentials.txt is ignored by source control (Git) and you can use it locally to save time by entering your fb
    # email in the 1st row and your pass in the 2nd
    if not os.path.exists('fb_credentials.txt'):
        # fb-use email
        email = input('Email: ')
        # password = input('Password: ')
        password = getpass.getpass('Password: ')
    else:
        email, password = open('fb_credentials.txt', 'r').read().split('\n')

    # Navigate to Facebook's homepage to load Facebook's cookies.
    response = session.get('https://m.facebook.com')

    # Attempt to login to Facebook
    response = session.post('https://m.facebook.com/login.php', data={
        'email': email,
        'pass': password
    }, allow_redirects=False)

    # If c_user cookie is present, login was successful
    if 'c_user' in response.cookies:
        print('FB login successful')
        return True
    else:
        print('FB login failed')
        return False
