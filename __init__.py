from mycroft import MycroftSkill, intent_handler
from os.path import dirname, join
from mycroft.util.parse import extract_datetime, normalize
from mycroft.util.format import nice_time, nice_date
from mycroft.util.time import now_local
from mycroft.util import play_wav
from datetime import datetime, timedelta
import time
import re


ROUTINE_PING = join(dirname(__file__), 'twoBeep.wav')

MINUTES = 60 #seconds


def getMilitaryTimeFromString(string):
    if "evening" in string:
        return "18:00"
    elif "night" in string:
        return "21:00"
    elif "dawn" in string:
        return "5:00"
    elif "midday" in string:
        return "12:00"
    elif "midnight" in string:
        return "0:00"
    else:
        # Use regular expressions to extract the time
        time_pattern = re.compile(r'(\d{1,2})\s+(\d{2})\s+(am|pm)', re.IGNORECASE)
        match = time_pattern.search(string)
        
        time_pattern2 = re.compile(r'(\d{1,2})\s*(am|pm)', re.IGNORECASE)
        match2 = time_pattern2.search(string)
        
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            meridiem = match.group(3)
            
            
            # Convert to 24-hour format
            if meridiem:
                if meridiem.lower() == 'pm' and hour != 12:
                    hour += 12
                elif meridiem.lower() == 'am' and hour == 12:
                    hour = 0

            #Format the time as a string and return
            return str(f'{hour:02}:{minute}')
            
        elif match2:
            hour = int(match2.group(1))
            meridiem = match2.group(2)
            
            hour = hour % 12
            
            if meridiem:
                if meridiem.lower() == 'pm' and hour != 12:
                    hour += 12
                elif meridiem.lower() == 'am' and hour == 12:
                    hour = 0
            
            return str(f'{hour:02}:00')
            
            
            
def getTimeFromString(string):
    #string should be in format of "00:00"
    hour, minute = map(int, string.split(":"))
    am_pm = 'am' if hour < 12 else 'pm'
    hour = hour % 12
    if hour == 0:
        hour = 12
        
    if minute == 0:
        return f"{hour} {am_pm}"
    
    return f"{hour} {minute} {am_pm}"
    
     

    
                

def getDaysFromString(string):
    # Define a regular expression pattern for matching day names
    day_pattern = re.compile(r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b', re.IGNORECASE)

    # Find all matches of the day pattern in the input string
    matches = day_pattern.findall(string)

    # Format the list of matches as a comma-separated string of day names
    days_string = ', '.join(matches)

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
            if military_time == r[1] and day_of_week.lower in r[2]:
                #Play sound
                play_wav(ROUTINE_PING)
                self.speak_dialog('routine.activate', data={'activity': r[0]})
    
        
    @intent_handler('test_set_time.intent')
    def handle_set_time(self, message):  
        try:
            response = self.get_response('give me time') 
            military_time = getMilitaryTimeFromString(response)
            time = getTimeFromString(military_time)
            self.speak_dialog(time)
        except:
            self.speak_dialog('Error occured in set time')
        
        
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
                #Add dialog
                self.speak_dialog('Sorry but I could not recognise the time provided.')
        
        #Loops until user proivdes a valid set of days for activity                                    
        while True:
            try:                  
                response = self.get_response('get_days', data={"activity": activity})
                days = getDaysFromString(response)
                break                   
            except Exception as e:
                #Add dialog
                self.speak_dialog('Please individually list each day')
        
        
        try:        
            #Outputs the time and days routine is set for
            self.speak_dialog("okay " + activity + " has been set for " + time + " on " + days)
            
            #Will store data into a dictionary
            self.settings['routine'].append((activity, military_time, days))
        except:
            self.speak_dialog('Please individually list each day')
            
        
        
    @intent_handler('time.change.intent')
    def handle_routine_change(self, message):
        #Logic here
        #Needs to get activity from intent
        
        activity = message.data.get('activity')
        loop = True
        
        #Loops through 'routine'
        
        #checks to see if any routines are being stored
        for r in self.settings['routine']:
            if activity in r[0]:
                answer = self.ask_yesno('confirm.change_time', data={'activity': activity})
                if answer == 'yes':
                    if 'routine' in self.settings:
                        while loop:
                            try:
                                response = self.get_response('get_time', data={"activity": activity}) 
                                military_time = getMilitaryTimeFromString(response)
                                time = getTimeFromString(military_time)
                                r[1] = military_time   
                                self.speak_dialog(activity + ' has been set for ' + time)
                                loop = False
                            except:
                                self.speak_dialog('Please phrase your time in the example format of 9 20 am')
                break
        else:  # Let user know that no routine was found under activity name
            self.speak_dialog('not_found.activity', data={'activity': activity})

        
                
            

    @intent_handler('day.change.intent')
    def handle_routine_change(self, message):
        # Get activity from intent
        activity = message.data.get('activity')
        loop = True

        # Loop through routines to find the one with the specified activity
        for r in self.settings['routine']:
            if activity in r[0]:
                # Ask user if they want to change the day of the routine
                answer = self.ask_yesno('confirm.change_day', data={'activity': activity})
                if answer == 'yes':
                    if 'routine' in self.settings:
                        while loop:
                            try:
                                # Ask user for the new day(s) for the routine
                                response = self.get_response('get_days', data={"activity": activity})
                                days = getDaysFromString(response)
                                r[2] = days
                                self.speak_dialog(activity + ' has been set for ' + days)
                                loop = False
                            except:
                                self.speak_dialog('Please individually list each day')
                break
        else:
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
        #Needs to get routine list here

        #self.settings['routine.tasks'] = [("Go shopping", "12 AM", "Monday, Thursday")]

        #Iterates through list of routine tasks
        for r in self.settings['routine']:
            #Says to user "alright I have created a routine for x at time everyday"
            self.speak_dialog('routine.list', data={
            'routine': r[0],
            'time': getTimeFromString(r[1]),
            'days': r[2]})


def create_skill():
    return RoutineNew()
