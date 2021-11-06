import pywikibot
enwiki = pywikibot.Site('en', 'wikipedia')
enwiki_repo = enwiki.data_repository()


def item_page(qid=str):
    return pywikibot.ItemPage(enwiki_repo, qid)

def data_page(url=str):
    return pywikibot.Page(enwiki_repo, url)

def raw_page_print(url=str):
    print(data_page(url).text)

################################################################################

def add_wikidata_text(url=str, added=str):
    # Adds text at the end of the page in a new line
    # Inputs are the string url after '/wiki/' and the added text

    page = pywikibot.Page(enwiki_repo, url)

    page.text = page.text + '\n\n' + added

    try:
        page.save("Text added through pywikibot")

    except:
        print('Error. Please check log in status.')

################################################################################

def print_wikidata_p(item_page, n = False):
    # We'll access this dic a number of times
    item_dict = item_page.get()

    print(item_page.title() + ' ' + item_dict['labels']['en'])
    print('\n+++++++++++++++++++++++++++++++')
    print('-------------------------------')

    if n == False:
        # Create a list of all the P numbers from our item page
        props = [prop for prop in item_dict['claims']]

    elif type(n) == list:
        # Work with passed list of P numbers
        props = n

    elif type(n) == int:
        # Lastly, use the first n properties
        props = [prop for prop in item_dict['claims']][:n]

    else:
        print('Error. Please check the property list.')
        return 0

    # We shall list all requested properties
    for prop in props:
        try:
            # Retrieve the property page object and extract the name
            # This is costly and might be improved
            # Printing just the P number is a faster alternative
            prop_page = pywikibot.PropertyPage(enwiki_repo, 'Property:' + prop)
            prop_name = prop_page.get()['labels']['en']
            print(prop + ' ' + prop_name)

            for claim in item_dict['claims'][prop]:
                print('\n')
                # There are two scenarios: the value is a data item or not

                try:
                # Try to print the value label and Q number
                    print('Value: ' + claim.getTarget().get()['labels']['en'])
                    print('Code: ' + claim.getTarget().title())

                except:
                # Else print the value as is
                    print('Value: ')
                    print(claim.getTarget())


            print('-------------------------------')
            print('-------------------------------')

        except:
            print('Error. Please check the property list.')
            break

        # The outer try can fail because: an element of props isn't a valid string P number,
        # or one of the P numbers isn't a key in item_dict['claims'] a.k.a that property can't be found
        # in our passed item page. Instead of convoluting the code with more excepts we print
        # a generic error message pointing at the property list

################################################################################

def print_wikidata(s, n = False):
    print_wikidata_p(item_page(s), n)
