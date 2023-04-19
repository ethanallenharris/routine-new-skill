from mycroft import MycroftSkill, intent_handler
from os.path import dirname, join
from mycroft.util.parse import extract_datetime, normalize
from mycroft.util.format import nice_time, nice_date
from mycroft.util.time import now_local
from mycroft.util import play_wav
from datetime import datetime, timedelta
import time
import re
import json


ROUTINE_PING = join(dirname(__file__), 'twoBeep.wav')

MINUTES = 60 #seconds




def getMilitaryTimeFromString(string):
    #Use regular expression pattern for the format "00:00"
    military_pattern = re.compile(r'^\d{2}:\d{2}$')

    #If time provided is already in military time format
    if military_pattern.match(string):
        return string

    #Searches for common time of day names    
    if "evening" in string:
        return "18:00"
    elif "midnight" in string:
        return "0:00"
    elif "night" in string:
        return "21:00"
    elif "dawn" in string:
        return "5:00"
    elif "midday" in string:
        return "12:00"
    else:
        #Use regular expression pattern for tdifferent time formats
        
        #Format "00:00 a.m." or "00:00 p.m."
        regular_time_pattern = re.compile(r'^(\d{1,2}):(\d{2})\s+(a\.m\.|p\.m\.)$')
        regular_time = regular_time_pattern.match(string)
        
        #Format "00 to 00"
        time_to_pattern = re.compile(r'^(\d{1,2})\s+to\s+(\d{1,2})$')
        time_to = time_to_pattern.match(string)
        
        #Format "00 past 00"
        time_past_pattern = re.compile(r'^(\d{1,2})\s+past\s+(\d{1,2})$')
        time_past = time_past_pattern.match(string)
        
        #Format "00"
        time_pattern = re.compile(r'^(\d{1,2})$')
        time = time_pattern.match(string)
        
        
        #If user input is in format "00:00 a.m." or "00:00 p.m."
        if regular_time:
            groups = regular_time.groups()
            hours = int(groups[0])
            minutes = int(groups[1])
            time_of_day = groups[2]

            if time_of_day == 'p.m.' and hours != 12:
                hours += 12
            elif time_of_day == 'a.m.' and hours == 12:
                hours = 0

            return '{:02d}:{:02d}'.format(hours, minutes)
        #If user input is in format "00 to 00"    
        elif time_to:
            groups = time_to.groups()
            hours = int(groups[1])
            minutes = int(groups[0])
            
            hours -= 1
            if hours < 0:
                hours = 0
            
            minutes = 60 - minutes
            return '{:02d}:{:02d}'.format(hours, minutes)
        #If user input is in format "00 to 00"  
        elif time_past:
            groups = time_past.groups()
            hours = int(groups[1])
            minutes = int(groups[0])
            return '{:02d}:{:02d}'.format(hours, minutes)
        #If user input is in format "00"  
        elif time:
            groups = time.groups()
            hours = int(groups[0])
            return '{:02d}:{:02d}'.format(hours, 0)
        else:
            return None






            
def getTimeFromString(string):
    #String should be in format of "00:00"
    
    #Split string into hour and minutes
    hour, minute = map(int, string.split(":"))
    #Get correct meridiam (am/pm)
    am_pm = 'a.m.' if hour < 12 else 'p.m.'
    #Hour should not exceed 12. (13 pm doesnt exist)
    hour = hour % 12
    if hour == 0:
        hour = 12
        
    if minute == 0:
        return f"{hour} {am_pm}"
    
    return f"{hour} {minute} {am_pm}"
    
     

    
                

