import requests
import json
import time

class VoiceVoxManager:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 50021
        self.speaker_id = 8
        self.max_retry = 10
    
    def create_query(self, text, speaker_id=None):
        if speaker_id is None:
            speaker_id = self.speaker_id
        query = {
            "speaker": speaker_id,
            "text": text
        }
        for i in range(self.max_retry):
            try:
                response = requests.post(
                f"http://{self.host}:{self.port}/audio_query",
                params=query,
                timeout=10)
                if response.status_code == 200:
                    return response.json(), query
            except:
                pass
    
    def create_wav(self, query, params):
        for i in range(self.max_retry):
            try:
                response = requests.post(
                f"http://{self.host}:{self.port}/synthesis",
                headers={"Content-Type": "application/json"},
                params=params,
                data=json.dumps(query),
                timeout=10)
                if response.status_code == 200:
                    return response.content
            except:
                pass
    
    def save_audio(self, content, filename):
        with open(filename, "wb") as f:
            f.write(content)
    
    def call_voicevox(self, text, filename, speaker_id=None):
        query, params = self.create_query(text, speaker_id)
        content = self.create_wav(query, params)
        self.save_audio(content, filename)

if __name__ == "__main__":
    manager = VoiceVoxManager()
    start = time.time()
    input_text = "こんにちは"
    query, params = manager.create_query(input_text)
    content = manager.create_wav(query, params)
    with open("../../data/sounds/test1.wav", "wb") as f:
        f.write(content)

    print(time.time() - start)