# User Reconnaissance & Information gathering

This module's purpose is to gather information about Facebook users with public information on their profiles, and to create a collection of that information, which will be used in a dictionary attack.

## How to use

* `pip install requirements.txt`
* Download [chromedriver](http://chromedriver.chromium.org/downloads)
* Facebook login: can be achieved either by filling in your information when prompted to or by creating a file `facebook_credentials.txt` (which is ignored in the repository) with the following format (space separated or in 2 separate rows):
`emailusedforfacebook@email.com facebookpassword`

* `python info_gather.py -test 1` for running test scenario
* `python info_gather.py -file FILENAME` for running with your targets file

## Flow

* Facebook login
* Execution of each query of each target user
* HTML code retrieval by using a browser driver ([Selenium](http://selenium-python.readthedocs.io/) with chromedriver), since Facebook creates the HTML code, that includes our fields of interest, dynamically, after executing javascript code
* Parsing of the HTML code with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/). We extract the fields we need by searching for the `<div>` classes in which they belong
* Aggregation of the data per user in `output.json`