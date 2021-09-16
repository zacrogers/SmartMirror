import requests
from bs4 import BeautifulSoup
import csv
import datetime as dt
from apscheduler.schedulers.background import BackgroundScheduler
from collections import namedtuple
import atexit

NodeData = namedtuple("NodeData", "light temperature humidity")

class SensorNode:
    ''' Class for interacting with web server hosted on ESP12 based sensor board. '''
    def __init__(self, name, ip_addr, trig_time=None, trig_level=None):
        self.name = name
        self.ip_addr = ip_addr
        self.trig_time = trig_time
        self.trig_level = trig_level
        self.data = NodeData("1", "2", "3")
        self.power_node = None
        self.timer_enabled = False

    def get_data(self):
        ''' Fetches light, temperature and humidity data from web server'''
        try:
            data = requests.get(self.ip_addr)

            if(data.status_code == 200):
                soup = BeautifulSoup(data.text, 'html.parser')
                table = soup.find("table", class_="sensor_values")
                headers = [header.text for header in table.findAll("th")]
                values = [{headers[i]: cell.text for i, cell in enumerate(row.find_all('td'))}
                            for row in table.find_all('tr')]

                vals = list(values[1].values()) #  First row in list is empty so only return second
                self.data = NodeData(vals[0], vals[1], vals[2])

        except requests.exceptions.RequestException as e:
            print(e)
            return False
    
    def update_power_node(self):
        if self.power_node is None:
            return

        if self.timer_enabled:
            time_split = self.trig_time.split(":")
            _trig_time = dt.time(int(time_split[0]), int(time_split[1]), 0)
            current_time = dt.datetime.now().time()

            self.get_data()

            if(current_time >= _trig_time):
                if(self.data.light < self.trig_level):
                    self.power_node.all_on()


class PowerNode:
    ''' Class for interacting with web server hosted on ESP12 based relay controlling board. '''
    def __init__(self, name, ip_addr):
        self._NUM_CHANNELS = 4  
        self.name = name
        self.ip_addr = ip_addr
        self.relay_states = list([0, 0, 0, 0])
        self.channel_labels = list(["1", "2", "3", "4"])
        
        self.get_state()

    def get_state(self):
        ''' Get current state of all power outlets in node. '''
        try:
            data = requests.get(f"{self.ip_addr}/relay_states")

            if(data.status_code == 200):
                soup = BeautifulSoup(data.text, 'html.parser')
                table = soup.find("table", class_="relay_states")
                headers = [header.text for header in table.findAll("th")]
                values = [{headers[i]: cell.text for i, cell in enumerate(row.find_all('td'))}
                            for row in table.find_all('tr')]

                self.relay_states = list(values[1].values()) #  First row in list is empty so only return second

        except requests.exceptions.RequestException as e:
            print(e)
            return False

    def turn_on(self, relay_num):
        ''' Turn on single outlet. '''
        try:
            data = requests.get(f"{self.ip_addr}/relay_{relay_num}_on")

            if(data.status_code == 200):
                self.get_state()

        except requests.exceptions.RequestException as e:
            print(e)

    def turn_off(self, relay_num):
        ''' Turn off single outlet. '''
        try:
            data = requests.get(f"{self.ip_addr}/relay_{relay_num}_off")

            if(data.status_code == 200):
                self.get_state()

        except requests.exceptions.RequestException as e:
            print(e)

    def all_on(self):
        ''' Turn all outlets on. Leaves them on if they already are. '''
        for i in range(4):
            self.turn_on(i+1)

    def all_off(self):
        ''' Turn all outlets off. Leaves them off if they already are. '''
        for i in range(4):
            self.turn_off(i+1)

    def set_channel_label(self, num:int, label:str):
        ''' Set display label for node channels. '''
        if(num < self._NUM_CHANNELS-1):
            return

        self.channel_labels[num] = label
        

