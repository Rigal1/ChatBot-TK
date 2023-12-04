import tkinter as tk

class ChatStatusFrame(tk.Frame):
    def __init__(self, parent, frame_controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.chatbot_control_frame = tk.Frame(parent)
        self.chatbot_control_frame.grid(row=0, column=0, sticky="nw")

        self.AVATAR_SIZE_PX = 300
        self.frame_controller = frame_controller

        self.labels = {}
        self.entries = {}
        self.buttons = {}

        # チャットボットの表情を表示するラベル
        self.expression_label = tk.Label(self.chatbot_control_frame)
        self.expression_label.grid(row=0, column=0, columnspan=3)

        # コントロールボタン
        self.buttons["SaveLog"] = tk.Button(self.chatbot_control_frame, text="セーブ", command=self.save_log)
        self.buttons["SaveLog"].grid(row=1, column=0)

        self.buttons["LoadLog"] = tk.Button(self.chatbot_control_frame, text="ロード", command=self.load_log)
        self.buttons["LoadLog"].grid(row=1, column=1)

        self.buttons["ClearChat"] = tk.Button(self.chatbot_control_frame, text="クリア", command=self.clear_log)
        self.buttons["ClearChat"].grid(row=1, column=2)

        # レスポンスデータフレーム
        self.response_data_frame = tk.Frame(self.chatbot_control_frame)
        self.response_data_frame.grid(row=2, column=0, columnspan=3)

        self.labels["ResponseTime"] = tk.Label(self.response_data_frame, text="応答時間")
        self.labels["ResponseTime"].grid(row=0, column=0, sticky='w')
        self.entries["ResponseTime"] = tk.Entry(self.response_data_frame, state='readonly')
        self.entries["ResponseTime"].grid(row=1, column=0, sticky='w')

        self.labels["CurrentPrice"] = tk.Label(self.response_data_frame, text="費用")
        self.labels["CurrentPrice"].grid(row=0, column=1, sticky='w')
        self.entries["CurrentPrice"] = tk.Entry(self.response_data_frame, state='readonly')
        self.entries["CurrentPrice"].grid(row=1, column=1, sticky='w')

        self.labels["TotalPrice"] = tk.Label(self.response_data_frame, text="総費用")
        self.labels["TotalPrice"].grid(row=0, column=2, sticky='w')
        self.entries["TotalPrice"] = tk.Entry(self.response_data_frame, state='readonly')
        self.entries["TotalPrice"].grid(row=1, column=2, sticky='w')

        self.labels["IsConversationEnd"] = tk.Label(self.response_data_frame, text="会話終了判定")
        self.labels["IsConversationEnd"].grid(row=0, column=3, sticky='w')
        self.entries["IsConversationEnd"] = tk.Entry(self.response_data_frame, state='readonly')
        self.entries["IsConversationEnd"].grid(row=1, column=3, sticky='w')

        initial_image = self.frame_controller.load_resized_image("data/chara/images/neutral.png", resize=(self.AVATAR_SIZE_PX, self.AVATAR_SIZE_PX))

        self.expression_label.configure(image=initial_image)
        self.expression_label.image = initial_image  # 画像の参照を保持

    def update_info(self, data):
        for key in self.entries.keys():
            self.entries[key].config(state='normal')
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, data[key])
            self.entries[key].config(state='readonly')

        # 応答に応じた画像を更新（例: 'happy'）
        expression_image = self.frame_controller.load_expression_image(data["emotion"], resize=(self.AVATAR_SIZE_PX, self.AVATAR_SIZE_PX))
        self.expression_label.configure(image=expression_image)
        self.expression_label.image = expression_image  # 画像の参照を保持する

    
    
    def save_log(self):
        self.frame_controller.save_log()

    def load_log(self):
        self.frame_controller.load_log()

    def clear_log(self):
        self.frame_controller.clear_log()