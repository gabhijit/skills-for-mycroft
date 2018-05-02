import time
import requests
import datetime
import urllib
from pycricbuzz import Cricbuzz
from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'Nikita'

LOGGER = getLogger(__name__)

class CricketSkill(MycroftSkill):


    def __init__(self):
        super(CricketSkill, self).__init__(name="CricketSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))

        cricket_intent = IntentBuilder("CricketIntent").require("CricketKeyword").build()

         
        self.register_intent(cricket_intent, self.handle_cricket_intent)
        

    def handle_cricket_intent(self, message):
    	#self.speak("hello")
    	c = Cricbuzz()
    	matches = c.matches()
    	for match in matches:
    		self.speak("match is " + match['mchdesc'])
    		self.speak("match status is " +match['status'])

   
    def stop(self):
        pass

def create_skill():
    return CricketSkill()

