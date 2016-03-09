# scraper for pulling historical NCAA Tournament Result stats for machine learning project from sports-reference.com
# used http://docs.python-guide.org/en/latest/scenarios/scrape/ as a reference for libraries.
# If you use this, don't be a jerk, and limit the rate of your requests to something human-scale.

import requests
from lxml import html
import time
import csv

def serializeDataAsCSV(data,filename,headers=None):
	with open(filename, 'wb') as csvfile:
		writer= csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		if (headers is not None):
			writer.writerow(headers)
		for line in data:
			writer.writerow(line)

def fetchData(minYear,maxYear):
	print("Retrieving NCAA Tournament data for "+str(minYear)+"-"+str(maxYear))
	offset = 0
	goToNext=True
	output = []
	while goToNext:
		url = "http://www.sports-reference.com/cbb/play-index/tourney.cgi?request=1&match=single&year_min="+str(minYear)+"&year_max="+str(maxYear)+"&round=&region=&location=&school_id=&conf_id=&opp_id=&opp_conf=&seed=&seed_cmp=eq&opp_seed=&opp_seed_cmp=eq&game_result=&pts_diff=&pts_diff_cmp=eq&order_by=date_game&order_by_asc=&offset="+str(offset)
		page = requests.get(url)
		tree = html.fromstring(page.content)
		rows = tree.xpath("//table[contains(@class,'stats_table')]/tbody//tr/td[not(a)] | //table[contains(@class,'stats_table')]/tbody//tr/td/a |  //table[contains(@class,'stats_table')]/tbody//tr/td/a/preceding-sibling::text()")
		colNum = 0
		record = []
		for row in rows:
			if colNum == 5 or colNum == 8: #seeds, they come in with unicode junk and need to be stripped
				record.append(row.strip())
			elif colNum>0: #skip first col, which is arbitrary "rank" number based on sort order
				record.append(row.text_content())
			if colNum == 13: #final column, wrap
				colNum=0
				output.append(record)
				record=[]
			else:
				colNum+=1
		checkForNextPage = tree.xpath("//p//a[text()='Next page']")
		if (len(checkForNextPage)>0):
			goToNext=True
			offset+=100
			print("retrieved first "+str(offset)+" records. Sleeping.")
			time.sleep(30)
		else:
			goToNext=False;
	return(output)


minYear=1996
maxYear=2015
outputFile="/tmp/ncaa_tournament_history.csv"
headers = ["year","date","region","round","seed_A","school_A","points_A","seed_B","school_B","points_B","overtime","point_diff","location"]

outData = fetchData(minYear,maxYear)
print("finished retrieving "+str(len(outData))+" records. Exporting...")
serializeDataAsCSV(outData,outputFile,headers=headers)
print("Exported to: "+outputFile)
