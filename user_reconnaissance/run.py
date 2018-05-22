"""

"""
import argparse
from subprocess import call
import hashlib
import configparser
import json

# custom modules import
from info_extract import Extractor
from wordlist_gen import generate

config = configparser.ConfigParser()
config.read('data.ini')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # enter '-test 1' while executing to run test scenario
    parser.add_argument('-test', help='Run test scenario')
    parser.add_argument('-file', help='Targets file (.json)')

    args = parser.parse_args()

    extractor = Extractor()

    extractor.fb_login()

    extractor.cets(test=args.test, targets_filename=args.file)

    extractor.save()

    users_list = generate()

    pass_list = json.load(open(config['IO']['pass_list'], 'r'))

    for user in pass_list:
        pass_list[user] = hashlib.sha256(pass_list[user].encode('utf-8')).hexdigest()

        open('hashed_pass_' + user + '.txt', 'w').writelines(pass_list[user])

        call(["john", "-wordlist=results/" + user + "wordlist.lst", "-rules", "hashed_pass_" + user + ".txt"])
        call(["rm", "hashed_pass_" + user + ".txt"])