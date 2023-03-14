from mycroft import MycroftSkill, intent_handler
from mycroft.util.parse import extract_datetime, normalize
from mycroft.util.format import nice_time, nice_date
import time
import re



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

    @intent_handler('goodmorning.set.intent')
    def handle_goodnight_goodmorning(self, message):
        self.speak_dialog('goodmorning.set')
        
        
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
            time = "12:00 am"
            #say to user "I have created activity for 9 AM everyday"
            self.speak_dialog('routine.set', data={
            'routine': activity,
            'time': time,
            'days': 'everyday'})
            
            
            #expect yes/no response
            #NEED DIALOG FILE
            if self.ask_yesno('would you like to change the time set for ' + activity) == 'yes':
                #if user wants to change time/date of routine                
                loop = True
                                
                #Ask what time the user would like for this activity
                #NEED DIALOG FILE 
                response = self.speak_dialog('What time do you want for ' + activity) 
                                    
                #Loop until user gives a valid time                
                while loop:
                    try:    
                        #Loops until valid response given
                        while not response:
                            #while no response given, wait until response
                            response = self.get_response() 

                        #Ask what time the user would like for this activity
                        #NEED DIALOG FILE 
                        #response = self.get_response('What time do you want for ' + activity)                   
                        military_time = getMilitaryTimeFromString(response)
                        self.speak_dialog(military_time)
                        time = getTimeFromString(military_time)
                        loop = False         
                   
                    except Exception as e:
                        response = None
                        self.speak_dialog('Please rephrase your time in the example format of 9 20 am')
                        response = self.get_response('What time do you want for ' + activity) 
                                
                
            self.speak_dialog("okay " + activity + " has been set for " + time + " everyday")
            
            
            
                
                  
            #Then ask what days the user would like for this activity
            
            #if invalid answer say "Activity has been set for 12 am, are you happy with this?"
            #yesno
            
            #if 'no' loop, and ask user for what days they would like
            
            #if 'yes' go to days
            
            days = "everyday"
            
            #expect yes/no response
            #NEED DIALOG FILE
            if self.ask_yesno('would you like to change the dates for ' + activity) == 'yes':
                #if user wants to change time/date of routine                
                response = None
                                
                #Ask what time the user would like for this activity
                #NEED DIALOG FILE 
                response = self.get_response('What days do you want for ' + activity) 
                                    
                #Loop until user gives a valid time                
                while loop:
                    try:    
                        #Loops until valid response given
                        while not response:
                            #while no response given, wait until response
                            response = self.get_response() 
                            loop = True

                        #Ask what time the user would like for this activity
                        #NEED DIALOG FILE 
                        #response = self.get_response('What time do you want for ' + activity)                   
                        days = getDaysFromString(response)
                        loop = False         
                   
                    except Exception as e:
                        response = None
                        self.speak_dialog('Please rephrase and individually list each ')
                        response = self.get_response('What days do you want for ' + activity) 
                                
            
            
            #Outputs the time and days routine is set for
            self.speak_dialog("okay " + activity + " has been set for " + time + " on " + days)
            
            #--------------------------------------------------------------------------------
            
            #set routine
            
            #say "alright I have created a routine for x at time everyday"
            
           
           
           
            
        #Says to user "alright I have created a routine for x at time everyday"
        #self.speak_dialog('routine.set', data={'routine': activity,'time': '9 AM','days': 'everyday'})
        
        
        
        #empties directory
        #self.settings['routine'] = [];
        
        #if user is cool with default time
        
        #will store data into a directory
        #self.settings['routine'].append((activity, military_time, days))
        
        

        
        
    @intent_handler('routine.change.intent')
    def handle_routine_change(self, message):
        #Logic here

        #Says to user "Ok I have changed your routine to be at X time on X days"
        self.speak_dialog('routine.change')
        
        
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
