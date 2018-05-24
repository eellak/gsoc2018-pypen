# User Reconnaissance & Information gathering

This module's purpose is to gather information about Facebook users with public information on their profiles, and to create a collection of that information, which will be used in a dictionary attack.

## How to use

* Execute: `pip install -r requirements.txt`
* Download [chromedriver](http://chromedriver.chromium.org/downloads)
* Facebook login: can be achieved either by filling in your information when prompted to or by creating a file `facebook_credentials.txt` (which is ignored in the repository) with the following format (space separated or in 2 separate rows):
`emailusedforfacebook@email.com facebookpassword`
* Download [JohnTheRipper - Jumbo Version](https://github.com/magnumripper/JohnTheRipper/archive/bleeding-jumbo.tar.gz). After downloading, extract the file, go to `src` subdirectory and execute: `./configure && make`.
Once you're done, inside of the `run` subdirectory you'll find `john` executable. Copy it's path and paste it in our data.ini file, in the **jtr** field, under the **MODULES** section. 
If you completed the above, then you're done setting the prerequisites. Now you'll have to provide our module with the information necessary, in a suitable format.

### Input data

* A target users file, in `JSON` format. The key fields consist of user IDs and the value fields are lists of queries (URLs) that you want to execute for each target (About page, Pages liked etc). You can take a look at `demo/test_targets.json`. The name of your targets file will be provided as the `-file` option (see below)
* A passwords list, in `JSON` format. The filename should be `pass_list.json` (or you can change it in `data.ini`). The key fields consist of user IDs and the value fields are hashed passwords. It is recommended that you pass the hash type of these passwords as the `-format` option (available hash types [here](http://pentestmonkey.net/cheat-sheet/john-the-ripper-hash-formats). You can take a look at `demo/test_pass_list.json`.

* `python run.py -test 1` for running test scenario
* `python run.py -file FILENAME` for running with your targets file

Example
* `python run.py -file my_targets.json -format raw-sha256 -rules Jumbo`

## Flow

* Facebook login
* Execution of each query of each target user
* HTML code retrieval by using a browser driver ([Selenium](http://selenium-python.readthedocs.io/) with chromedriver), since Facebook creates the HTML code, that includes our fields of interest, dynamically, after executing javascript code
* Parsing of the HTML code with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/). We extract the fields we need by searching for the `<div>` classes in which they belong
* Aggregation of the data per user in `output.json`
* Wordlist generation per user, results saved in the respective subdir
* Password cracking with [JohnTheRipper](http://www.openwall.com/john/) according to our settings (rules, wordlist etc), output saved in `cracked_password.txt`