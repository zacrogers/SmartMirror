#!/usr/bin/python3
import tkinter as tk
import time
import datetime
import os 
from PIL import ImageTk,Image
import json

# import weather
import news



class Mirror(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.DIR_PATH = os.path.dirname(os.path.realpath(__file__))
        self.NUM_HEADLINES = 10
        self.BG_COLOR = 'black'
        self.TEXT_COLOR = "white"
        self.FONT = "Verdana"
        self.CELSIUS = u"\u2103"
        self.CITIES = ["Auckland", "Wellington", "Christchurch", "Dunedin"]
        self.country = "NZ"

        self.home_city = self.CITIES[1]

        self.headline_labels = []
        self.temperature_labels = []

        self.load_settings()

        self.top_frame = tk.Frame(self, bg=self.BG_COLOR)

        # Date/time display
        self.dt_frame = tk.Frame(self.top_frame, bg=self.BG_COLOR)

        self.date = tk.Label(self.dt_frame, text=self.get_date(), bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=(self.FONT, 22))
        self.date.pack(expand=True, fill=tk.BOTH, side=tk.TOP, anchor=tk.E)

        self.clock = tk.Label(self.dt_frame, text=self.get_time(), bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=(self.FONT, 50))
        self.clock.pack(expand=True, fill=tk.BOTH, side=tk.TOP, anchor=tk.E)

        self.dt_frame.pack(expand=True, side=tk.LEFT)

        # Weather information
        self.temp_frame = tk.Frame(self.top_frame, bg=self.BG_COLOR)

        # Weather icon
        self.weather_canv = tk.Canvas(self.temp_frame, width=100, height=100, bg=self.BG_COLOR, highlightthickness=0)
        self.weather_image = Image.open(f"{self.DIR_PATH}/icons/Clear.png")
        self.weather_image = self.weather_image.resize((100, 100), Image.ANTIALIAS)

        self.weather_icon = ImageTk.PhotoImage(self.weather_image)
        self.canv_img = self.weather_canv.create_image(50, 50, image=self.weather_icon)
        self.weather_canv.pack(anchor=tk.E, side=tk.LEFT)

        # Temperature info
        # self.get_temperature()
        temp = 10 #weather.get_temp(self.home_city, self.country)
        self.home_temp_label = tk.Label(self.temp_frame, 
                                        text=f"{temp} {self.CELSIUS}", 
                                        bg=self.BG_COLOR, 
                                        fg=self.TEXT_COLOR, 
                                        font=(self.FONT, 40))

        self.home_temp_label.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, anchor=tk.S)

        self.temp_frame.pack(expand=True, side=tk.LEFT)
        self.top_frame.pack(expand=True, side=tk.TOP, fill=tk.BOTH, pady=60)

        # Filler to space out screen center
        self.filler = tk.Label(self, height=35, text='fill', bg=self.BG_COLOR)
        self.filler.pack(expand=True, fill=tk.BOTH)

        # News headlines
        self.hl_frame = tk.Frame(self, bg=self.BG_COLOR)
        self.get_headlines()
        self.hl_frame.pack(expand=True, side=tk.TOP, fill=tk.BOTH, padx=30) 

        # Start label updating callbacks
        self.parent.after(1000, self.refresh_settings)	
        self.parent.after(1000, self.update_time)
        self.parent.after(1000, self.update_date)
        self.parent.after(1000, self.update_home_temp)
        self.parent.after(1000, self.update_weather_status)
        self.parent.after(1000, self.update_headlines)

    def load_settings(self):
        with open(f"{self.DIR_PATH}/settings.json", "r") as f:
        	settings = json.load(f)
        	self.country = settings.get("country")
        	self.home_city = settings.get("city")

    def get_time(self):
        current_time = datetime.datetime.now()
        return current_time.strftime("%H:%M")

    def get_date(self):
        current_date = datetime.date.today()
        return current_date.strftime("%B %d, %Y")

    def get_temperature(self):
        row = 0
        for city in self.CITIES:
            temp = 100 
            # temp = weather.get_temp(city, self.country)
            temp_label = tk.Label(self.temp_frame, 
                                  text=f"{city} {temp}{self.CELSIUS}", 
                                  bg=self.BG_COLOR, 
                                  fg=self.TEXT_COLOR, 
                                  font=(self.FONT, 10))

            self.temperature_labels.append(temp_label)
            temp_label.pack(anchor=tk.W)           

    def get_weather_status(self, city, country):
        return "Clear" 
        # return weather.get_status(city, country)

    def get_headlines(self):
        hl = news.get_nz_headlines()

        for i in range(self.NUM_HEADLINES):

            # Remove website name
            line = hl[i].split('-')
            curr_line = ""
            for l in range(len(line)-1):
                curr_line+=line[l]

            # Limit string length to fit screen
            truncated_str = (curr_line[:108]) if len(curr_line) > 108 else curr_line

            l = tk.Label(self.hl_frame, 
                         text=truncated_str, 
                         bg=self.BG_COLOR, 
                         fg=self.TEXT_COLOR, 
                         font=(self.FONT, 10))

            self.headline_labels.append(l)
            l.pack(anchor=tk.W)


    ### Label content updating ###
    def refresh_settings(self):
    	self.load_settings()
    	self.parent.after(60000, self.refresh_settings)

    def update_time(self):
        self.clock.configure(text=self.get_time())
        self.parent.after(1000, self.update_time)

    def update_date(self):
        self.date.configure(text=self.get_date())
        self.parent.after(1000, self.update_date)

    def update_home_temp(self):
        temp = 10 
        # temp = weather.get_temp(self.home_city, self.country)
        self.home_temp_label.configure(text=f"{temp} {self.CELSIUS}")
        self.parent.after(60000, self.update_home_temp)

    def update_temperature(self):
        index = 0

        for city in self.CITIES:
            temp = weather.get_temp(city, self.country)
            self.temperature_labels[index].configure(text=f"{city} {temp}{self.CELSIUS}")
            index+=1

        self.parent.after(60000, self.update_temperature)

    def update_weather_status(self):
        status = "Clear" 
        # status =  weather.get_status(self.home_city, self.country)

        if self.is_daytime():
            self.weather_image = Image.open(f"{self.DIR_PATH}/icons/{status}.png")
        else:
            self.weather_image = Image.open(f"{self.DIR_PATH}/icons/Night_{status}.png")

        self.weather_image = self.weather_image.resize((100, 100), Image.ANTIALIAS)
        self.weather_icon = ImageTk.PhotoImage(self.weather_image)

        self.weather_canv.itemconfigure(self.canv_img, image=self.weather_icon)
        self.parent.after(60000, self.update_weather_status)


    def update_headlines(self):
        hl = news.get_nz_headlines()

        for i in range(self.NUM_HEADLINES):
            # Remove website name
            line = hl[i].split('-')
            curr_line = ""

            for l in range(len(line)-1):
                curr_line+=line[l]

            # Limit string length to fit screen
            truncated_str = (curr_line[:108]) if len(curr_line) > 108 else curr_line
            self.headline_labels[i].configure(text=truncated_str)

        self.parent.after(60000, self.update_headlines)

    # For weather icon display
    def is_daytime(self):
        seven_am = datetime.time(7,00,00)
        seven_pm = datetime.time(19,00,00)
        now = datetime.datetime.now().time()

        return True if now > seven_am and now < seven_pm else False


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Smart mirror")
    # root.attributes('-fullscreen', True, '-topmost', True)
    root.lift()
    m = Mirror(root, bg="black")
    m.pack(expand = True, fill=tk.BOTH)

    root.mainloop()
