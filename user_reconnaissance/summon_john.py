"""
This module is responsible for executing John The Ripper for password cracking
"""
import json
import os
from subprocess import run, PIPE
import hashlib


def crack(users_list, test, hash_type, rules, config):
    """
    TODO docstring
    """
    pass_list = json.load(open(config['IO']['pass_list'] if not test else config['IO']['test_passwords'], 'r'))

    for user in users_list:

        if test:
            # create SHA256 hashes of our test profiles passwords
            pass_list[user] = hashlib.sha256(pass_list[user].encode('utf-8')).hexdigest()
            hash_type = 'raw-sha256'

        open('hashed_pass_' + user + '.txt', 'w').write(user + ':' + pass_list[user])

        # call JtR
        run([config['MODULES']['jtr'],
              "--wordlist=results/" + user + "_wordlist.lst",
              "--format=" + hash_type if hash_type else "",
              "--rules:" + (rules if rules else 'All'),
              "hashed_pass_" + user + ".txt"])

        # save cracked passwords in the respective folder, each UserID in it's file
        result = run([config['MODULES']['jtr'],
              "--show",
              "--format=" + hash_type if hash_type else "",
              "hashed_pass_" + user + ".txt"], stdout=PIPE)

        run(["rm", "hashed_pass_" + user + ".txt"])

        result = result.stdout.decode('utf-8').split('\n')[0]
        open("cracked_passwords.txt", "a").write(result+'\n')

    return None
