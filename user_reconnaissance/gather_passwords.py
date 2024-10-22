#!/usr/bin/env python3
"""
This script is for testing purposes. It outputs passwords generated by JtR to created_passwords.py

File name: gather_passwords.py
Author: Konstantinos Christos Liosis
Date created: 24/5/2018
Python Version: 3.6.0
"""
import json
import os
from subprocess import run, PIPE
import hashlib
import configparser

config = configparser.ConfigParser()
config.read('data.ini')

test = True
rules = 'CustomHeavy'

try:
    pass_list = json.load(open(config['IO']['pass_list'] if not test else config['IO']['test_passwords'], 'r'))
except Exception as e:
    print(e)
    exit()

# check if john path is set correctly
if os.path.exists(config['MODULES']['jtr']) and \
        not run([config['MODULES']['jtr']], stdout=PIPE).returncode:
    print('JtR path is set correctly')
else:
    print("John The Ripper path is not set correctly. Please modify it in data.ini (check the docs for "
          "further info")
    exit()

for user in pass_list:

    if test:
        # text/demo scenario
        # create SHA256 hashes of our test profiles passwords
        pass_list[user] = hashlib.sha256(pass_list[user].encode('utf-8')).hexdigest()
        hash_type = 'raw-sha256'

    open('hashed_pass_' + user + '.txt', 'w').write(user + ':' + pass_list[user])

    user_file = open("created_passwords_" + user + ".txt", "w")
    # call JtR
    result = run([config['MODULES']['jtr'],
         "--wordlist=results/" + user + "_wordlist.lst",
         "--rules:" + (rules if rules else 'All'),
         "--stdout"], stdout=user_file)

    run(["rm", "hashed_pass_" + user + ".txt"])

    user_file.close()
