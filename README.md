# NCAAStatScraper
Simple scripts for extracting historical NCAA Basketball stats from sports-reference.com. I hacked it together for a Machine Learning project, but if you decide to use please make sure you limit your requests to something human-scale (as-implemented it sleeps 30s for every request or two)

You may need to install *lxml* and *requests* via pip.

Run NCAATournamentScraper.py to get NCAA Tournament ("March Madness") data, and set the minYear and maxYear variables to whatever time frame interests you.

Run NCAAScraper.py to get performance statistics by team. The years array holds all the years to pull.

Credits: Used http://docs.python-guide.org/en/latest/scenarios/scrape/ as a reference for libraries.
