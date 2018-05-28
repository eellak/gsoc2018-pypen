"""
This module is the entry point to our user reconnaissance flow. It creates an instance of our Extractor class, logs in
to Facebook, extracts & saves information for users in the target list (JSON file), generates a wordlist per user and
then calls John The Ripper for password cracking
"""
import argparse
import configparser


# custom modules import
from info_extract import Extractor
from wordlist_gen import generate_words, add_words
from summon_john import crack
from get_users import get_users

config = configparser.ConfigParser()
config.read('data.ini')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # enter '-test 1' while executing to run test scenario
    parser.add_argument('-test', help='Run test scenario')
    # Targets file in JSON format
    parser.add_argument('-file', help='Targets file (.json)')
    # JtR rules for word mangling during cracking procedure
    parser.add_argument('-rules', help='JtR rules (Default: "Custom"). See john.conf for all rules available')
    # JtR hash type
    parser.add_argument('-format', help='JtR hash format (Default: "Auto-detect")')
    # Page ID of company/organization etc to get users from
    parser.add_argument('-pageid', help='Page ID of company/organization etc to get users from')

    args = parser.parse_args()

    # instantiate our Extractor class
    extractor = Extractor()

    # log in Facebook in order to be able to retrieve data
    extractor.fb_login()

    # find users
    if args.pageid:
        get_users(extractor, args.pageid)
        exit()

    # extract user data
    extractor.extract(test=args.test, targets_filename=args.file)

    # save extracted data to results folder
    extractor.save()

    # add extra, user/company/organization specific words to wordlists
    add_words()

    # generate wordlists
    user_wordlists = generate_words()

    crack(user_wordlists, args.test, args.format, args.rules, config)

    exit()
