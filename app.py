from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from apscheduler.schedulers.background import BackgroundScheduler
import datetime as dt
import atexit
import time
import pickle
import threading
import pandas as pd
import json
import os
import re

from music import AudioPlayer
from mirror_bt import BtStrip
from node_scraper import SensorNode, PowerNode


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
SENSOR_NODES_FILENAME = "node_config.pkl"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DIR_PATH}/users.db'
app.config['SECRET_KEY'] = 'potato'

db = SQLAlchemy(app)
# db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)

## Audio player
player = AudioPlayer()
headers = ["artist", "album", "song"]
tracks = player.track_db.filter(headers)
playlist = []

## Bluetooth power strip
bt_strip = BtStrip()
module_names = ["Bedroom", "Lounge", "Kitchen"]
power_strip_names = ["Lamp", "Uplights", "LED", "Monitor"]

# Sensor nodes
MAX_NODES = 4
sensor_nodes = []

lights_off = True

# Power nodes
power_nodes = []
power_nodes.append(PowerNode("Bedroom", "http://192.168.1.79"))



def update_time():
	global lights_off
	start = dt.time(19,0,0)
	end = dt.time(23,0,0)
	current_time = dt.datetime.now().time()

	if(current_time >= start and current_time <= end):

		if(lights_off):
			lights_off = False
			bt_strip.toggle_plug(int(1))
			time.sleep(5)
			bt_strip.toggle_plug(int(2))
			time.sleep(5)
			bt_strip.toggle_plug(int(3))


scheduler = BackgroundScheduler()
scheduler.start()

scheduler_jobs = []


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


for i in tracks.index:
    playlist.append((tracks[headers[0]][i],
                          tracks[headers[1]][i],
                          tracks[headers[2]][i]))

current_track = "Test"#playlist[0]

current_page = 'index.html'

cities = ["Wellington", "Christchurch", "Auckland", "Dunedin"]
current_city = ""


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


@app.route('/')
def index():
	user = User.query.filter_by(username = 'admin', password='1234')
	return render_template('index.html', current_track=current_track)
 

@app.route('/media', methods=['GET', 'POST'])
def media():
	global current_track
	global thread

	# Get string from form annd clean up into tuple for AudioPlayer()
	if request.method == "POST":
		req = request.form.get('tracks')

		full_string = ""
		for r in req:
			full_string+=r

		# Clean up string (remove quotes and brackets)
		st_to_tup = full_string[1:(len(full_string)-1)].split(',') #Strip brackets
		st_to_tup = [s.strip() for s in st_to_tup] # Strip whitespace
		st_to_tup = [s.strip("'") for s in st_to_tup] # Strip quotes
		st_to_tup = [s.strip("\\") for s in st_to_tup] # Strip backslashes

		current_track = tuple(st_to_tup)

	return render_template('media.html', tracks=playlist, current_track=current_track)#, thread=thread)


@app.route('/<action>', methods=['GET', 'POST'])
def action(action):

	if action == "play":
		player.play_track(*current_track)
	elif action == "stop":
		player.stop_track()
	elif action == "pause":
		player.pause_track()

	return redirect('/media')


@app.route('/power_strip', methods=['GET', 'POST'])
def power_strip():
	global power_nodes

	# Reload node states
	for node in power_nodes:
		node.get_state()

	if request.method == "POST":
		# Change node channel labels
		for node in power_nodes:
			for index, label in enumerate(node.channel_labels):
				label_form = request.form.get(f"pwr-node-{node.name}-{index}")

				if label_form:
					node.channel_labels[index] = label_form

		# Delete selected sensor node
		node_delete_form = request.form.get('nodes-delete')
		
		if node_delete_form:
			for node in sensor_nodes:
				if node.name == node_delete_form:
					power_nodes.remove(node)

		# Add new power node 
		name_form = request.form.get('node_name')
		ip_form   = request.form.get('node_ip')

		if name_form != None and ip_form != None:
			if re.match("^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$", ip_form):

				# Only add node if unique name and ip address
				has_name = False
				has_ip = False

				for node in power_nodes:
					if node.name == name_form:
						has_name = True

					if node.ip_addr == ip_form:
						has_name = True

				if not has_name and not has_ip:
					power_nodes.append(PowerNode(name_form, f"http://{ip_form}/sensors"))
			else:
				print("Not valid ip")					


	return render_template('power_strip.html', power_nodes=power_nodes, enumerate=enumerate)


