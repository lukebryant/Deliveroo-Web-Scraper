from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import threading
import datetime
import sqlite3
import time


def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

def writeSnapShotToCSV(csvfile, restaurants):
	html = urlopen("https://deliveroo.co.uk/restaurants/bristol/bedminster?&day=today&time=ASAP&tags=")
	reqTime = datetime.datetime.now()
	bsObj = BeautifulSoup(html.read(), "html.parser")
	mylis = bsObj.find_all("li", { "class" : "restaurant-index-page-tile" })
	index = 1;
	times = [0] * (1 + len(restaurants) * 2);
	for li in mylis:
		timeRange = li.find("span", { "class" : "restaurant-index-page-tile--time-number-range" })
		timeAt = li.find("span", { "class" : "restaurant-index-page-tile--time-number" })
		restaurantText = li.find("h3").text if li.find("h3") is not None else ""
		timeRangeText = timeRange.text if timeRange is not None else " "
		timeAtText 		= timeAt.text if timeAt is not None else " "
		times[0] = reqTime;
		if restaurantText in restaurants:
			times[restaurants[restaurantText] * 2 + 1] = timeRangeText;
			times[restaurants[restaurantText] * 2 + 2] = timeAtText;
	try:
		writer.writerow(times)
	except PermissionError:
		print("File is open elsewhere, so can't write")

def initialiseCSV(csvfile):
	html = urlopen("https://deliveroo.co.uk/restaurants/bristol/bedminster?&day=today&time=ASAP&tags=")
	bsObj = BeautifulSoup(html.read(), "html.parser")
	mylis = bsObj.find_all("li", { "class" : "restaurant-index-page-tile" })
	restaurantsDict = dict();
	deliveryTimeColumnNames = ["TimeStamp"];
	index = 0;
	for li in mylis:
		restaurantText = li.find("h3").text if li.find("h3") is not None else ""
		if restaurantText not in restaurantsDict:
			restaurantsDict[restaurantText] = index
			deliveryTimeColumnNames += ['Expected Delivery Time', 'Delivery At']
			index+=1
	try:
		writer.writerow([""] + intersperse(list(restaurantsDict.keys()),""))
		writer.writerow(deliveryTimeColumnNames)
	except PermissionError:
		print("File is open elsewhere, so can't write")
	return restaurantsDict

with open('waitTime' + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + '.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	restaurantsDict = initialiseCSV(csvfile)
	# connection = sqlite3.connect("company.db")
	# cursor = connection.cursor()
	# sql_command = """
	# CREATE TABLE restaurant ( 
	# restaurant_number INTEGER PRIMARY KEY, 
	# name VARCHAR(20), 
	# est_range CHAR(10), 
	# # est_time CHAR(10)
	# # )""";
	# cursor.execute(sql_command);
	# connection.commit()
	# connection.close()
	while(1):
		# threading.Timer(30, 	writeSnapShotToCSV(csvfile,restaurantsDict)).start()
		writeSnapShotToCSV(csvfile,restaurantsDict)
		time.sleep(60)

