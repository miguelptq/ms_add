from tkinter import *
from tkinter import Tk
from datetime import datetime, timedelta
import re


class MainWindow:
    def __init__(self):
        self.main_window = Tk()
        self.ammount_ms_lbl = Label(self.main_window, text= "Command List")
        self.ammount_ms_lbl.grid(row=0, column=0)
        self.text_widget = Text(self.main_window, width=50, height=10)
        self.text_widget.grid(row=1, column=0, sticky="nsew")

        self.ammount_ms_lbl = Label(self.main_window, text= "Ammount of Ms to Add")
        self.ammount_ms_lbl.grid(row=2, column=0, sticky="w")
        self.ammount_ms_entry = Entry(self.main_window)
        self.ammount_ms_entry.grid(row=3, column=0, columnspan = 2, sticky="nsew")

        self.add_ms_btn = Button(self.main_window, text="Add Ms", command=self.on_button_click)
        self.add_ms_btn.grid(row=4, column=0, sticky="ws",pady=20)
        self.main_window.rowconfigure(0, weight=1)
        self.main_window.columnconfigure(0, weight=1)

    def on_text_change(self,event):
        self.text_widget.configure(height=1 + len(self.text_widget.get("1.0", "end-1c")) // self.text_widget.cget("width"))

    def on_button_click(self):
        def is_valid_line(line):
            pattern = r'^\d+\|\d+,\d+,(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3})$'
            match = re.match(pattern, line)
            return bool(match)
        ms_to_add = 0
        if self.ammount_ms_entry.get():
            ms_to_add = int(self.ammount_ms_entry.get())
        lines = self.text_widget.get("1.0", "end-1c").split("\n")
        for i, line in enumerate(lines, 1):
            if not is_valid_line(line):
                 print(f"Invalid line: {line}")
            else:
                time_str = line.split(",")[2].strip()
                time_format = "%Y-%m-%dT%H:%M:%S.%f"
                time_obj = datetime.strptime(time_str, time_format)
                time_obj += timedelta(milliseconds=ms_to_add)
                new_time_str = time_obj.strftime(time_format)
                if new_time_str.endswith('000'):
                        new_time_str = new_time_str[:-3]
                lines[i-1] = line.replace(time_str, new_time_str)
                print(lines[i-1])
        print("---End---")
