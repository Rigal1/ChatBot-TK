import speech_recognition as sr

class VoiceRecognizeManager:
    def __init__(self, pause_threshold=1, energy_threshold = 200):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = pause_threshold
        self.recognizer.energy_threshold = energy_threshold

    def recognize(self):
        try:
            with sr.Microphone(device_index=0) as source:
                ## 録音開始
                print("録音開始・・・")
                audio = self.recognizer.listen(source)
                ## 音声ファイル保存
                with open("data/sounds/user_audio.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                    print("録音終了")
        except Exception as e:
            print(e)
