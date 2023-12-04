import tkinter as tk
from tkinter import ttk

ICON_SIZE_PX = 50

class ChatFrame(tk.Canvas):
    def __init__(self, parent, frame_controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.frame = tk.Frame(self)
        self.vsb = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=self.vsb.set)

        self.frame_controller = frame_controller

        # ユーザーのアイコン画像を初期化
        self.user_image = self.frame_controller.load_resized_image("data/user/user_icon.png", resize=(ICON_SIZE_PX, ICON_SIZE_PX))

        # ボットのアイコン画像を初期化
        self.bot_images = {}

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

    def add_message_frame(self, text, sender, emotion=None):
        row_number = self.frame.grid_size()[1]

        if sender == "user":
            icon_label = tk.Label(self.frame, image=self.user_image)
            icon_label.image = self.user_image  # 参照を保持
            icon_label.grid(row=row_number, column=0, sticky='ns')
            text_column = 1
        else:
            bot_image = self.frame_controller.load_expression_image(emotion, resize=(ICON_SIZE_PX, ICON_SIZE_PX))
            self.bot_images[len(self.bot_images)] = bot_image
            icon_label = tk.Label(self.frame, image=bot_image)
            icon_label.image = bot_image  # 画像の参照を保持する
            icon_label.grid(row=row_number, column=0, sticky='ns')
            text_column = 1

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

    # Placeholder method to clear the chat (implementation depends on the specific GUI setup)
    def clear_chat(self):
        # Clear the display of the chat
        # Assuming the chat messages are displayed in a frame or similar widget
        # Here we need to remove all widgets from the frame
        for widget in self.frame.winfo_children():
            widget.destroy()
