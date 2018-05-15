"""
This is the main information gathering module. By calling the send_request function, it will retrieve the HTML code of
the results, it will send it to the parser and then it will store the data for this user in an appropriate structure.
"""

import requests
import json
import copy

# custom modules import
from fb_login import fb_login
from send_req import send_request
from parser import parse


class Gather():
    def __init__(self, test: bool = False):

        self.session = requests.Session()
        self.test = test

        if self.test:
            target = {"100026027770190": "https://www.facebook.com/100026027770190/about"}
            self.CETS(target)

    def CETS(self, targets: dict = None):
        """
        Connect-Extract-Transform-Save
        Gets as input a dict of target profiles IDs as keys and URLs as values, then executes login, request & parsing
        """
        try:
            if not fb_login(self.session):
                raise Exception('FB login failed')
        except Exception as e:
            return None

        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like '
                                                   'Gecko) Chrome/65.0.3325.181 Safari/537.36',
                                     # 'accept-encoding': 'gzip, deflate, br',
                                     # 'charset': 'utf-8',
                                     # 'accept - language': 'el - GR, el;q = 0.9, cy;q = 0.8, en;q = 0.7',
                                     # 'accept': '* / *',
                                     # 'dnt': '1',
                                     # 'cookie': 'datr=' + self.session.cookies._cookies['.facebook.com']['/']['datr'].value
                                     #        + 'sb=' + self.session.cookies._cookies['.facebook.com']['/']['sb'].value
                                     #        + 'xs=' + self.session.cookies._cookies['.facebook.com']['/']['xs'].value
                                     })


        # the output dictionary, with profile IDs as keys and a list of words or phrases as values
        output = {}

        for target in targets.keys():
            output[target] = []
            # make sure value fields are lists
            if type(targets[target]) is not list:
                targets[target] = [targets[target]]

            for url in targets[target]:
                html_data = send_request(self.session, url)
                extracted_data = parse(html_data)
                output[target].extend(extracted_data)

        print(output)

        # save output to a JSON file
        json_output = json.dumps(output)
        f = open("output.json", "w")
        f.write(json_output)
        f.close()
        return


if __name__ == '__main__':
    info = Gather(test=True)
    info.CETS()
