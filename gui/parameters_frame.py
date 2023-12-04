import tkinter as tk
from tkinter import ttk

# パラメーター設定エリア
class ParametersFrame(tk.LabelFrame):
    def __init__(self, parent, frame_controller, bot, *args, **kwargs):
        super().__init__(parent, text="Parameters", *args, **kwargs)
        self.bot = bot # Reference to the bot object
        self.frame_controller = frame_controller
        self.parameters = {}  # This will store the parameter entries as a dictionary.
        self.load_parameters()  # Load parameters from JSON at initialization
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

        # Adding a button to reload parameters from JSON
        self.reload_button = tk.Button(self, text="Reload Parameters", command=self.load_parameters)
        self.reload_button.grid(row=101, column=0, sticky="w")  # Placed at row 101 for simplicity

        # Save parameters button
        self.save_button = tk.Button(self, text="Save Parameters", command=self.save_parameters)
        self.save_button.grid(row=101, column=1, sticky="w")  # Placed next to the load button
        
        # Initialize the frame with 8 parameters
        # for i in range(4):
        #     self.add_parameter()
    
    def clear_parameters(self):
        # Clear existing parameters
        for label, entry in self.parameters.values():
            label.destroy()
            entry.destroy()
        self.parameters.clear()
    
    def set_parameters(self, parameters):
        for row, (key, value) in enumerate(parameters.items(), start=1):
            label = tk.Label(self, text=key)
            entry = tk.Entry(self)
            entry.insert(0, value)  # Set the default value from JSON
            self.parameters[key] = (label, entry)
            label.grid(row=row, column=0, sticky="w")
            entry.grid(row=row, column=1)

    def load_parameters(self):
        self.clear_parameters()
        self.parameters = self.frame_controller.load_parameter()
        self.set_parameters(self.parameters)

    def read_parameters(self):
        for label, entry in self.parameters.values():
            print(label.cget("text"), entry.get())
            self.parameters[label.cget("text")] = entry.get()

    def save_parameters(self):
        self.frame_controller.save_parameter(self.parameters)

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

        
