"""
This module is responsible for calling the Extractor methods specifically for user retrieval
"""


def get_users(extractor, page_id: str):

    # extract users
    extractor.extract(pageid=page_id)

    # save extracted users to pageid_users_list.txt file
    extractor.save(pageid=page_id)