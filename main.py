import tkinter as tk
from tkinter import scrolledtext, ttk, PhotoImage, scrolledtext
from PIL import Image, ImageTk
import time
import json
import threading
import chatbot  # 仮のchatbotライブラリ

ICON_SIZE_PX = 80
AVATAR_SIZE_PX = ICON_SIZE_PX * 4

class ChatFrame(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.frame = tk.Frame(self)
        self.vsb = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=self.vsb.set)

        # ユーザーのアイコン画像をロード
        self.user_image = load_and_resize_image("data/user/user_icon.png", size=(ICON_SIZE_PX, ICON_SIZE_PX))
        # ボットのアイコン画像を初期化
        self.bot_images = {}

        # Initialize the list to store messages and emotions
        self.conversation_log = []

        # スクロールバーをgridに配置します。右側に余白が出ないようにcolumn=3に設定します。
        self.vsb.grid(row=0, column=3, sticky='ns', rowspan=2)  # Modification: Move scrollbar to the far right
        
        # Canvasをgridに配置します。右側に余白が出ないようにcolumn=1に設定します。
        self.grid(row=0, column=1, sticky='nsew')
        
        self.create_window((0, 0), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        # ウィジェットの配置にgridを使うために、親フレームのgridの重みを設定
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        # Configureイベントをバインドして、ウィンドウのリサイズに応じてwraplengthを更新します。
        self.bind("<Configure>", self.onCanvasConfigure)

        # Mousewheel event for scrolling
        parent.bind("<MouseWheel>", self.on_mousewheel)  # Modification: Bind mousewheel event

    def on_mousewheel(self, event):  # Modification: Add this method to handle mouse wheel scrolling
        self.yview_scroll(-1*(event.delta//120), "units")

    

    def add_message(self, text, sender="user", emotion="NEUTRAL"):
        row_number = self.frame.grid_size()[1]

        if sender == "user":
            icon_label = tk.Label(self.frame, image=self.user_image)
            icon_label.image = self.user_image  # 参照を保持
            icon_label.grid(row=row_number, column=0, sticky='ns')
            text_column = 1
            role = "user"
        else:
            bot_image = get_bot_expression_image(emotion, resize=(ICON_SIZE_PX, ICON_SIZE_PX))
            self.bot_images[len(self.bot_images)] = bot_image
            icon_label = tk.Label(self.frame, image=bot_image)
            icon_label.image = bot_image  # 画像の参照を保持する
            icon_label.grid(row=row_number, column=0, sticky='ns')
            text_column = 1
            role = "assistant"

        self.conversation_log.append({"role": role, "content": text})

        color = "#DDDDDD" if sender == "user" else "#AAAAAA"
        label = tk.Label(self.frame, text=text, bg=color, anchor="w", justify="left")
        
        label.grid(row=row_number, column=text_column, sticky='ew')
        self.frame.grid_columnconfigure(0, weight=1)

        
        # ラベルにConfigureイベントをバインドするのではなく、
        # Canvasのサイズ変更時に全てのラベルを更新するようにします。
        # label.bind('<Configure>', lambda e, l=label: self.update_label_wraplength(l))
        self.update_label_wraplength(label)

        self.update_idletasks()  # Update the layout to get the correct scroll region size
        self.yview_moveto(1)  # Move the yview to the bottom

    def onCanvasConfigure(self, event):
        # Canvasのサイズが変更されたときに呼び出されます。
        # ここで全てのラベルのwraplengthを更新します。
        self.update_labels_wraplength()
    
    def update_label_wraplength(self, label):
        # ラベルのwraplengthをCanvasの現在の幅に基づいて設定します。
        self.update_idletasks() 
        canvas_width = self.winfo_width()
        padding = 20  # 余白を設定します。
        label.configure(wraplength=canvas_width - ICON_SIZE_PX - padding)  # Modification: Adjust the padding.

    def update_labels_wraplength(self):
        # フレーム内のすべてのラベルのwraplengthを更新します。
        self.update_idletasks() 
        canvas_width = self.winfo_width()
        padding = 20  # 余白を設定します。
        for label in self.frame.winfo_children():
            if isinstance(label, tk.Label):
                label.configure(wraplength=canvas_width - ICON_SIZE_PX - padding)  # Modification: Adjust the padding for all labels.

    def onFrameConfigure(self, event):
        # スクロール領域を更新します。
        self.configure(scrollregion=self.bbox("all"))

    def save_conversation_log(self):
        # Assuming the function to get the current emotion
        current_emotion = self.get_emotion()  # Placeholder function

        # Format the conversation log
        formatted_log = [{"messages": self.conversation_log, "emotion": current_emotion}]

        # Save the formatted log to a JSON file
        # For demonstration purposes, printing the JSON string
        with open('./data/user/conversation_log.json', 'w', encoding="utf-8") as file:
            json.dump(formatted_log, file, indent=4)
        # print(json.dumps(formatted_log, indent=4))

    # Placeholder for the get_emotion function
    def get_emotion(self):
        return "GetEmotion"  # Example return value
    
    def load_conversation_log(self):
        # For demonstration purposes, assuming a hardcoded file path
        # In a real application, you would use a file dialog or a configurable file path
        try:
            with open('./data/user/conversation_log.json', 'r', encoding="utf-8") as file:
                loaded_log = json.load(file)

            # Clear the current chat
            # This part depends on how the chat messages are displayed in the GUI
            # Assuming there's a method in ChatFrame to clear the chat
            self.clear_chat()

            # Load the messages from the log
            for entry in loaded_log:
                for message in entry["messages"]:
                    self.add_message(message["content"], message["role"])

        except Exception as e:
            print("Error loading log:", e)

    # Placeholder method to clear the chat (implementation depends on the specific GUI setup)
    def clear_chat(self):
        # Clear the conversation log
        bot.delete_memory()
        self.conversation_log.clear()

        # Clear the display of the chat
        # Assuming the chat messages are displayed in a frame or similar widget
        # Here we need to remove all widgets from the frame
        for widget in self.frame.winfo_children():
            widget.destroy()


def load_and_resize_image(image_path, size=(50, 50)):
    # PILを使って画像を開き、リサイズします。
    image = Image.open(image_path)
    image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)

# 画像を取得する関数（仮に定義）
def get_bot_expression_image(expression, resize=(50, 50)):
    # ここで画像のファイルパスを選択します。実際には表情に応じた画像を返す必要があります。
    character_dir = "chara" # 仮のディレクトリ名
    if expression == "CONFUSION" or expression == "SURPRISED":
        expression = "NEUTRAL"
        
    image_paths = {
        "JOY": f"data/{character_dir}/happy.png",
        "NEUTRAL": f"data/{character_dir}/neutral.png",
        "SAD": f"data/{character_dir}/sad.png",
        "ANGRY": f"data/{character_dir}/angry.png"
    }
    return load_and_resize_image(image_paths[expression], size=resize)

# チャットボットからの応答を取得し、ログに表示する関数
def send_message(event=None):
    user_input = user_input_box.get("1.0", tk.END).strip()
    if user_input:
        # ユーザーの入力をログに追加
        chat_frame.add_message(user_input, "user")
        # 入力ボックスをクリア
        user_input_box.delete("1.0", tk.END)

        # チャットボットの応答をログに追加
        threading.Thread(target=process_bot_response, args=(user_input,)).start()
        return "break"  # テキストボックスの改行を防ぐ
        
        
def process_bot_response(user_input):
    # チャットボットの応答を取得（この操作は数秒かかると仮定）
    bot_response = bot.generate_reply_memory(user_input)

    # GUI操作はメインスレッドで行う必要があるため、
    # 応答をログに追加する部分をafterを使ってメインスレッドで実行する
    root.after(0, update_chat_log, bot_response)

def update_chat_log(bot_response):
    # チャットボットの応答をログに追加
    chat_frame.add_message(bot_response["reply"], "bot", bot_response["emotion"])
    response_time_entry.config(state='normal')
    response_time_entry.delete(0, tk.END)
    response_time_entry.insert(0, bot_response["ResponseTime"])
    response_time_entry.config(state='readonly')
    
    current_price_entry.config(state='normal')
    current_price_entry.delete(0, tk.END)
    current_price_entry.insert(0, bot_response["CurrentPrice"])
    current_price_entry.config(state='readonly')
    
    total_price_entry.config(state='normal')
    total_price_entry.delete(0, tk.END)
    total_price_entry.insert(0, bot_response["TotalPrice"])
    total_price_entry.config(state='readonly')

    is_conversation_end_entry.config(state='normal')
    is_conversation_end_entry.delete(0, tk.END)
    is_conversation_end_entry.insert(0, bot_response["IsConversationEnd"])
    is_conversation_end_entry.config(state='readonly')

    # 応答に応じた画像を更新（例: 'happy'）
    expression_image = get_bot_expression_image(bot_response["emotion"], resize=(AVATAR_SIZE_PX, AVATAR_SIZE_PX))
    expression_label.configure(image=expression_image)
    expression_label.image = expression_image  # 画像の参照を保持する



# パラメーター設定エリア
class ParametersFrame(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, text="Parameters", *args, **kwargs)
        self.parameters = {}  # This will store the parameter entries as a dictionary.
        self.load_parameters_from_json()  # Load parameters from JSON at initialization
        self.create_widgets()
        
    def create_widgets(self):
        # Add Parameter button

        # Dropdown menu elements
        self.dropdown_options = ["Option 1", "Option 2", "Option 3"]  # This list can be dynamically updated
        # Dropdown (Combobox) creation
        self.dropdown_label = tk.Label(self, text="プロンプトver.")
        self.dropdown = ttk.Combobox(self, values=self.dropdown_options, state="readonly")

        # Adding the dropdown to the grid
        self.dropdown_label.grid(row=99, column=0, sticky="w")  # Placed at row 99 for simplicity
        self.dropdown.grid(row=99, column=1, sticky="ew")

        # Set the default value to the first option
        self.dropdown.set(self.dropdown_options[0])

        # Add Parameter button moved below the dropdown for better layout

        # self.add_button = tk.Button(self, text="Add Parameter", command=self.add_parameter)
        # self.add_button.grid(row=100, column=0, sticky="w")

        # Adding a button to reload parameters from JSON
        self.reload_button = tk.Button(self, text="Reload Parameters", command=self.load_parameters_from_json)
        self.reload_button.grid(row=101, column=0, sticky="w")  # Placed at row 101 for simplicity

        # Save parameters button
        self.save_button = tk.Button(self, text="Save Parameters", command=self.save_parameters)
        self.save_button.grid(row=101, column=1, sticky="w")  # Placed next to the load button
        
        # Initialize the frame with 8 parameters
        # for i in range(4):
        #     self.add_parameter()

    def load_parameters_from_json(self):
        # Clear existing parameters
        for label, entry in self.parameters.values():
            label.destroy()
            entry.destroy()
        self.parameters.clear()
        
        # Load parameters from JSON
        with open('./data/user/parameters.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            
        # Create parameters based on loaded JSON
        for row, (key, value) in enumerate(data.items(), start=1):
            label = tk.Label(self, text=key)
            entry = tk.Entry(self)
            entry.insert(0, value)  # Set the default value from JSON
            self.parameters[key] = (label, entry)
            label.grid(row=row, column=0, sticky="w")
            entry.grid(row=row, column=1)
        bot.set_prompt(data)

    def save_parameters(self):
        # Collect current parameters into a dictionary
        # print(self.parameters)
        parameters_dict = {}
        for label, entry in self.parameters.values():
            print(label.cget("text"), entry.get())
            parameters_dict[label.cget("text")] = entry.get()
        # parameters_dict = {label.cget("text"): entry.get() for label, entry in self.parameters}
        
        # Save the parameters to a JSON file
        with open('./data/user/parameters.json', 'w', encoding="utf-8") as file:
            json.dump(parameters_dict, file, indent=4)
        
    def apply_parameters(self):
        # Here, you'd handle the parameters, for example:
        for key, (label, entry) in self.parameters.items():
            print(f"{key}: {entry.get()}")  # Example output

    def add_parameter(self):
        # Calculate the next row number for the new parameter
        row_number = len(self.parameters) + 1
        # Create a new label and entry for the parameter
        label = tk.Label(self, text=f"Param {row_number}")
        entry = tk.Entry(self)
        # Store the label and entry in the parameters list
        self.parameters.append((label, entry))
        # Place the label and entry on the grid
        label.grid(row=row_number, column=0, sticky="w")
        entry.grid(row=row_number, column=1)

        

    # def apply_parameters(self):
    #     # Here, you'd handle the parameters, for example:
    #     for index, (label, entry) in enumerate(self.parameters):
    #         print(f"Param {index+1}: {entry.get()}")  # Example output

# GUIの作成
root = tk.Tk()
root.title("Chatbot Interface")

# チャットボットのインスタンスを作成
bot = chatbot.Bot()

# メインウィンドウのグリッドの重みを設定して、リサイズに対応
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3) # チャットログの幅を調整
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)


# パラメーター設定フレーム（左下に配置）
parameters_frame = ParametersFrame(root)
parameters_frame.grid(row=1, column=0, sticky="sw", padx=5, pady=5)


# チャットフレーム（右側に配置）
chat_frame = ChatFrame(root)
chat_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

# チャットボットのコントロールフレームを作成
chatbot_control_frame = tk.Frame(root)
chatbot_control_frame.grid(row=0, column=0, sticky="nw")

# チャットボットの表情を表示するラベル（新しいフレーム内に配置）
expression_label = tk.Label(chatbot_control_frame)
expression_label.grid(row=0, column=0, columnspan=3)

# コントロールボタンをフレーム内に横並びで配置
save_log_button = tk.Button(chatbot_control_frame, text="Save Log", command=chat_frame.save_conversation_log)
save_log_button.grid(row=1, column=0)

load_log_button = tk.Button(chatbot_control_frame, text="Load Log", command=chat_frame.load_conversation_log)
load_log_button.grid(row=1, column=1)

clear_chat_button = tk.Button(chatbot_control_frame, text="Clear Chat", command=chat_frame.clear_chat)
clear_chat_button.grid(row=1, column=2)

# レスポンスデータを表示するためのウィジェットを作成
response_data_frame = tk.Frame(chatbot_control_frame)
response_data_frame.grid(row=2, column=0, columnspan=3)

# ResponseTime
response_time_label = tk.Label(response_data_frame, text="応答時間")
response_time_label.grid(row=0, column=0, sticky='w')
response_time_entry = tk.Entry(response_data_frame, state='readonly')
response_time_entry.grid(row=1, column=0, sticky='w')

# CurrentPrice
current_price_label = tk.Label(response_data_frame, text="費用")
current_price_label.grid(row=0, column=1, sticky='w')
current_price_entry = tk.Entry(response_data_frame, state='readonly')
current_price_entry.grid(row=1, column=1, sticky='w')

# TotalPrice
total_price_label = tk.Label(response_data_frame, text="総費用")
total_price_label.grid(row=0, column=2, sticky='w')
total_price_entry = tk.Entry(response_data_frame, state='readonly')
total_price_entry.grid(row=1, column=2, sticky='w')

# IsConversationEnd
is_conversation_end_label = tk.Label(response_data_frame, text="会話終了判定")
is_conversation_end_label.grid(row=0, column=3, sticky='w')
is_conversation_end_entry = tk.Entry(response_data_frame, state='readonly')
is_conversation_end_entry.grid(row=1, column=3, sticky='w')


# ユーザー入力エリアと送信ボタン（下部に配置）
user_input_box = tk.Text(root, height=3)
user_input_box.grid(row=2, column=0, columnspan=3, sticky="ew")
user_input_box.bind("<Return>", send_message)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=2, column=3, sticky="e")



root.bind('<Configure>', lambda e: chat_frame.onFrameConfigure(None))

# 最初のアバター画像をセット
initial_expression_image = get_bot_expression_image("JOY", resize=(AVATAR_SIZE_PX, AVATAR_SIZE_PX))
expression_label.configure(image=initial_expression_image)
expression_label.image = initial_expression_image  # 画像の参照を保持

root.mainloop()
