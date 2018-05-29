"""
This module is responsible for parsing our fields of interest with BeautifulSoup, given the respective minified versions of their CSS
class names and the HTML code, whether it's about profile fields or search results from Facebook
"""

from bs4 import BeautifulSoup
import configparser
import json

fields_data = configparser.ConfigParser()
fields_data.read('data.ini')

def get_field(extracted_info, item, type, contents):
    extracts = []
    extracts.append(item.find(class_='_c24 _50f4').text)
    if item.find(class_='_50f8 _2ieq'):
        for sub_item in item.find_all(class_='_50f8 _2ieq'):
            extracts.append(sub_item.find(class_='fsm fwn fcg').text)

    for useless_text in contents:
        for pos, extract in enumerate(extracts):
            extracts[pos] = str(extract).replace(useless_text, '')


    extracted_info[type] = extracts

def parse(input_html_data: str, search_type: str=None):
    """
    Depending on the search type, in_profile of graph_search, this function will extract as many information as
    possible, out of those that are of our interest

    -Search results such as Users, Pages or Friends names can be found inside of <div class=”_32mo”><span></span></div>
    -Profile info (about):
        Birthday: <span class="_c24 _2ieq"><div><div></div><span class="accessible_elem">Birthday</span></div></span>
        Information (city, workplace etc) parent divs: <div class="_6a _5u5j _6b"></div>
        Current city, Marital status (Married), Schools, Workplaces: <div class="_c24 _50f4"></div>. The values that
        we’re interested in may be followed by phrases like “Lives in” or “Married to”.
        Extra info like Homeplace or marriage date: <div class="_50f8 _2ieq"><div class="fsm fwn fcg"></div></div>
        Name: <a class="_2nlw _2nlv"></a>
    -Get profile id: Find elements with div class="_3u1 _gli _uvb" and get "id" field from their JSON value
    """

    soup = BeautifulSoup(input_html_data, 'lxml')

    extracted_info = {}

    if search_type == 'about':
        findings = soup.find_all(attrs={'class': ['_2nlw _2nlv', '_c24 _2ieq', '_6a _5u5j _6b']})

        for item in findings:
            if ' '.join(item.attrs['class']) == '_6a _5u5j _6b':
                get_content = item.find(class_='_c24 _50f4')
                if get_content:
                    for field_type in fields_data["FIELDS"]:
                        if any(x in get_content.text for x in fields_data["FIELDS"][field_type].split(',')[:-1]):
                            get_field(extracted_info, item, field_type, fields_data["FIELDS"][field_type].split(',')[:-1])
            else:
                if ' '.join(item.attrs['class']) == '_2nlw _2nlv':
                    extracted_info['name'] = [item.text]
                elif ' '.join(item.attrs['class']) == '_c24 _2ieq':
                    extracted_info['birthday'] = [item.text.replace('Birthday', '')]
                else:
                    extracted_info['other']=[item.text]

    elif search_type == 'graph':
        # all search results appear under the class '_32mo' so we just need to use find_all
        extracted_info['other - search results'] = [item.text for item in soup.find_all(class_='_32mo')]

    else:
        # users search
        users = soup.find_all(class_='_3u1 _gli _uvb')
        for user in users:
            extracted_info.update({user.find(class_='_32mo').text
                                   + ' : '
                                   + str(json.loads(user.attrs['data-bt'])['id'])
                                   +'\n' : None})

    return extracted_info
