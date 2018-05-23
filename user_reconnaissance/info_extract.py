"""
This is the main information gathering module. By calling the send_request function, it will retrieve the HTML code of
the results, it will send it to the parser and then it will store the data for this user in an appropriate structure.
"""

import requests
import json

# custom modules import
from fb_login import fb_login
from send_req import send_request
from parser import parse
import configparser

config = configparser.ConfigParser()
config.read('data.ini')

class Extractor():
    def __init__(self):

        self.session = requests.Session()
        # set a browser-like user-agent header in order not to be considered a crawler
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like '
                                                   'Gecko) Chrome/65.0.3325.181 Safari/537.36'})
        # the output dictionary, with profile IDs as keys and a list of words or phrases as values
        self.output = {}

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
        if self.logged_in():
            # demo
            if test:
                # Test users profiles
                targets_filename = config['IO']['test_targets']

            # targets file read
            if targets_filename:
                try:
                    targets = json.load(open(targets_filename, 'r'))
                except Exception as e:
                    print(e)
                    return None

            elif not test:
                print('You have to define an input file "-file FILENAME"')
                return None

            for target in targets.keys():
                self.output[target] = {}
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
                    self.output[target].update(extracted_data)

                print("Info gathering complete for user with id "+target)
                print(json.dumps(self.output[target], indent=3, sort_keys=True))

        else:
            print('You need to log in Facebook first')
            return None

    def save(self):
        # save output to a JSON file
        if self.output:
            json_output = json.dumps(self.output, ensure_ascii=False)
            f = open(config['IO']['output'], "w")
            f.write(json_output)
            f.close()
            return None
        else:
            print('No info has been gathered, output is empty - Nothing to save here')
            return None

