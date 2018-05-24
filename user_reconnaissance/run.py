"""
This module is the entry point to our user reconnaissance flow. It creates an instance of our Extractor class, logs in
to Facebook, extracts & saves information for users in the target list (JSON file), generates a wordlist per user and
then calls John The Ripper for password cracking
"""
import argparse
import configparser


# custom modules import
from info_extract import Extractor
from wordlist_gen import generate_words
from summon_john import crack

config = configparser.ConfigParser()
config.read('data.ini')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # enter '-test 1' while executing to run test scenario
    parser.add_argument('-test', help='Run test scenario')
    parser.add_argument('-file', help='Targets file (.json)')
    # JtR rules for word mangling during cracking procedure
    parser.add_argument('-rules', help='JtR rules (Default: "Custom"). See john.conf for all rules available')
    # JtR hash type
    parser.add_argument('-format', help='JtR hash format (Default: "Auto-detect")')

    args = parser.parse_args()

    extractor = Extractor()

    extractor.fb_login()

    extractor.extract(test=args.test, targets_filename=args.file)

    extractor.save()

    users_list = generate_words()

    crack(users_list, args.test, args.format, args.rules, config)
