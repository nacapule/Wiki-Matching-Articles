import pywikibot
enwiki = pywikibot.Site('en', 'wikipedia')
enwiki_repo = enwiki.data_repository()


def item_page(qid=str):
    return pywikibot.ItemPage(enwiki_repo, qid)

def data_page(url=str):
    return pywikibot.Page(enwiki_repo, url)

def property_page(pid=str):
    return pywikibot.PropertyPage(enwiki_repo, 'Property:' + pid)

def wiki_claim(pid=str):
    return pywikibot.Claim(enwiki_repo, pid)

def print_page(url=str):
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

def print_wikidata_p(item_page=str, n = False):
    # We'll access this dic a number of times
    item_dict = item_page.get()

    print(item_page.title() + ' ' + item_dict['labels']['en'])
    print('\n+++++++++++++++++++++++++++++++')
    print('-------------------------------')

    # Create a list of all the P numbers from our item page
    if n == False:
        props = [prop for prop in item_dict['claims']]
    # Work with passed list of P numbers
    elif type(n) == list:
        props = n
    # Lastly, use the first n properties
    elif type(n) == int:
        props = [prop for prop in item_dict['claims']][:n]
    else:
        print('Error. Please check the property list.')
        return 0

    for prop in props:
        try:
            # Retrieve the property page object and extract the name
            # Printing just the P number is a faster, less descriptive alternative
            prop_page = property_page(prop)
            prop_label = prop_page.labels['en']
            print(prop + ' ' + prop_label)

            for claim in item_dict['claims'][prop]:
                # There are two scenarios: the value is a data item or not
                # Try to print the value Q number and label
                try:
                    qid = claim.getTarget().title()
                    label = claim.getTarget().labels['en']
                    print(qid + ' ' + label)
                # Else print the value object as is
                except:
                    print(claim.getTarget())

                # Getting the qualifiers when relevant
                # Code is analogous to the regular statements
                if claim.qualifiers:
                    for qprop, qvalues in claim.qualifiers.items():
                        qprop_page = property_page(qprop)
                        qprop_label = qprop_page.labels['en']
                        print(indent(qprop + ' ' + qprop_label, '     '))
                        for qvalue in qvalues:
                            # Same distinction. Qualifier value might be an item or not
                            try:
                                qid = qvalue.getTarget().title()
                                label = claim.getTarget().labels['en']
                                print(indent(str(qid) + ' ' + str(label), '     '))
                            except:
                                print(indent(str(qvalue.getTarget()), '     '))

            print('-------------------------------')
            print('-------------------------------')

        except:
            print('Error. Please check the property list.')
            break

        # The outer try can fail because: an element of props isn't a valid string P number,
        # or one of the P numbers isn't a key in item_dict['claims'] a.k.a that property can't be found
        # in our passed item page.

################################################################################

def print_wikidata(s, n = False):
    page = pywikibot.ItemPage(enwiki_repo, s)

    return print_wikidata_p(page, n)

################################################################################

def add_statement(qid=str, pid=str, value=str, value_type = 's'):
    # We will consider 2 scenarions: value_type = 's' for a string and 'q' for an item
    item = item_page(qid)
    claim = wiki_claim(pid)

    if value_type == 'q':
        try:
            target = item_page(value)
            claim.setTarget(target)
            item.addClaim(claim, summary=u'pywikibot test Outreachy')
            print(pid + ':' + value + ' added to ' + qid)
        except:
            print('Error. Please check value QID or credentials')

    if value_type == 's':
        try:
            target = pywikibot.WbMonolingualText(value,'en')
            claim.setTarget(target)
            item.addClaim(claim, summary=u'pywikibot test Outreachy')
            print(pid + ':' + value + ' added to ' + qid)
        except:
            print('Error. Please check credentials')

################################################################################

def add_qualifier(qid=str, pid1=str, value1=str, pid2=str, value2=str):
    # Similar to previous function with item values, but now we take outer and inner pids 
    item = item_page(qid)
    # We look for a the speficic property-value pair pid1-value1.
    for claim in item.claims[pid1]:
        if claim.getTarget().title() == value1:
            qualifier = wiki_claim(pid2)
            target = item_page(value2)
            qualifier.setTarget(target)
            claim.addQualifier(qualifier, summary=u'pywikibot test Outreachy')
            print(pid2 + ':' + value2 + ' added to ' + pid1 + ':' + value1 + ' in ' + qid)
