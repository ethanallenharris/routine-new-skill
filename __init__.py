from mycroft import MycroftSkill, intent_file_handler


class RoutineNew(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

        @intent_handler('goodmorning.set.intent')
        def handle_goodmorning_set(self, message):
            #Needs to set goodmorning routine here

            #Says to user "ok I will say goodmorning everyday at 9am"
            self.speak_dialog('goodmorning.set')


        @intent_handler('routine.set.intent')
        def handle_routine_set(self, message):
            #Needs to set routine here

            #Check if user gave a routine
            routine = message.data.get('routine')


            #appends to list of routines

            self.settings['routine.tasks'].append((routine, '9 AM', 'everyday'))


            #Says to user "alright I have created a routine for x at time everyday"
            self.speak_dialog('routine.set', data={
            'routine': routine,
            'time': '9 AM',
            'days': 'everyday'})



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
