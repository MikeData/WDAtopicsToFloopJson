# WDAtopicsToFloopJson
attempt to append WDA topics to floop data json - everything is documented in the jupyet notebook "MAIN PROCESSING". Most of this is fairly hacky but should make sense and we can intervene at any stage this way.

## whats in this repo?

orinal scraper.py   - what is sounds like

WDAfloopscrape .json    - the principle scrape delivered by the scraper

labels.json    - labels deliverd by the scraper

MAIN PROCESSING - jupyter notebook explaing all stages of what ive done and the code. you can click and read it in github if you dont want to run locally.

data.json - the data used for the floop graphic

ammendments.json - the new json we're appending to data.json

FINAL_WDAhackedintofloopdata.json - data.json with ammendments.json appended.

## NOTES

as it says in the notebook ive assumed ONS as organisation 24 (I think it was 24,the next free numner anyway). thats not defined anywhere yet and probably needs to be.
