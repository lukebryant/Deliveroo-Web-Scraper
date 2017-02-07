from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import threading
import datetime

def writeSnapShotToCSV(csvfile, writer):
	html = urlopen("https://deliveroo.co.uk/restaurants/bristol/bedminster?&day=today&time=ASAP&tags=")
	reqTime = datetime.datetime.now()
	bsObj = BeautifulSoup(html.read(), "html.parser")
	mylis = bsObj.find_all("li", { "class" : "restaurant-index-page-tile" })
	writer.writerow(['Timestamp', 'Restaurant', 'Expected Delivery Time', 'Delivery At'])
	for li in mylis:
		timeRange = li.find("span", { "class" : "restaurant-index-page-tile--time-number-range" })
		timeAt = li.find("span", { "class" : "restaurant-index-page-tile--time-number" })
		restaurantText = li.find("h3").text if li.find("h3") is not None else ""
		timeRangeText = timeRange.text if timeRange is not None else " "
		timeAtText 		= timeAt.text if timeAt is not None else " "
		writer.writerow([reqTime, restaurantText, timeRangeText, timeAtText])
	return

with open('waitTime.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	for i in range (0,1):
		threading.Timer(0.5, 	lambda: writeSnapShotToCSV(csvfile, writer)).start()
