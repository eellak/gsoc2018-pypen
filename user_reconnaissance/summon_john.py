"""
This module is responsible for executing John The Ripper for password cracking
"""
import json
import os
from subprocess import run, PIPE
import hashlib


def crack(users_list: list, test: bool, hash_type: str, rules:str, config):
    """
    After getting a list of user passwords for a user defined file (filename found in data.ini['IO']['pass_list']), we
    call John The Ripper from the command line (subprocess.run) while defining various JtR options, such as the
    password hash type (md5, sha256 etc), mangling rules, wordlist input for dictionary attack. What's really important
    here is the correct setting of the 'john' executable path (in data.ini['MODULES']['jtr']) after building it.
    The output (crackd password) can be found in 'cracked_passwords.txt'
    """

    try:
        pass_list = json.load(open(config['IO']['pass_list'] if not test else config['IO']['test_passwords'], 'r'))
    except Exception as e:
        print(e)
        return None

    # check if john path is set correctly
    if os.path.exists(config['MODULES']['jtr']) and \
            not run([config['MODULES']['jtr']], stdout=PIPE).returncode:
        print('JtR path is set correctly')
    else:
        print("John The Ripper path is not set correctly. Please modify it in data.ini (check the docs for "
              "further info")
        return None

    for user in users_list:

        if test:
            # text/demo scenario
            # create SHA256 hashes of our test profiles passwords
            pass_list[user] = hashlib.sha256(pass_list[user].encode('utf-8')).hexdigest()
            hash_type = 'raw-sha256'

        open('hashed_pass_' + user + '.txt', 'w').write(user + ':' + pass_list[user])

        # call JtR
        run([config['MODULES']['jtr'],
              "--wordlist=results/" + user + "_wordlist.lst",
              "--format=" + hash_type if hash_type else "",
              "--rules:" + (rules if rules else 'Custom'),
              "hashed_pass_" + user + ".txt"])

        # save cracked passwords in the respective folder, each UserID in it's file
        result = run([config['MODULES']['jtr'],
              "--show",
              "--format=" + hash_type if hash_type else "",
              "hashed_pass_" + user + ".txt"], stdout=PIPE)

        run(["rm", "hashed_pass_" + user + ".txt"])

        result = result.stdout.decode('utf-8').split('\n')[0] \
            if '0 password hashes cracked' not in result.stdout.decode('utf-8').split('\n')[0] \
            else ''

        if result:
            open("cracked_passwords.txt", "a").write(result+'\n')

    return None
