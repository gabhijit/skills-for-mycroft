import time
import requests
import os

from adapt.intent import IntentBuilder
from os.path import dirname
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'Nikita'
logger = getLogger(__name__)

class Take_NotesSkill(MycroftSkill):
    def __init__(self):
        super(Take_NotesSkill, self).__init__(name="Take_NotesSkill")
        self.topic_name = None
        self.taking_notes = False
        self.notes = ""
        self.path = os.path.dirname(__file__) + "/notes"
        self.path1 = ""
        if not os.path.exists(self.path):
            os.makedirs(self.path)	

    def initialize(self):
        take_notes_intent = IntentBuilder("NotesIntent").require("NotesKeyword").optionally("Topicname").build()
        self.register_intent(take_notes_intent,self.handle_take_notes_intent)
		
        stop_notes_intent = IntentBuilder("StopNotesIntent").require("StopNotesKeyword").require("Topicname").build()
        self.register_intent(stop_notes_intent,self.handle_stop_notes_intent)

        read_notes_intent = IntentBuilder("ReadNotesIntent").require("ReadNotesKeyword").require("Topicname").build()
        self.register_intent(read_notes_intent,self.handle_read_notes_intent)

    def handle_take_notes_intent(self, message):
        name = message.data.get("Topicname")
        #utt = message.metadata['utterance']
        #self.speak("utt is "+ utt[0])
        if not name:
            self.topic_name = time.asctime()
        else:
		self.topic_name = name
        
       	file_object = open(self.topic_name,"w")
       	#self.speak("hi")
       	if (self.taking_notes==False):
       		self.notes = ""
	       	self.taking_notes = True
       		self.speak("Taking notes on "+ self.topic_name)
	       	self.notes = self.get_response("taking.notes", num_retries=1)
	       	self.path1 = self.path + "/" + self.topic_name + ".txt"
	       	#with open(self.path1, "w") as f:
		#	f.write(self.notes)

    def handle_stop_notes_intent(self, message):    
       	if (self.taking_notes==True):
		#path = self.path + "/" + self.topic_name + ".txt"
		#with open(path, "w") as f:
		#	f.write(self.notes)
		#self.speak("Saving notes")	
		self.taking_notes = False
		self.speak("Stopped taking notes")
		self.speak("notes taken are" + self.notes)
       	if (self.taking_notes==False):
		self.speak("I am not taking any notes at present")		       	
       	self.notes = ""			
			
    def handle_read_notes_intent(self, message):
        name = message.data.get("Topicname")
        path = self.path+"/"+name+".txt"
        with open(path, "r") as f:
		self.speak(f.read())	        	    			


    def converse(self, utterance, lang):
        if self.taking_notes:
        	if "end note" in utterance:
        		self.taking_notes = False
        	else:
        		self.speak("", expect_response=True)
        		self.notes.append(utterance[0])
        		#with open(self.path1, "w") as f:
        		#	f.write(self.notes)
        	return True 
        else : 
        	return False


        
    def stop(self):
       	pass

def create_skill():
	return Take_NotesSkill()

