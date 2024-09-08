import tkinter
from tkinter import *
import datetime
from datetime import date
import urllib.request
import time

global jam
jam = 0

class App:
    def __init__(self, window, window_title):


        self.window = window
        self.window.title(window_title)
        window_height = 350
        window_width = 300

        screen_width = self.window .winfo_screenwidth()
        screen_height = self.window .winfo_screenheight()
        
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))


        self.window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.window.rowconfigure(0, minsize=100, weight=1)
        self.window.columnconfigure(1, minsize=200, weight=1)
        
        fr_button = Frame(self.window)
        fr_graph = Frame(self.window)
        fr_result = Frame(self.window)
        
        self.lbl_obj = Label(fr_button, text="Summary:", font=('Times 14'))
        self.lbl_obj.grid(row=15, column=0, padx=10, pady=5, sticky="w")

        self.lbl_mag_min = Label(fr_button, text="MAC Address", font=('Times 14'))
        self.lbl_mag_min.grid(row=16, column=0, padx=10, pady=5, sticky="w")
        self.lbl_sabes = Label(fr_button, text=": 0 ", font=('Times 14'))
        self.lbl_sabes.grid(row=16, column=1, padx=5, pady=5, sticky="w")

        self.lbl_mag_max = Label(fr_button, text="Device ID", font=('Times 14'))
        self.lbl_mag_max.grid(row=17, column=0, padx=10, pady=5, sticky="w")
        self.lbl_batu = Label(fr_button, text=": 0 ", font=('Times 14'))
        self.lbl_batu.grid(row=17, column=1, padx=5, pady=5, sticky="w")

        self.lbl_phase_min = Label(fr_button, text="Pintu", font=('Times 14'))
        self.lbl_phase_min.grid(row=18, column=0, padx=10, pady=5, sticky="w")
        self.lbl_cy = Label(fr_button, text=": 0", font=('Times 14'))
        self.lbl_cy.grid(row=18, column=1, padx=5, pady=5, sticky="w")

        self.lbl_phase_max = Label(fr_button, text="Object local", font=('Times 14'))
        self.lbl_phase_max.grid(row=19, column=0, padx=10, pady=5, sticky="w")
        self.lbl_val = Label(fr_button, text=": None", font=('Times 14'))
        self.lbl_val.grid(row=19, column=1, padx=5, pady=5, sticky="w")

        self.lbl_rtsp1 = Label(fr_button, text="Status ", font=('Times 14'))
        self.lbl_rtsp1.grid(row=20, column=0, padx=10, pady=5, sticky="w")
        self.lbl_rtsp1val = Label(fr_button, text=": None", font=('Times 14'))
        self.lbl_rtsp1val.grid(row=20, column=1, padx=5, pady=5, sticky="w")

        fr_button.grid(row=0, column=0, sticky="ns")
        fr_graph.grid(row=0, column=1, sticky="nsew")
        fr_result.grid(row=0, column=2, sticky="nsew")

        
        self.window.after(2000, self.timer)

        self.window.mainloop()
        
    
    
    def timer(self):
        global jam

        #print(datetime.datetime.now())
        if self.connect():
            self.lbl_rtsp1val['text'] = ": Connected"
            print("Connected")
        else:
            self.lbl_rtsp1val['text'] = ": Connection loss"
            print("connection loss")
            
        current_time = datetime.datetime.now()
        if jam != current_time.hour:
            jam = current_time.hour            

        self.window.after(3000, self.timer)
        

        
    def connect(self, host='http://google.com'):
        try:
            urllib.request.urlopen(host) #Python 3.x           
            return True
        except:
            return False

# Create a window and pass it to the Application object
App(tkinter.Tk(), "IoT Measurement. 1.0")