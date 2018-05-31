# User Reconnaissance & Information gathering

This module's purpose is to gather information about Facebook users with public information on their profiles, and to create a collection of that information, which will be used in a dictionary attack.

## How to use

### Setup

Tested & working on Ubuntu 16.04 and elementaryOS with Python 3.5.2 and Python 3.6.0

* Execute: `pip install -r requirements.txt`
* Download [chromedriver](http://chromedriver.chromium.org/downloads)
* Facebook login: can be achieved either by filling in your information when prompted to or by creating a file `facebook_credentials.txt` (which is ignored in the repository) with the following format (space separated or in 2 separate rows):
`emailusedforfacebook@email.com facebookpassword`
* Download [JohnTheRipper - Jumbo Version](https://github.com/magnumripper/JohnTheRipper/archive/bleeding-jumbo.tar.gz). After downloading, extract the file, go to `/src` subdirectory and execute: `./configure && make`.
Once you're done, inside of the `/run` sub-directory you'll find `john` executable. Copy it's path and paste it in our `data.ini` file, in the **jtr** field, under the **MODULES** section.
* When you're done with building JtR, copy the `john.conf` file that you'll find in `/user_reconnaissance` in the `/run` sub-directory of JohnTheRipper folder, replacing the existing configuration file. This is needed in order for the model to use our rules for password cracking. With our configuration file, apart from all the rules provided by the jumbo version of JtR, one can use the rules **Custom** (a combination of preexisting rules, is the default) and **CustomHeavy** which can crack (by brute-force) a bit more passwords with complicated suffixes (can be quite time consuming)

If you completed the above, then you're done setting the prerequisites. Now you'll have to provide our module with the information necessary, in a suitable format.

### Input data - Execution

* A target users file, in `JSON` format. The key fields consist of user IDs and the value fields are lists of queries (URLs) that you want to execute for each target (About page, Pages liked etc). You can take a look at `demo/test_targets.json`. The name of your targets file will be provided as the `-file` option (see below). For testing purposes, 5 Facebook profiles have been created, the IDs of whom you'll find in the demo files.
* A passwords list, in `JSON` format. The filename should be `pass_list.json` (or you can change it in `data.ini`). The key fields consist of user IDs and the value fields are hashed passwords. It is recommended that you provide the hash type of these passwords as the `-format` option (available hash types [here](http://pentestmonkey.net/cheat-sheet/john-the-ripper-hash-formats). You can take a look at `demo/test_pass_list.json`.
* A file for extra words to be added in the wordlists (optional). The filename should be `extra_words.txt` and it should contain one word per line. This file can provide useful words for targeted applications. For example, if you're trying to crack the passwords of the employees of a company named **EXAMPLE COMPANY**, adding the word **example** in the extra words file will possibly increase your cracking success.
* By executing `python run.py -pageid PAGE_ID` where *PAGE_ID* is the Facebook Page ID of the business/organization, the employees of which you're interested in, you'll get as output a file `PAGE_ID_users_list.txt` with the Facebook users that were found to be associated with that page (in the format *NAME : USER_PROFILE_ID*) and a properly formatted JSON file (`PAGE_ID_target_users.json`), ready to use as input to our information gathering module. You can later use these files in conjunction with a local database (or something similar containing hashes of passwords of that target group) to form a proper JSON file (`pass_list.json` as described above) for password cracking in order to check the user passwords' strength. Depending on the number of users that are associated with that page and your connection speed, the script may end up running for a long amount of time, since the results page is loaded by scrolling down through the webdriver, meaning we should wait for the data to load after each scroll and repeat that procedure until we get to the bottom of the page.

* `python run.py -test 1` for running test scenario
* `python run.py -file FILENAME` for running with your targets file

Example
* `python run.py -file my_targets.json -format raw-sha256 -rules CustomHeavy`

You can always use `python run.py --help` for information about options.
Many parameters (such as filenames of input/output files etc) can be changed at will through `data.ini` file.

## Flow

* Facebook login
* Execution of each query of each target user
* HTML code retrieval by using a browser driver ([Selenium](http://selenium-python.readthedocs.io/) with chromedriver), since Facebook creates the HTML code, that includes our fields of interest, dynamically, after executing javascript code
* Parsing of the HTML code with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/). We extract the fields we need by searching for the `<div>` classes in which they belong
* Aggregation of the data per user in `output.json`
* Additional words for wordlist (optional). Unless you have created a `extra_words.txt` file, you'll be prompted about whether or not you'd like to add some extra, ad-hoc words in the wordlist
* Wordlist generation per user, results saved in the respective subdir
* Password cracking with [JohnTheRipper](http://www.openwall.com/john/) according to our settings (rules, wordlist etc), output saved in `cracked_password.txt`

### Disclaimer

*The purpose of this library is educational, for Penetration Testing and Ethical Hacking and under no circumstances for malicious actions. It's use will comply to all current data protection legislation.*