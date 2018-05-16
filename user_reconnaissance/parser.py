"""
This module is responsible for parsing our fields of interest with BeautifulSoup, given the respective minified versions of their CSS
class names and the HTML code, whether it's about profile fields or search results from Facebook
"""

from bs4 import BeautifulSoup


def parse(input_html_data: str, search_type: str=None):
    """
    Depending on the search type, in_profile of graph_search, this function will extract as many information as
    possible, out of those that are of our interest

    -Search results such as Pages or Friends names can be found inside of <div class=”_32mo”><span></span></div>
    -Profile info (about):
        Birthday: <span class="_c24 _2ieq"><div><div></div><span class="accessible_elem">Birthday</span></div></span>
        Information (city, workplace etc) parent divs: <div class="_6a _5u5j _6b"></div>
        Current city, Marital status (Married), Schools, Workplaces: <div class="_c24 _50f4"></div>. The values that
        we’re interested in may be followed by phrases like “Lives in” or “Married to”.
        Extra info like Homeplace or marriage date: <div class="_50f8 _2ieq"><div class="fsm fwn fcg"></div></div>
        Name: <a class="_2nlw _2nlv"></a>
    """

    soup = BeautifulSoup(input_html_data, 'lxml')

    extracted_info = []

    if search_type == 'about':
        findings = soup.find_all(attrs={'class': ['_2nlw _2nlv', '_c24 _2ieq', '_6a _5u5j _6b']})
    else:
        # all search results appear under the class '_32mo' so we just need to use find_all
        findings = soup.find_all(class_='_32mo')

    for item in findings:
        if item.find(class_='_c24 _50f4'):
            extracted_info.append(item.find(class_='_c24 _50f4').text)
            if item.find(class_='_50f8 _2ieq'):
                for sub_item in item.find_all(class_='_50f8 _2ieq'):
                    extracted_info.append(sub_item.find(class_='fsm fwn fcg').text)
        else:
            extracted_info.append(item.text)

    return extracted_info
