import time
import requests
from adapt.intent import IntentBuilder
from mtranslate import translate
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
        yes = 0
        string = ""
        sunsign = message.data.get("Sunsign")
        response = requests.get("http://horoscope-api.herokuapp.com/horoscope/today/" + sunsign).json()
        self.speak_dialog("sunsign.horoscope", data=response)
        time.sleep(35)
        res = self.get_response("more.horoscope", num_retries=1)
        self.speak("The response is " +res)
        data = res.split(" ")
        length = len(data) 
        self.speak("length is "+str(length))  
        for i in range (0, length):
        	if(data[i]=="yes"):
        		yes=yes+1
        		self.speak("yes count is "+str(yes))
        		#continue
        	elif (data[i] == "week" or data[i]=="month" or data[i] == "year"):
        		string=data[i]
        		self.speak("string is "+ string)
        		break
        	else:
        		#self.speak("You didn't confirm if you want to know anything further!")
        		continue
			
        if (yes!=0 or string!=""):
        	respp = requests.get("http://horoscope-api.herokuapp.com/horoscope/"+string+"/" + sunsign).json()	
        	self.speak("hi")
        	dialogg = string + ".horoscope"
        	self.speak_dialog(dialogg, data=respp)
        else :
        	self.speak("You didn't confirm if you want to know anything further!")


    def stop(self):
        pass


def create_skill():
	return HoroscopeSkill()

