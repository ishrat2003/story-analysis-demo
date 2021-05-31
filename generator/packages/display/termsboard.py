class TermsBoard:
    
    def __init__(self, mainTopic, rcStory):
        self.mainTopic = mainTopic
        self.rcStory = rcStory
        self.board = {
            'main_topic': self.mainTopic
        }
        return

    def get(self):
        return self.board
    