"""
This is the main information gathering module. By calling the send_request function, it will retrieve the HTML code of
the results, it will send it to the parser and then it will store the data for this user in an appropriate structure.
"""

import requests
import json
import sys

# custom modules import
from fb_login import fb_login
from send_req import send_request
from parser import parse


class Gather():
    def __init__(self):

        self.session = requests.Session()
        # set a browser-like user-agent header in order not to be considered a crawler
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like '
                                                   'Gecko) Chrome/65.0.3325.181 Safari/537.36'})

    def logged_in(self):
        return True if 'c_user' in self.session.cookies else False

    def fb_login(self):
        """
        FB login using the fb_login module
        """
        try:
            if not fb_login(self.session):
                raise Exception('FB login failed')
        except Exception as e:
            return None

    def cets(self, targets_filename: str = None, test: bool = False):
        """
        Connect-Extract-Transform-Save
        Gets as input a filename of a JSON file with target profiles IDs as keys and URLs as values, then executes login,
        request & parsing
        """
        # demo
        if test:
            # Test users profiles
            targets_filename = 'test_targets.json'

        # targets file read
        if targets_filename:
            try:
                targets = json.load(open(targets_filename, 'r'))
            except Exception as e:
                print(e)
                return

        # the output dictionary, with profile IDs as keys and a list of words or phrases as values
        output = {}

        for target in targets.keys():
            output[target] = []
            # make sure value fields are lists
            if type(targets[target]) is not list:
                targets[target] = [targets[target]]

            print("Retrieving and parsing HTML data for user with id "+target+"...")
            for url in targets[target]:
                # get the HTML code
                html_data = send_request(self.session, url)
                # send the HTML code to the parser
                extracted_data = parse(html_data, search_type='about' if 'about' in url else 'graph')
                # extend the output with the information gathered
                output[target].extend(extracted_data)

            print("Info gathering complete for user with id "+target)
            print(output[target])

        # save output to a JSON file
        json_output = json.dumps(output)
        f = open("output.json", "w")
        f.write(json_output)
        f.close()
        return


if __name__ == '__main__':
    args = sys.argv
    # enter '-test' while executing to run test scenario
    test_arg = True if '-test' or '-TEST' in args else False

    gatherer = Gather()

    gatherer.fb_login()

    gatherer.cets(test=test_arg) if gatherer.logged_in() else print('You need to log in Facebook first')
