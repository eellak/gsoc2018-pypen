"""
This module is responsible for creating a input wordlist for our dictionary attacks with JtR. This is done by
combining the words from particular word groups that have a good likelihood of forming a password (like "name"
and "birthday"). Phrases are broken down to words, dates written in full are tranformed to numeric form.
"""
from itertools import combinations_with_replacement
import json
import configparser
import re
import os
from dateutil.parser import parse
import itertools

config = configparser.ConfigParser()
config.read('data.ini')

fields_map = config['FIELDS_MAP']

# regular expression for date detections, details following below
date_pattern = re.compile(r'^[a-zA-Z]{3,8}\s[0-9]{1,2}\,\s[0-9]{4}$')

def generate():
    in_file = open(config['IO']['extracted_data'], 'r')
    in_data = json.load(in_file)

    for user in in_data:
        wordlist = []

        for field in in_data[user]:
            # step1: convert dates to numeric form in all possible variations. Dates can be found in the following fields:
            # birthday, family and relationship status. Facebook dates follow a certain pattern:
            # month (written in full) day (numeric), year (numeric)
            # we will make use of that to easily tranform it
            if (fields_map['bday'] or fields_map['fam_rel']) == field:
                entries_to_add = []

                for pos, value in enumerate(in_data[user][field]):
                    pos_to_del = None
                    if re.search(date_pattern, value):
                        # we will delete this entry afterwards
                        pos_to_del = pos
                        fb_date = parse(re.search(date_pattern, value).string)
                        entries_to_add = [fb_date.strftime(config['DATE_FORMATS'][date_format]) for date_format
                                          in config['DATE_FORMATS']]

                if pos_to_del:
                    del(in_data[user][field][pos_to_del])

                # lstrip() leading zeros as additional format
                entries_to_add.extend([x.lstrip('0') for x in entries_to_add])
                in_data[user][field].extend(entries_to_add)

        # step2: break down to words
        def flatten(nested_list):
            return list(set(itertools.chain.from_iterable(nested_list)))

        for field in in_data[user]:
            # split multi-word items and turn them to lowercase (JtR rules will try capitalization variations)
            in_data[user][field] = flatten(item.replace(',', '').split(' ') for item in in_data[user][field])
            wordlist.extend(list(map(lambda x: x.lower(), in_data[user][field])))

        # step3: combine fields given the rules we've defined
        # "family and relationship status" with itself
        # "family and relationship status" with “name”
        # “Name” with “birthday”
        # “Other - search results” with “birthday”
        # “Other - search results” with “name”
        to_append = []
        if fields_map['fam_rel'] in in_data[user]:
            to_append.extend(combinations_with_replacement(in_data[user][fields_map['fam_rel']] +
                                                           in_data[user][fields_map['fam_rel']], 2))
            to_append.extend(combinations_with_replacement(in_data[user][fields_map['fam_rel']] +
                                                           in_data[user][fields_map['fam_rel']], 3))
            to_append.extend(combinations_with_replacement(in_data[user][fields_map['fam_rel']] +
                                                           in_data[user][fields_map['name']], 2))
            to_append.extend(combinations_with_replacement(in_data[user][fields_map['fam_rel']] +
                                                           in_data[user][fields_map['name']], 3))
        if fields_map['other'] in in_data[user]:
            to_append.extend(combinations_with_replacement(in_data[user][fields_map['other']] +
                                                           in_data[user][fields_map['name']], 2))
            to_append.extend(combinations_with_replacement(in_data[user][fields_map['other']] +
                                                           in_data[user][fields_map['name']], 3))
            if fields_map['bday'] in in_data[user]:
                to_append.extend(combinations_with_replacement(in_data[user][fields_map['other']] +
                                                               in_data[user][fields_map['bday']], 2))
                to_append.extend(combinations_with_replacement(in_data[user][fields_map['other']] +
                                                               in_data[user][fields_map['bday']], 3))
                to_append.extend(combinations_with_replacement(in_data[user][fields_map['name']] +
                                                               in_data[user][fields_map['bday']], 2))
                to_append.extend(combinations_with_replacement(in_data[user][fields_map['name']] +
                                                               in_data[user][fields_map['bday']], 3))

        for item in to_append:
            wordlist.append(''.join(item).lower())

        if not os.path.exists('results'):
            os.makedirs('results')
        out_file = open('results/' + user + '_wordlist.lst', 'w')
        out_file.writelines([item+'\n' for item in wordlist])

    return in_data.keys()

