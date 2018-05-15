"""
This module is responsible for parsing our fields of interest with BeautifulSoup, given the respective minified versions of their CSS
class names and the HTML code, whether it's about profile fields or search results from Facebook
"""

from bs4 import BeautifulSoup


def parse(input_html_data: str, search_type: str=None):
    """
    Depending on the search type, in_profile of graph_search, this function will extract as many information as
    possible, out of those that are of our interest
    """
    # TODO when we get the HTML code properly, all that will be left is to encorporate more fields

    print("Parsing HTML data...")
    soup = BeautifulSoup(input_html_data, 'lxml')
    print(soup.find(id='pagelet_timeline_main_column'))
    print(soup.findAll('div', {'id': 'pagelet_timeline_main_column'}))
    return soup.find_all(class_='_c24 _2ieq')
