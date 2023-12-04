class MessageInputHandler:
    def __init__(self, chat_manager):
        self.chat_manager = chat_manager
    
    def call_chatbot(self, message):
        return self.chat_manager.call(message)
    
    def call_chatbot_no_voicevox(self, message):
        return self.chat_manager.call_chatbot(message)

    def save_log(self):
        self.bot.save_log()