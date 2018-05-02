# Import statements: the list of outside modules you'll be using in your
# skills, whether from other files in mycroft-core or from external libraries
import time
import requests

from mtranslate import translate 
from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'Nikita'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)

# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class ZomatoFoodSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(ZomatoFoodSkill, self).__init__(name="ZomatoFoodSkill")

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        self.load_data_files(dirname(__file__))

        '''zomato_category_intent = IntentBuilder("ZomatoCategoryIntent").require("ZomatoCategoryKeyword").build()
        self.register_intent(zomato_category_intent, self.handle_zomato_category_intent)'''
        
        zomato_cuisine_intent = IntentBuilder("ZomatoCuisineIntent").require("ZomatoCuisineKeyword").build()
        self.register_intent(zomato_cuisine_intent, self.handle_zomato_cuisine_intent)

        '''zomato_cityid_intent = IntentBuilder("ZomatoCityIdIntent").require("ZomatoCityIdKeyword").build()
        self.register_intent(zomato_cityid_intent, self.handle_zomato_cityid_intent)'''
        
        zomato_search_intent = IntentBuilder("ZomatoSearchIntent").require("ZomatoSearchKeyword").require("Keyword").build()
        self.register_intent(zomato_search_intent, self.handle_zomato_search_intent)

    # The "handle_xxxx_intent" functions define Mycroft's behavior when
    # each of the skill's intents is triggered: in this case, he simply
    # speaks a response. Note that the "speak_dialog" method doesn't
    # actually speak the text it's passed--instead, that text is the filename
    # of a file in the dialog folder, and Mycroft speaks its contents when
    # the method is called.
    '''def handle_zomato_category_intent(self, message):
    	location = self.get_location(message)
    	self.speak("location recieved"+ str(location))
	headers = {'Accept': "application/json",'user-key': "44aaaa8c97eab3c1057ba3f6472bee05"}
	url = "https://developers.zomato.com/api/v2.1/categories"
	response = requests.get(url, headers=headers).json()
	for i in response['categories']:
		self.speak("category is "+ (i['categories']['name']))		
		
    def handle_zomato_cityid_intent(self, message):
    	#location = self.get_location(message)
    	#self.speak("location recieved"+ str(location))
	headers = {'Accept': "application/json",'user-key': "44aaaa8c97eab3c1057ba3f6472bee05"}
	url = "https://developers.zomato.com/api/v2.1/cities?q=pune"
	response = requests.get(url, headers=headers).json()
	for i in response['location_suggestions']:
		self.speak("cityid is "+ str(i['id']))'''
		
    def handle_zomato_cuisine_intent(self, message):
    	location = self.get_location(message)
    	self.speak("sthaan praapt hua "+ str(location))
	headers = {'Accept': "application/json",'user-key': "44aaaa8c97eab3c1057ba3f6472bee05"}
	url = "https://developers.zomato.com/api/v2.1/cuisines?city_id=5"
	response = requests.get(url, headers=headers).json()
	for i in response['cuisines']:
		new_cuisine=translate(i['cuisine']['cuisine_name'],"hi")
		self.speak("aapke shahar ke liye upalabdh bhojan hai "+ new_cuisine)
		
    def handle_zomato_search_intent(self, message):
    	keyword = message.data.get("Keyword")
    	search_word = keyword.split(" ")
    	length = len(search_word)
	string = ""
    	if length > 1:
		#self.speak("length is "+str(length))   
    		for l in range(0,length):
			#self.speak("hi")  
			if l == 0:
				string = search_word[l]
			else:
				string=string+"%20"+search_word[l]
		#self.speak("string is "+ string)
	else:
		string=keyword   	
    	#location = self.get_location(message)    	
    	#self.speak("location recieved"+ str(location))
	headers = {'Accept': "application/json",'user-key': "44aaaa8c97eab3c1057ba3f6472bee05"}
	url = "https://developers.zomato.com/api/v2.1/search?entity_id=5&entity_type=city&count=3&q="+string
	url_review = "https://developers.zomato.com/api/v2.1/reviews?res_id="
	response = requests.get(url, headers=headers).json()
	for i in response['restaurants']:
		id = i['restaurant']['id']
		
		name=translate(i['restaurant']['name'],"hi")
		address=translate(i['restaurant']['location']['address'],"hi")
		cuisines=translate(i['restaurant']['cuisines'],"hi")
		avg_cost=translate(str(i['restaurant']['average_cost_for_two']),"hi")
		#self.speak(avg_cost)
		avg_rat=translate(str(i['restaurant']['user_rating']['aggregate_rating']),"hi")
		
		#self.speak("naam hai")
		self.speak((translate("name is","hi"))+ name)
		self.speak((translate("address is","hi"))+ address)
		#self.speak("upalabdh vyanjan hain "+ cuisines)
		self.speak(translate("average cost for two is ","hi"))
		self.speak(avg_cost)	
		self.speak((translate("average rating is","hi")))
		self.speak(avg_rat)

		self.speak(translate("The latest five reviews are as follows: ","hi"))
		url_review = "https://developers.zomato.com/api/v2.1/reviews?res_id=" + str(id)
		responses = requests.get(url_review, headers=headers).json()
		for j in responses['user_reviews']:
			self.speak((translate("response is ","hi"))+ (translate(j['review']['review_text'],"hi")))
    	
    def get_location(self,message):
    	location = self.location_pretty
	return location
	'''
    	if type(location) is dict:		
    		return location['city']['name']'''
    	
#response = curl -X GET --header "Accept: application/json" --header "user-key: 44aaaa8c97eab3c1057ba3f6472bee05" "https://developers.zomato.com/api/v2.1/categories"
#for i in response['categories']:#self.speak_dialog("zomato.category",data=response['name'])


    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, the method just contains the keyword "pass", which
    # does nothing.
    def stop(self):
        pass

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return ZomatoFoodSkill()
