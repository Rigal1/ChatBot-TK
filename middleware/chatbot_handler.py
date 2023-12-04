class ChatbotHandler:
    def __init__(self, chatbot_manager):
        self.chatbot_manager = chatbot_manager

    def call_chatbot(self, message):
        return self.chatbot_manager.call(message)
    
    def call_chatbot_no_voicevox(self, message):
        return self.chatbot_manager.call_chatbot(message)
    
    def call_chatbot_stream(self, message):
        return self.chatbot_manager.call_stream(message)

    def save_log(self):
        self.chatbot_manager.save_log()
    
    def load_log(self):
        self.chatbot_manager.load_log()
    
    def update_parameter(self, data):
        self.chatbot_manager.set_prompt(data)
    
    def delete_memory(self):
        self.chatbot_manager.delete_memory()