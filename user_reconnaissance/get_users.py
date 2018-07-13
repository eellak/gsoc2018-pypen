#!/usr/bin/env python3
"""
This module is responsible for calling the Extractor methods specifically for user retrieval

File name: get_users.py
Author: Konstantinos Christos Liosis
Date created: 25/5/2018
Python Version: 3.6.0
"""

def get_users(extractor, page_id: str):

    # extract users
    extractor.extract(pageid=page_id)

    # save extracted users to pageid_users_list.txt file
    extractor.save(pageid=page_id)