# scraper for pulling historical NCAA Basketball stats for machine learning project from sports-reference.com
# used http://docs.python-guide.org/en/latest/scenarios/scrape/ as a reference for libraries.
# If you use this, don't be a jerk, and limit the rate of your requests to something human-scale.

from lxml import html 	#req'd install
import requests			#req'd install
import time
import csv

def serializeDataAsCSV(data,filename,headers=None):
	with open(filename, 'wb') as csvfile:
		writer= csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		if (headers is not None):
			writer.writerow(headers)
		for line in data:
			writer.writerow(line)

def fetchAdvStatsForYear(year):
	page = requests.get("http://www.sports-reference.com/cbb/seasons/"+str(year)+"-advanced-school-stats.html")
	tree = html.fromstring(page.content)

	rows = tree.xpath("//tbody//tr[not(contains(@class,'over_header'))]/td[not(a)] | //tbody//tr[not(contains(@class,'over_header'))]/td/a")
	item = 0
	current=[str(year)]
	output=[]
	for row in rows:
		item+=1
		if (item % 17 != 0):
			current.append(row.text_content())
		if (item % 30 == 0):
			output.append(current)
			current=[str(year)]
			item=0

	return output;

def fetchBasicStatsForYear(year):
	page = requests.get("http://www.sports-reference.com/cbb/seasons/"+str(year)+"-school-stats.html")
	tree = html.fromstring(page.content)

	rows = tree.xpath("//tbody//tr[not(contains(@class,'over_header'))]/td[not(a)] | //tbody//tr[not(contains(@class,'over_header'))]/td/a")
	item = 0
	current=[str(year)]
	output=[]
	for row in rows:
		item+=1
		if (item != 17):
			current.append(row.text_content())
		if (item % 34 == 0):
			output.append(current)
			current=[str(year)]
			item=0
	return output;



advHeaders = ["year","alpha_order","school","games","games_won","games_lost","win_loss_pct","srs","sos","conf_wins","conf_losses","home_wins","home_losses","away_wins","away_losses","points_scored","opponent_points_scored","pace","offensive_rating","free_throw_attempt_rate","three_point_attempt_rate","true_shooting_pct","total_rebound_pct","assist_pct","steal_pct","block_pct","effective_field_goal_pct","turnover_pct","offensive_rebound_pct","free_throws_per_field_goal_attempt_rate"]
basicHeaders = ["year","alpha_order","school","games","games_won","games_lost","win_loss_pct","srs","sos","conf_wins","conf_losses","home_wins","home_losses","away_wins","away_losses","points_scored","opponent_points_scored","minutes_played","field_goals","field_goal_attempts","field_goal_pct","three_point_goals","three_point_attempts","three_point_pct","free_throws","free_throw_attempts","free_throw_pct","offensive_rebounts","total_rebounds","assists","steals","blocks","turnovers","personal_fouls"]
years=[2014]
outputDirectory="/tmp/"
#years = [yr for yr in range(1995,2016)]

output = []
for year in years:
	output = fetchAdvStatsForYear(year)
	print(str(len(output))+" advanced records fetched for "+str(year))
	serializeDataAsCSV(output,outputDirectory+"team_stats_"+str(year)+"_adv.csv",headers=advHeaders)
	print("Advanced records written for "+str(year))
	output = fetchBasicStatsForYear(year)
	print(str(len(output))+" basic records fetched for "+str(year))
	serializeDataAsCSV(output,outputDirectory+"team_stats_"+str(year)+"_basic.csv",headers=basicHeaders)
	print("Basic records written for "+str(year))
	time.sleep(30) #don't be a jerk, limit to 2 requests/minute
