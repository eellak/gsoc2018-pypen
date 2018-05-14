'''
This is the main information gathering module. By calling the send_request function, it will retrieve the HTML code of
the results, it will send it to the parser and then it will store the data for this user in an appropriate structure.
'''

import requests

# custom modules import
from send_req import send_request
from parser import parse

session = requests.Session()

html_data = send_request(session, test=True)

print("HTML data is retrieved")
print(html_data)

extracted_data = parse(html_data)