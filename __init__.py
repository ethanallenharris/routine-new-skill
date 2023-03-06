from mycroft import MycroftSkill, intent_file_handler


class RoutineNew(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('new.routine.intent')
    def handle_new_routine(self, message):
        routine = message.data.get('routine')

        self.speak_dialog('new.routine', data={
            'routine': routine
        })


def create_skill():
    return RoutineNew()

