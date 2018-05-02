import time
import requests
import json
from mtranslate import translate
from adapt.intent import IntentBuilder
from os.path import dirname
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'Nikita'
logger = getLogger(__name__)

class HoroscopeSkill(MycroftSkill):
    def __init__(self):
        super(HoroscopeSkill, self).__init__(name="HoroscopeSkill")

    def initialize(self):
        horoscope_intent = IntentBuilder("HoroscopeIntent") \
            .require("HoroscopeKeyword").require("Sunsign").build()
        self.register_intent(horoscope_intent,
                             self.handle_horoscope_intent)

    def handle_horoscope_intent(self, message):

        sunsign = message.data.get("Sunsign")
        response = requests.get("http://horoscope-api.herokuapp.com/horoscope/today/" + sunsign).json()
	
#--Hindi lines--
	new_response=response['horoscope']
	
	if (',' or ';' or '{' or '}' or '[' or ']' or '.' or '\"' or '\'') in new_response:
		new_response=new_response.replace(','," ")
		new_response=new_response.replace(';'," ")
		new_response=new_response.replace('{'," ")
		new_response=new_response.replace('}'," ")
		new_response=new_response.replace('['," ")
		new_response=new_response.replace(']'," ")
		new_response=new_response.replace('.',"\n")
		new_response=new_response.replace('\"'," ")
		new_response=new_response.replace('\''," ")

	new_text=translate(new_response,"hi")
	self.speak(new_text)
#--Hindi lines end--




    def stop(self):
        pass


def create_skill():
	return HoroscopeSkill()