@app.route('/sensors', methods=['GET', 'POST'])
def sensors():
	global sensor_nodes
	global scheduler_jobs

	# Load previous node data
	try:
		with open(f"{DIR_PATH}/{SENSOR_NODES_FILENAME}", "rb") as f:
			sensor_nodes = pickle.load(f)
	except Exception as e:
		print(e)

	# Update sensor node data
	for sensor in sensor_nodes:
		sensor.get_data()

		# if sensor.timer_enabled:
		# 	new_job = scheduler.add_job(func=sensor.update_power_node, trigger="interval", seconds=10)
		# 	scheduler_jobs.append(new_job)
	

	if request.method == "POST":
		# Delete selected sensor node
		node_delete_form = request.form.get('nodes-delete')

		if node_delete_form:
			for node in sensor_nodes:
				if node.name == node_delete_form:
					sensor_nodes.remove(node)


		# Update light triggering values for nodes
		for index, node in enumerate(sensor_nodes):
			slider_form = request.form.get(f'light-trigger-level{index}')
			time_form   = request.form.get(f'trigger-time{index}')
			timer_checkbox = request.form.get(f'timer-enabled-checkbox-{node.name}')

			node.trig_time = node.trig_time if time_form is None else time_form
			node.trig_level = node.trig_level if slider_form is None else slider_form 
			node.timer_enabled = False if timer_checkbox is None else True

		# Link power node to sensor node for timed triggering
		for sense_node in sensor_nodes:
			link_form = request.form.get(f'sense-node-link-{sense_node.name}')

			if link_form != "None":
				for pwr_node in power_nodes:
					if pwr_node.name == link_form:
						sense_node.power_node = pwr_node

				print(sense_node.timer_enabled)


		# Add new sensor node 
		name_form = request.form.get('node_name')
		ip_form   = request.form.get('node_ip')

		if name_form != None and ip_form != None:
			if re.match("^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$", ip_form):

				# Only add node if unique name and ip address
				has_name = False
				has_ip = False

				for node in sensor_nodes:
					if node.name == name_form:
						has_name = True

					if node.ip_addr == ip_form:
						has_ip = True

				if not has_name and not has_ip:
					sensor_nodes.append(SensorNode(name_form, f"http://{ip_form}/sensors"))
			else:
				print("Not valid ip")

		# Save sensor node data if changed
		try:
			with open(f"{DIR_PATH}/{SENSOR_NODES_FILENAME}", "wb") as f:
				pickle.dump(sensor_nodes, f)

		except Exception as e:
			print(e)

	# Because the sensor nodes list is reinitialised each time the page loads
	# the previous jobs need to be cleared each time to prevent them getting stuck
	for job in scheduler_jobs:
		job.remove()

	scheduler_jobs.clear()

	for node in sensor_nodes:
		if node.timer_enabled:
			new_job = scheduler.add_job(func=node.update_power_node, trigger="interval", seconds=60)
			scheduler_jobs.append(new_job)

	return render_template('sensors.html', str=str, sensor_nodes=sensor_nodes, power_nodes=power_nodes, enumerate=enumerate)


@app.route('/<strip>/<channel>')
def power_strip_action(strip, channel):
	for node in power_nodes:
		if strip == f"pwr_node_{node.name}":
			if int(node.relay_states[int(channel)]) == 0:
				node.turn_on(int(channel)+1)

			elif int(node.relay_states[int(channel)]) == 1:
				node.turn_off(int(channel)+1)
		

	# if strip == "st_1":
	# 	if channel == "ps_1":
	# 		bt_strip.toggle_plug(int(1))

	# 	elif channel == "ps_2":
	# 		bt_strip.toggle_plug(int(2))

	# 	elif channel == "ps_3":
	# 		bt_strip.toggle_plug(int(3))

	# 	elif channel == "ps_4":
	# 		bt_strip.toggle_plug(int(4))

	return redirect('/power_strip')


@app.route('/settings', methods=['GET', 'POST'])
def settings():
	if request.method == "POST":
		req = request.form.get('cities')
		city = ""

		for r in req:
			city+=r

		current_city = city
		settings = None
		with open(f"{DIR_PATH}/settings.json", "r") as f:
			settings = json.load(f)
			settings["city"] = city.strip("'")

			if settings != None:
				with open(f"{DIR_PATH}/settings.json", "w+") as f:
					json.dump(settings, f)
	        	     	
	return render_template('settings.html',  current_track=current_track, cities=cities)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')