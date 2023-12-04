from middleware import parameter_input_handler

class FrameController():
    def __init__(self,
                 image_control_handler,
                 event_handler,
                 sound_handler,
                 chatbot_hundler
                 ):
        self.image_control_handler = image_control_handler
        self.event_handler = event_handler
        self.sound_handler = sound_handler
        self.chatbot_hundler = chatbot_hundler
        self.current_character = "chara"

    def call_chatbot(self, message):
        return self.chatbot_hundler.call_chatbot(message)
    
    def load_image(self, path):
        return self.image_control_handler.load_image(path)
    
    def load_resized_image(self, path, resize):
        return self.image_control_handler.load_resized_image(path, resize)
    
    def load_expression_image(self, emotion, resize):
        return self.image_control_handler.load_expression_image(emotion, resize)
    
    def save_log(self, path = "./data/log/log.json"):
        self.chatbot_hundler.save_log(path)
    
    def load_log(self):
        return self.event_handler.call_load_log_event()
    
    def clear_log(self):
        self.event_handler.call_clear_log_event()
    
    def update_parameter(self, data):
        self.chatbot_hundler.update_parameter(data)
    
    def save_parameter(self, data):
        path = f"./data/{self.current_character}/json/parameters.json"
        parameter_input_handler.save_parameter(data, path)
    
    def load_parameter(self):
        path = f"./data/{self.current_character}/json/parameters.json"
        params = parameter_input_handler.load_parameter(path)
        self.chatbot_hundler.update_parameter(params)
        self.chatbot_hundler.delete_memory()
        return params
    
    def play_sound(self, path="data/sounds/tmp.wav"):
        self.sound_handler.play_sound(path)
    
    def play_sound_all(self, path="data/sounds/tmp.wav"):
        self.sound_handler.play_sound_all(path)
    
    def set_current_character(self, character):
        self.current_character = character