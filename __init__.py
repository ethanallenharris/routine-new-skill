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
        time_pattern = re.compile(r'(\d{1,2})\s+(\d{2})\s+(am|pm)')
        #match = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)', string)
        match = time_pattern.search(string)
        
        time_pattern2 = re.compile(r'(\d{1,2}):(\d{2})\s*(am|pm)')
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
            
            
            
        if match2:
            hour = int(match2.group(1))
            meridiem = match2.group(2)
            
            hour = hour % 12
            
            return hour + ":00"
            
            
            
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
        self.schedule_repeating_event(self.__check_routine, datetime.now(), 0.5 * MINUTES, name='routine')

        
    def __check_routine(self, message):
        #Get current local datetime
        now = now_local()
        #Get the military time value from datetime
        military_time = now.strftime('%H:%M')
        #Checks routine activities time
        for r in self.settings.get('routine', []):
            #If routine activity matches current military time
            if military_time == r[1]:
                #Play sound
                play_wav(ROUTINE_PING)
                self.speak_dialog('routine.activate', data={'activity': r[0]})
    
        
    @intent_handler('routine.set.intent')
    def handle_routine_set(self, message):
        #Needs to set routine here

        #Check if user gave a routine activity
        activity = message.data.get('routine')


        #appends to list of routines

        #has set routine
        
        #maybe ask user if they are sure they want to add that to their routine
        
        
        
        
        #SAMPLE CONVERSATION
        
        #"can you add a routine {routine}"
        
        #"sure, I can add {routine} for 9 AM everyday"
        
        #"would you like to change the date or time of this routine, respond with 'yes' or 'no'"
        #**Listens**
        
        #"yes"
        
        #"alright what time or day would you like for this activity to be in your routine?"
        #(maybe give the user a sample response)
        
        #"nine thirty, monday and thursday"
        
        #**will disect response and re-arrange routine time/days**
        
        
        #see if user can add a time or date to routine
        
        
        
        
        #User calls intent
        
        #Check user actually has an activity
        
        #If no, say "please provide an activity to your routine"
        #End
        
        
        #if user has an activity
        #output dialog
        #then ask if user would like to change date / time
        
        if activity == "":
            #No routine activity supplied
            #NEED DIALOG FILE
            self.speak_dialog('Please supply an activity for your routine')
            
        else:
            #If user did supply activity
            time = "12 am"
            military_time = "12:00"
            days = "everyday"
            #say to user "I have created activity for 9 AM everyday"
            self.speak_dialog('routine.set', data={
            'routine': activity,
            'time': time,
            'days': days})
            
            
            #expect yes/no response
            #NEED DIALOG FILE
            if self.ask_yesno('would you like to change the time set for ' + activity) == 'yes':
                #if user wants to change time/date of routine                
                                
                #Ask what time the user would like for this activity
                #NEED DIALOG FILE 
                #response = self.speak_dialog('What time do you want for ' + activity)
                                    
                #Loop until user gives a valid time                
                try:                       
                    response = self.get_response('get_time', data={"activity": activity}) 
                    military_time = getMilitaryTimeFromString(response)
                    time = getTimeFromString(military_time)
                    #self.speak_dialog('confirm_time', data={"activity": activity, "time": time})
                   

                    #Ask what time the user would like for this activity
                    #NEED DIALOG FILE 
                    #response = self.get_response('What time do you want for ' + activity)                   
                    #military_time = getMilitaryTimeFromString(response)
                    #self.speak_dialog(military_time)
                    #time = getTimeFromString(military_time)       
               
                except Exception as e:
                    response = None
                    self.speak_dialog('Please phrase your time in the example format of 9 20 am')
                    #response = self.get_response('What time do you want for ' + activity) 
                                
                
            self.speak_dialog("okay " + activity + " has been set for " + time + " everyday")
            
            
            
                
                  
            #Then ask what days the user would like for this activity
            
            #if invalid answer say "Activity has been set for 12 am, are you happy with this?"
            #yesno
            
            #if 'no' loop, and ask user for what days they would like
            
            #if 'yes' go to days
            

            
            #expect yes/no response
            #NEED DIALOG FILE
            if self.ask_yesno('would you like to change the dates for ' + activity) == 'yes':
                #if user wants to change time/date of routine                          
                #Ask what time the user would like for this activity
                #NEED DIALOG FILE 
                try:    
                    #response = self.get_response('What days do you want for ' + activity)                
                    response = self.get_response('get_days', data={"activity": activity})
                    days = getDaysFromString(response)
                    #self.speak_dialog('confirm_days', data={"activity": activity, "days": days})                    
                except Exception as e:
                    self.speak_dialog('Please individually list each day')
                    days = "everyday"             
                
                                
            
            #Outputs the time and days routine is set for
            self.speak_dialog("okay " + activity + " has been set for " + time + " on " + days)
            
            #--------------------------------------------------------------------------------
            
            #set routine
            
            #say "alright I have created a routine for x at time everyday"
            
           
           
           
            
        #Says to user "alright I have created a routine for x at time everyday"
        #self.speak_dialog('routine.set', data={'routine': activity,'time': '9 AM','days': 'everyday'})
        
        
        
        #empties directory
        self.settings['routine'] = [];
        
        #if user is cool with default time
        
        #will store data into a directory
        self.settings['routine'].append((activity, military_time, days))
        
        

        
        
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

        self.settings['routine.tasks'] = [("Go shopping", "12 AM", "Monday, Thursday")]

        #Iterates through list of routine tasks
        for r in self.settings['routine.tasks']:
            #Says to user "alright I have created a routine for x at time everyday"
            self.speak_dialog('routine.list', data={
            'routine': r[0],
            'time': r[1],
            'days': r[2]})


def create_skill():
    return RoutineNew()
