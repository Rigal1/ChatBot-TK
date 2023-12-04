import tkinter as tk
import threading

from middleware import event_handler, image_control_handler, sound_handler, chatbot_handler
from gui import frame_controller, chat_frame, parameters_frame, chat_status_frame
from backend import chat_manager
from backend.utils import sound_manager, voice_recognize_manager, voicevox_manager, image_manager
from backend.bot_utils import bot

# GUIの作成
root = tk.Tk()
root.title("Chatbot Interface")

# チャットボットのインスタンスを作成
bot = bot.Bot()
voicevox_manager = voicevox_manager.VoiceVoxManager()
image_manager = image_manager.ImageManager()
voice_recognize_manager = voice_recognize_manager.VoiceRecognizeManager()

# メインウィンドウのグリッドの重みを設定して、リサイズに対応
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3) # チャットログの幅を調整
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)

chat_manager = chat_manager.ChatManager(bot, voicevox_manager)

frame_controller = frame_controller.FrameController(
    image_control_handler=image_control_handler.ImageControlHandler(image_manager),
    event_handler=event_handler.EventHandler(),
    sound_handler=sound_handler.SoundHandler(sound_manager.SoundManager()),
    chatbot_hundler=chatbot_handler.ChatbotHandler(chat_manager)
)

chat_status_frame = chat_status_frame.ChatStatusFrame(root, frame_controller)
chat_status_frame.grid(row=0, column=0, sticky="nw")

parameters_frame = parameters_frame.ParametersFrame(root, frame_controller, bot)
parameters_frame.grid(row=1, column=0, sticky="sw", padx=5, pady=5)

chat_frame = chat_frame.ChatFrame(root, frame_controller)
chat_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")


def send_message(event=None):
    user_input = user_input_box.get("1.0", tk.END).strip()
    if user_input:
        # ユーザーの入力をログに追加
        chat_frame.add_message_frame(user_input, "user")
        # 入力ボックスをクリア
        user_input_box.delete("1.0", tk.END)

        # チャットボットの応答をログに追加
        threading.Thread(target=process_bot_response, args=(user_input,)).start()
        return "break"  # テキストボックスの改行を防ぐ

def process_bot_response(user_input):
    data = frame_controller.call_chatbot(user_input)
    chat_frame.add_message_frame(data["reply"], "bot", emotion=data["emotion"])
    frame_controller.play_sound()
    chat_status_frame.update_info(data)

user_input_box = tk.Text(root, height=3)
user_input_box.grid(row=2, column=0, columnspan=3, sticky="ew")
user_input_box.bind("<Return>", send_message)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=2, column=3, sticky="e")

root.bind('<Configure>', lambda e: chat_frame.onFrameConfigure(None))

root.mainloop()