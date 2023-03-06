from mycroft import MycroftSkill, intent_handler
from mycroft.util.parse import extract_datetime, normalize
from mycroft.util.format import nice_time, nice_date


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
            
            #say to user "I have created activity for 9 AM everyday"
            self.speak_dialog('routine.set', data={
            'routine': activity,
            'time': '12 AM',
            'days': 'everyday'})
            
            
            #expect yes/no response
            #NEED DIALOG FILE
            if self.ask_yesno('would you like to change the date or for ' + activity) == 'yes':
                #if user wants to change time/date of routine
                
                #Ask what time the user would like for this activity
                #NEED DIALOG FILE
                response = self.get_response('What time do you want for ' + activity)
                
                reminder_time, rest = (extract_datetime(response, now_local(), self.lang, default_time=DEFAULT_TIME) or (None, None))
                
                self.speak_dialog(reminder_time)
                
                                                                                    
                #response
                
                #handle "twelve thirty pm" and convert into time
                
                
                
                
                
                

                #if invalid answer say "Activity has been set for 12 AM, are you happy with this?"
                #yes/no
                
                
                
                #if no loop, and ask user for what time they would like
                
                
                #-------------------------------------------------------------------------------
                
                #Ask what days the user would like for this activity
                
                
                
                
                
                #if invalid answer say "Activity has been set for 12 AM, are you happy with this?"
                #yesno
                
                #if 'no' loop, and ask user for what days they would like
                
                #if 'yes' go to days
                #--------------------------------------------------------------------------------
                
                #set routine
                
                #say "alright I have created a routine for x at time everyday"
                
                
                
                
            
            
           
           
           
            
        #Says to user "alright I have created a routine for x at time everyday"
        #self.speak_dialog('routine.set', data={'routine': activity,'time': '9 AM','days': 'everyday'})
        
        
        
        #empties directory
        self.settings['routine'] = [];
        
        #if user is cool with default time
        
        #will store data into a directory
        self.settings['routine'].append((activity, '12 AM', 'everyday'))
        
        

        
        
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
