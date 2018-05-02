import time
import requests
import datetime
import urllib

from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'Nikita'

LOGGER = getLogger(__name__)

class BusSkill(MycroftSkill):


    def __init__(self):
        super(BusSkill, self).__init__(name="BusSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))

        bus_travel_intent = IntentBuilder("BusTravelIntent").require("BusTravelKeyword").require("Source").require("Destination").require("Date").build()

         
        self.register_intent(bus_travel_intent, self.handle_bus_travel_intent)
        

    def handle_bus_travel_intent(self, message):
    	count = 0
    	source = message.data.get("Source")
    	#self.speak(source)
    	source = source.split(" ")[0] 
    	destination = message.data.get("Destination")
    	destination = destination.split(" ")[0] 
    	date = message.data.get("Date")	
    	date = date.split(" ")[0] 
    	url = "http://developer.goibibo.com/api/bus/search/?app_id=c0c99ed9&app_key=4078fd071b4df0fbbdf916b79e3f0de3&format=json&source="+source+"&destination="+destination+"&dateofdeparture="+date
    	response = requests.get(url).json()
	for i in response['data']['onwardflights']:
		skey = i['skey']
		encoded_skey = urllib.quote_plus(skey)
		busseat_url = "http://developer.goibibo.com/api/bus/seatmap/?app_id=c0c99ed9&app_key=4078fd071b4df0fbbdf916b79e3f0de3&skey=" + encoded_skey + "\""
		self.speak("Origin is " + i['origin'])
		self.speak("Departure time is " + i['DepartureTime'])
		self.speak("Arrival time is " + i['ArrivalTime'])
		self.speak("bus is " + i['seat'] + " and " + i['busCondition'])
		self.speak("Duration is " + i['duration'])
		self.speak("Total fare is " + i['fare']['totalfare'] + " and travels is " + i['TravelsName'])
		response1 = requests.get(busseat_url).json()
		print ("Seats available are ")
		for i in response1['data']['onwardSeats']:
			print (" " + i['SeatName'])


   
    def stop(self):
        pass

def create_skill():
    return BusSkill()

