from operator import attrgetter

class Note:
    def __init__(self, id, user_name, user_id, text, timestamp):
        self.id = id
        self.user_name = user_name
        self.user_id = user_id
        self.text = text
        self.timestamp = timestamp

def sort_notes(notes):
    result = sorted(notes, key = attrgetter("timestamp"), reverse = True)
    return result
