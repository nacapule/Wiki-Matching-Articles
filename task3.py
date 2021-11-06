import pywikibot
from pywikibot import pagegenerators
from pywikibot.data import api
import requests
from task2 import item_page, print_wikidata


# From the provided example.py
def search_entities(site, itemtitle, limit):
    if limit <= 50:
     params = { 'action' :'wbsearchentities',
                'format' : 'json',
                'language' : 'en',
                'limit' : limit,
                'continue': 0,
                'type' : 'item',
                'search': itemtitle}
     request = api.Request(site=site, parameters=params)
     return request.submit()

################################################################################

 def search_item_description(label, limit):
# Using the API to return QIDs and their descriptions
    dic = search_entities(enwiki_repo, label, limit)
    # Record of found QIDs
    qids = [item['id'] for item in dic['search']]

    if dic:
        for item in dic['search']:
            page = item_page(item['id'])
            # Corroborating a correct item with pywikibot
            if page.get()['descriptions']['en'] == item['description']:
                print(item['id'] + ' ' + item['label'])
                # Show the description for the user to choose
                print(item['description'])
                print('\n')

            else:
                print(item['description'] + ' does not match')

    print('Select QID:')
    qid = input().upper()
    print('\n')
    print('+++++++++++++++++++++++++++++++')

    if qid not in qids:
        print('Warning: selected QID not a search result')

    return qid

################################################################################

# This function bridges the gap between Tasks 2 and 3
def item_properties(qid, n = False):
    page = item_page(qid)
    item_dict = page.get()

    print(page.title() + ' ' + item_dict['labels']['en'])
    print('\n+++++++++++++++++++++++++++++++')
    print('-------------------------------')

    # Display either all the item properties,
    if n == False
        props = [prop for prop in item_dict['claims']]
    # Or just the first n
    elif type(n) == int:
        props = [prop for prop in item_dict['claims']][:n]
    # Or we try for a passed list of props
    elif type(n) == list:
        props = n

    else:
        print('Error. Please check the property list.')
        return 0

    for prop in props:
        # Check if the solicited properties are in our data item
        if prop in item_dict['claims']:
            # We show both the P code and the property name, easier for user to choose
            prop_page = pywikibot.PropertyPage(enwiki_repo, 'Property:' + prop)
            prop_name = prop_page.get()['labels']['en']
            print(prop + ' ' + prop_name
        else:
            print('Warning: Property ' + prop + ' not in ' + qid)

################################################################################

# Integrating looking for a QID and showing info from its data page
def search_item_data(label, n, p):
    # n = number of items to display and select from
    # p = number or list of properties to display
    qid = search_item_description(label, n)
    return print_wikidata(qid, p)
