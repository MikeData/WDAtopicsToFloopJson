# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 13:46:33 2017

@author: Mike
"""

from bs4 import BeautifulSoup
import json, requests

def get_all_datasets(APIKEY):
    
    # for duplicate ids we'll just add a growing number to the end (for now)
    def recurse(myid, scrape, count=2):
        if myid + ' ' + str(count) in scrape.keys():
            recurse(myid, scrape, count+1)
        return myid + ' ' + str(count)
        
        
    """
    For each dataset we're looking to build a json file to being with of
    
    datasetID: {
                datasetName: 'Dataset 1' 
                context:'Census',
                dimensions: ['age, gender, etc]
                  },
    repeat....
    
    NOTE - jurys our on which url but if we have the ID and the context, we can make as we need...probably
    """
    
    scrape = {}
    lookups = {}

    for context in ['Social', 'Economic', 'Census']:

        # Get all URLs
        url = 'http://data.ons.gov.uk/ons/api/data/datasets.xml?apikey=Y6Xs59zXU0&context={con}'.format(con=context)
    
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        
        # get the dataset details .json API call for each dataset
        allDatasetDetails = soup.find_all('url', {'representation':'json'})
        
        # just the text, filter out any crap
        allDatasetDetails = [x.text for x in allDatasetDetails if 'datasetdetails' in x.text]
    
        for dset in allDatasetDetails:
    
            url = 'http://data.ons.gov.uk/ons/api/data/' + dset
            
            jdata = requests.get(url)
            detailsAsJson = json.loads(jdata.text)
            
            # lost the filler
            
            detailsAsJson = detailsAsJson['ons']['datasetDetail']
    
            myid = detailsAsJson['id']
            url = "<p>Not implemented yet</p>"
            name = detailsAsJson['names']['name'][0]['$']
            topics = []
    
            for x in range(0, len(detailsAsJson['dimensions']['dimension'])):
                # dname = detailsAsJson['dimensions']['dimension'][x]['dimensionId']

                engname = detailsAsJson['dimensions']['dimension'][x]['dimensionTitles']['dimensionTitle'][0]['$']
                codename = detailsAsJson['dimensions']['dimension'][x]['dimensionId']
                
                topics.append(codename)
                if codename in lookups.keys():
                    if engname != lookups[codename]:
                        # assert engname == lookups[codename], "Code {code} representing both '{c}' and '{d}'".format(code=codename, c=engname, d=lookups[codename])
                        if type(lookups[codename]) != list:
                            lookups[codename] = [lookups[codename], engname]
                        else:
                            if engname not in lookups[codename]:
                                lookups[codename].append(engname)
                else:
                    lookups.update({codename:engname})

            if myid in scrape.keys():
                myid = recurse(myid, scrape)
            
            scrape.update({myid: {'name':name, 'url':url, 'topics':topics, 'context':context}})
        
    return scrape, lookups
    
        
    
    
    
    
scrape, lookups = get_all_datasets('Y6Xs59zXU0')

with open("WDAfloopscrape.json", "w") as outfile:
    json.dump(scrape, outfile)

with open("labels.json", "w") as outfile:
    json.dump(lookups, outfile)
