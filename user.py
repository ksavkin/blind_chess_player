class User:
    chat_id = ""

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def __hash__(self):
        return hash(self.chat_id)

    def __eq__(self, user):
        return self.chat_id == user.chat_id