def getDaysFromString(string):
    #Define a regular expression pattern for matching day names
    day_pattern = re.compile(r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b', re.IGNORECASE)

    #Find all matches of the day pattern in the input string
    matches = day_pattern.findall(string)

    #Format the list of matches as a comma-separated string of day names
    days_string = ', '.join(matches)
    
    if "weekend" in string:
        return "saturday and sunday"
    elif "weekdays" in string:
        return "monday, tuesday, wednesday, thursday and friday"
    return days_string           
        
        
        




class RoutineNew(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        
    def initialize(self):  
        #Creates repeating event to check for routine activity every 30 seconds  
        self.schedule_repeating_event(self.__check_routine, datetime.now(), 0.5 * MINUTES, name='routine')
        #If routine list doesn't exist yet instatiate it
        if 'routine' not in self.settings:
            self.settings['routine'] = [];
        
    def __check_routine(self, message):
        #Get current local datetime
        now = now_local()
        #Get the military time value from datetime
        military_time = now.strftime('%H:%M')
        #Get the day of week from datetime
        day_of_week = now.strftime('%A')
        #Checks routine activities time
        for r in self.settings.get('routine', []):
            #If routine activity matches current military time
            if military_time == r[1] and day_of_week.lower() in r[2]:
                #Play sound
                play_wav(ROUTINE_PING)
                self.speak_dialog('routine.activate', data={'activity': r[0]})
    
        
    #Intent to create a new routine activity    
    @intent_handler('routine.set.intent')
    def handle_routine_set(self, message):
        #Asks user to name routine activity
        #Add dialog
        activity = self.get_response('What would you like to call your routine activity?')
        
        #Loops until user provides a valid time for activity
        while True:
            try:
                #Asks user for time                       
                response = self.get_response('get_time', data={"activity": activity})
                #Function extracts a military time from user response 
                military_time = getMilitaryTimeFromString(response)
                #Function returns a more text to speech friendly time
                time = getTimeFromString(military_time)
                break
            except Exception as e:
                #Output 'time not recognised'
                self.speak_dialog('incorrect.time')
        
        #Loops until user proivdes a valid set of days for activity                                    
        while True:
            try:                  
                response = self.get_response('get_days', data={"activity": activity})
                days = getDaysFromString(response)
                break                   
            except Exception as e:
                #Output 'Induvidually list each day'
                self.speak_dialog('incorrect.days')
        
        
        try:        
            #Outputs the time and days routine activity is set for
            self.speak_dialog('routine.set', data={
                'activity': activity,
                'time': time,
                'days': days})
            
            #Will store data into a dictionary
            self.settings['routine'].append((activity, military_time, days))
        except:
            self.speak_dialog('')
            
        
    @intent_handler('time.change.intent')
    def handle_routine_change(self, message):
        #Get activity from intent
        activity = message.data.get('activity')
        
        #Variable 'found' will highlight if successfully found the activity in routine dictionary
        found = False
        
        #Loops through 'routine'
        for r in self.settings['routine']:
            if activity in r[0]:
                #If activity is found
                found = True
                #Ask if user they are sure they want to change the time for this activity
                answer = self.ask_yesno('confirm.change_time', data={'activity': activity})
                if answer == 'yes':
                    if 'routine' in self.settings:
                        while True:
                            try:
                                #Asks user for time                       
                                response = self.get_response('get_time', data={"activity": activity})
                                #Function extracts a military time from user response 
                                military_time = getMilitaryTimeFromString(response)
                                #Function returns a more text to speech friendly time
                                time = getTimeFromString(military_time)
                                r[1] = military_time   
                                self.speak_dialog('time.change', data={'activity': activity, 'time': time})
                                break
                            except Exception as e:
                                #Add dialog
                                self.speak_dialog('incorrect.time')
        else:  # Let user know that no routine was found under activity name
            if not found:
                self.speak_dialog('not_found.activity', data={'activity': activity})

        
                
            

    @intent_handler('day.change.intent')
    def handle_routine_day_change(self, message):
        # Get activity from intent
        activity = message.data.get('activity')
        
        #variable 'found' will highlight if successfully found the activity in routine
        found = False

        # Loop through routines to find the one with the specified activity
        for r in self.settings['routine']:
            if activity in r[0]:
                found = True
                # Ask user if they want to change the day of the routine
                answer = self.ask_yesno('confirm.change_day', data={'activity': activity})
                if answer == 'yes':
                    if 'routine' in self.settings:
                        while True:
                            try:
                                # Ask user for the new day(s) for the routine
                                response = self.get_response('get_days', data={"activity": activity})
                                days = getDaysFromString(response)
                                r[2] = days
                                self.speak_dialog('day.change', data={'activity': activity, 'days': days})
                                break
                            except:
                                self.speak_dialog('Please individually list each day')
        else:
            if not found:
                self.speak_dialog('not_found.activity', data={'activity': activity})
            
            
        
    
    @intent_handler('routine.remove.intent')
    def handle_routine_remove(self, message):
        # Get activity from intent
        activity = message.data.get('activity')

        # Loop through routines to find the one with the specified activity
        for r in self.settings['routine']:
            if activity in r[0]:
                # Ask user to confirm they want to remove the routine
                answer = self.ask_yesno('confirm.remove', data={'activity': activity})
                if answer == 'yes':
                    self.settings['routine'].remove(r)
                    self.speak_dialog('routine.removed', data={'activity': activity})
                else:
                    self.speak_dialog('routine.not_removed', data={'activity': activity})
                break
        else:
            self.speak_dialog('not_found.activity', data={'activity': activity})
    
    
        
    @intent_handler('routine.list.intent')
    def handle_routine_list(self, message):
        #Iterates through list of routine tasks
        for r in self.settings['routine']:
            #Individually output each activity in routine
            self.speak_dialog('routine.list', data={
            'routine': r[0],
            'time': getTimeFromString(r[1]),
            'days': r[2]})



    @intent_handler('web.delete.intent')
    def web_app_delete(self, message):
        routine = message.data.get('routine')
        for r in self.settings['routine']:
            if routine in r[0].lower():
                self.settings['routine'].remove(r)
                
    
    @intent_handler('web.edit.intent')
    def web_app_edit(self, message):
        routine = message.data.get('name')
        for r in self.settings['routine']:
            if routine in r[0].lower():
                routine_time = message.data.get('time')
                routine_days = message.data.get('days')
                # Apply changes
                r[1] = routine_time
                r[2] = routine_days
                
    @intent_handler('web.new.intent')
    def web_app_edit(self, message):
        routine = message.data.get('name')
        routine_time = message.data.get('time')
        routine_days = message.data.get('days')
        self.settings['routine'].append((routine, routine_time, routine_days))
        

    
    @intent_handler('nuke.intent')
    def remove_all(self, message):
        for r in self.settings['routine']:
            self.settings['routine'].remove(r)
        self.speak_dialog("routine has been reset")
                
        

def create_skill():
    return RoutineNew()
