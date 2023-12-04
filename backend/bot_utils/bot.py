import json
from openai import OpenAI

from backend.bot_utils import funclist
from backend.utils import load_env

DOLLAR = 150

def estimate_emotion(emotion):
    response = {
        "emotion":emotion,
    }
    return json.dumps(response)

def is_conversation_end(result):
    response = {
        "result":result,
    }
    return json.dumps(response)

class Bot:
    def __init__(self, mode="official") -> None:
        api_dict = load_env.load_env(".env")
        self.api = api_dict["OPENAI_API_KEY_OFFICIAL"] if mode == "official" else api_dict["OPENAI_API_KEY_PRIVATE"]
        print(self.api)
        self.model_name = "gpt-3.5-turbo-1106"
        self.is_conversation_end_model_name = "gpt-3.5-turbo-0613:aimy::8HnA0bU0" if mode == "official" else "gpt-4-1106-preview"
        self.client = OpenAI(api_key=self.api)
    
    def estimate_emotion(self, text):
        system_prompt = "Estimate the emotion of the following text."
        functions = funclist.estimate_emotion()
        completion = self.client.chat.completions.create(
            model = self.model_name,
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature = 1.0,
            tools = functions,
            tool_choice = {"type": "function", "function": {"name": "estimate_emotion"}},
        )
        tool_calls = json.loads(completion.choices[0].message.tool_calls[0].function.arguments)
        emotion = tool_calls["emotion"]
        return emotion
    
    def is_conversation_end(self, log):
        system_prompt = "Has this topic reached a natural endpoint for moving to another?"
        functions = funclist.is_conversation_end()
        completion = self.client.chat.completions.create(
            model = self.is_conversation_end_model_name,
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": log}
            ],
            temperature = 1.0,
            tools = functions,
            tool_choice = {"type": "function", "function": {"name": "is_conversation_end"}},
        )
        tool_calls = json.loads(completion.choices[0].message.tool_calls[0].function.arguments)
        is_conversation_end = tool_calls["is_conversation_end"]
        return is_conversation_end

    def is_conversation_end_2(self, log):
        system_prompt = "Has this topic reached a natural endpoint for moving to another?"
        completion = self.client.chat.completions.create(
            model = self.is_conversation_end_model_name,
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": log}
            ],
            temperature = 1.0,
        )
        is_conversation_end = completion.choices[0].message.content
        return is_conversation_end


    def generate_reply_memory(self, messages):
        completion = self.client.chat.completions.create(
            model = self.model_name,
            messages = messages,
            temperature = 1.0,
        )
        return completion
    
    def generate_reply_stream(self, messages):
        completion = self.client.chat.completions.create(
            model = self.model_name,
            messages = messages,
            temperature = 1.0,
            stream=True,
        )
        return completion
    
    def dammy_reply(self):
        return_dammy_dict = {"reply": "dammy", "emotion": "dammy", "ResponseTime": "dammy", "CurrentPrice": "dammy", "TotalPrice": "dammy", "IsConversationEnd": "dammy"}
        return return_dammy_dict

    def get_model_name(self):
        return self.model_name