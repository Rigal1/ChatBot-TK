import os
import threading
import time

from backend.utils import json_manager

DOLLAR = 150

class ChatManager:
    def __init__(self, bot, voicevox_manager):
        self.bot = bot
        self.voicevox_manager = voicevox_manager
        self.messages = []
        self.prompt = ""
        self.prompt_parameters = {}
        self.prompt_list = {}
        self.all_costs = 0
        self.communication_count = 0
        self.before_message = ""
        self.max_memory = 10
        self.split_message = ["、", "。", "?", "!", "？", "！"]
        self.delete_memory()
    
    def set_prompt(self, data):
        for key in data.keys():
            if key == "mainPromptPath":
                # self.prompt_list = data[key]
                # self.prompt = self.prompt_list["Current"]
                self.prompt = self.load_text(data[key])
            else:
                self.prompt_parameters[key] = data[key]

    def set_message(self, message, role):
        self.messages.append({"role": role, "content": message})
    
    def delete_memory(self):
        self.messages = [{"role": "system", "content": self.prompt}]
    
    def call(self, message, voice_valid = True, is_stream = False):
        data = self.call_chatbot(message)
        if voice_valid:
            self.call_voicevox(data["reply"])
        return data
    
    def call_chatbot(self, message):
        self.set_message(message, "user")
        self.reflesh_memory()
        start = time.time()
        completion = self.bot.generate_reply_memory(self.messages)
        end = time.time()
        reply = completion.choices[0].message.content
        self.set_message(reply, "assistant")
        data = self.create_info(reply, self.estimate_emotion(message, reply), completion, end-start, self.is_conversation_end(message, reply))
        return data
    
    def estimate_emotion(self, message, reply):
        return "NEUTRAL"
        log = f"user: {message}\nbot: {reply}"
        emotion = self.bot.estimate_emotion(log)
        return emotion
    
    def is_conversation_end(self, message, reply):
        # return False
        log = f"bot: {reply}\nuser: {message}"
        is_conversation_end = self.bot.is_conversation_end_2(log)
        return is_conversation_end
    
    def call_stream(self, message):
        data = self.call_chatbot_stream(message)
        return data
    
    def call_chatbot_stream(self, message):
        self.set_message(message, "user")
        audio_split_count = 0
        message = ""
        audio_message = ""
        completion = self.bot.generate_reply_stream(message)
        for chunk in completion:
            chunk_message = chunk.choices[0].delta.content
            message += chunk_message
            audio_message += chunk_message
            if chunk_message in self.split_message:
                filename = f"data/sounds/tmp{audio_split_count}.wav"
                threading.Thread(target=self.voicevox_manager.call_voicevox, args=(audio_message, filename)).start()
                audio_split_count += 1
                audio_message = ""
        if audio_message != "":
            filename = f"data/sounds/tmp{audio_split_count}.wav"
            threading.Thread(target=self.voicevox_manager.call_voicevox, args=(audio_message, filename)).start()
        os.rename(f"data/sounds/tmp{audio_split_count}.wav", f"data/sounds/tmp99.wav")
        self.set_message(message, "assistant")
        return message
    
    def reflesh_memory(self):
        if len(self.messages) > (self.max_memory*2 + 1):
            self.messages = self.messages[0] + self.messages[2:]
    
    def call_voicevox(self, message, filename = "data/sounds/tmp.wav"):
        self.voicevox_manager.call_voicevox(message, filename)
    
    def communication_price(self, usage, mode):
        if mode == "gpt-4-1106-preview":
            input_price = 0.01*DOLLAR/1000
            output_price = 0.03*DOLLAR/1000
            return input_price*usage.prompt_tokens + output_price*usage.completion_tokens
        elif mode == "gpt-3.5-turbo-1106":
            input_price = 0.001*DOLLAR/1000
            output_price = 0.002*DOLLAR/1000
            return input_price*usage.prompt_tokens + output_price*usage.completion_tokens
        
    def create_info(self, reply, emotion, completion, response_time, is_conversation_end):
        price = self.communication_price(completion.usage, self.bot.get_model_name())
        self.all_costs += price

        return_dict = {"reply": reply,
                       "emotion": emotion,
                       "ResponseTime": f"{response_time:.4f} s",
                       "CurrentPrice": f"¥{price:.2f}",
                       "TotalPrice": f"¥{self.all_costs:.2f}",
                       "IsConversationEnd": str(is_conversation_end)
                       }
        return return_dict
    
    def load_text(self, path):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        return text

    def save_log(self, path):
        json_manager.save_json(self.messages, path)

    def load_log(self, path):
        self.messages = json_manager.load_json(path)
