import time
import requests
import datetime
from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'Nikita'

LOGGER = getLogger(__name__)

class RailSkill(MycroftSkill):


    def __init__(self):
        super(RailSkill, self).__init__(name="RailSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))

        rail_code_intent = IntentBuilder("RailCodeIntent").require("RailCodeKeyword").require("Pname").build()
        self.register_intent(rail_code_intent, self.handle_rail_code_intent)

        rail_travel_intent = IntentBuilder("RailTravelIntent").require("RailTravelKeyword").require("Source").require("Destination").require("Date").build()
        self.register_intent(rail_travel_intent, self.handle_rail_travel_intent)

        rail_train_status_intent = IntentBuilder("RailTrainStatusIntent").require("RailTrainStatusKeyword").require("TrainNumber").require("Date").build()
        self.register_intent(rail_train_status_intent, self.handle_rail_train_status_intent)

        rail_pnr_status_intent = IntentBuilder("RailPnrStatusIntent").require("RailPnrStatusKeyword").require("PnrNumber").build()
        self.register_intent(rail_pnr_status_intent, self.handle_rail_pnr_status_intent)
        

	def rail_code(self, pname):
		url = "https://api.railwayapi.com/v2/suggest-station/name/" + pname + "/apikey/<YourAPiKey>/"
		response = requests.get(url).json()
		self.speak("source is" + pname)
		for i in response['stations']:
			self.speak("hey")
			self.speak("station name is "+ (i['name']))
			self.speak("hello")
			self.speak("station code is "+ (i['code']))		


        
    def handle_rail_code_intent(self, message):
    	pname = message.data.get("Pname")
	url = "https://api.railwayapi.com/v2/suggest-station/name/" + pname + "/apikey/<YourAPiKey>/"
	response = requests.get(url).json()
	for i in response['stations']:
		self.speak("station name is "+ (i['name']))
		self.speak("station code is "+ (i['code']))


    def handle_rail_travel_intent(self, message):
    	#self.speak("hi")
    	source = message.data.get("Source")
    	source = source.split(" ")[0] 
   	#self.speak("source is "+ source)
   	url = "https://api.railwayapi.com/v2/suggest-station/name/" + source + "/apikey/<YourAPiKey>/"
   	response = requests.get(url).json()
   	for i in response['stations']:
   		self.speak("station name is "+ (i['name']))
   		self.speak("station code is "+ (i['code']))
   	
    	

    	res = self.get_response('choose.source',num_retries=1)
    	#self.speak("response is "+res)



    	destination = message.data.get("Destination")
    	destination = destination.split(" ")[0] 
  	self.speak("destination is "+ destination)
   	url = "https://api.railwayapi.com/v2/suggest-station/name/" + destination + "/apikey/<YourAPiKey>/"
   	response = requests.get(url).json()
   	for i in response['stations']:
   		self.speak("station name is "+ (i['name']))
   		self.speak("station code is "+ (i['code']))
   	
    	res1 = self.get_response('choose.destination',num_retries=1)

    	date = message.data.get("Date")		
    	self.speak("Date is "+ date)
	url = "https://api.railwayapi.com/v2/between/source/"+res+"/dest/"+res1+"/date/"+date+"/apikey/ppipz4ugx<YourAPiKey>/"
	
	response = requests.get(url).json()
	#self.speak("hi")
	for i in response['trains']:
		self.speak("train number is "+ str(i['number']))
		self.speak("train name is "+ (i['name']))
		self.speak("train departure time from source is "+ str(i['src_departure_time']))
		self.speak("train arrival time for destination is "+ str(i['dest_arrival_time']))

    def handle_rail_train_status_intent(self, message):
    	train_number = message.data.get("TrainNumber")
    	date = message.data.get("Date")
	url = "https://api.railwayapi.com/v2/live/train/" + train_number> + "/date/" +date + "/apikey/<YourAPiKey>/"
	response = requests.get(url).json()
	self.speak("The current train position is "+response['position'])

    def handle_rail_pnr_status_intent(self, message):
    	pnr_number = message.data.get("PnrNumber")
	url = "https://api.railwayapi.com/v2/pnr-status/pnr/" + pnr_number + "/apikey/<YourAPiKey>/"
	response = requests.get(url).json()
	self.speak("Total passengers are "+str(response['total_passengers']))
	for i in response['passengers']:
		self.speak("Passenger Number " + str(i['no']))
		self.speak("Current Status is " + str(i['current_status']))
		self.speak("Booking Status was " + str(i['booking_status']))


    def stop(self):
        pass

def create_skill():
    return RailSkill()
