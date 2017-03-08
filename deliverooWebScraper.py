from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import threading
import datetime
import sqlite3
import time
import sys, re
from enum import Enum

class stringDayToEnum(Enum):
	Mon = 0
	Tue = 1
	Wed = 2
	Thu = 3
	Fri = 4
	Sat = 5
	Sun = 6

daysDict = {
	'Mon': 0,
	'Tue': 1,
	'Wed': 2,
	'Thu': 3,
	'Fri': 4,
	'Sat': 5,
	'Sun': 6
}

def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

def getOpeningTimes(link):
	html = urlopen("https://deliveroo.co.uk" + link)
	bsObj = BeautifulSoup(html.read(), "html.parser")	
	li = bsObj.find("ul", { "class" : "restaurant-info" })
	children = li.findChildren()
	for child in children:
		if child.has_attr('roo-tool-tipsy'):
			openingTimes = child
		# print(child.attrs)
	# print((openingTimes['roo-tool-tipsy']))
	content = openingTimes['roo-tool-tipsy'].split('content')
	# print(content)
	timesList = re.findall(r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)(?:-(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun))?:\s\d\d:\d\d-\d\d:\d\d',str(content))
	# testList = re.findall(r'[A-Z][a-z][a-z](?:-[A-Z][a-z][a-z])?:\s\d\d:\d\d-\d\d:\d\d',str(content))
	# print(timesList)
	openCloseTimes = ()
	for times in timesList:
		dayRange = times.split(": ")[0]
		# print(dayRange)
		if '-' in dayRange:
			startDay = daysDict[dayRange.split('-')[0]]
			endDay = daysDict[dayRange.split('-')[1]]
		else:
			startDay = daysDict[dayRange]
			endDay = daysDict[dayRange]
		openingTime = times.split(": ")[1].split("-")[0]
		closingTime = times.split(": ")[1].split("-")[1]
		# print("startDay = " + str(startDay))
		# print("endDay = " + str(endDay))
		for i in range (startDay,endDay+1):	
			openCloseTimes += (datetime.datetime.strptime(openingTime,"%H:%M").time(), datetime.datetime.strptime(closingTime,"%H:%M").time()),
			# print(i)
	return openCloseTimes
	# print(openCloseTimes)

	# input("Press Enter to continue...")


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
		# link = li.find("a", { "class" : "restaurant-index-page-tile--anchor" })
		print(li.a.get('href'))
		timeRangeText = timeRange.text if timeRange is not None else " "
		try:
			stringInts = timeRangeText.split("-")
			expectedTime = (int(stringInts[0].replace(" ", "")) + int(stringInts[1].replace(" ", "")))/2
		except ValueError:
			expectedTime = 99
		timeAtText = timeAt.text if timeAt is not None else " "
		times[0] = reqTime;
		if restaurantText in restaurants:
			times[restaurants[restaurantText][0] * 2 + 1] = expectedTime;
			times[restaurants[restaurantText][0] * 2 + 2] = timeAtText;
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
		openingTimes = getOpeningTimes(li.a.get('href'))
		if restaurantText not in restaurantsDict:
			restaurantsDict[restaurantText] = (index,openingTimes)
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
	if "Sotiris" not in restaurantsDict:
		print("Sotiris not found in dict")
	print(restaurantsDict["Sotiris"][0])
	print(restaurantsDict["Sotiris"][1])
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

