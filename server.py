#!/usr/bin/python3
import _thread
import RPi.GPIO as GPIO
import socket
import time
from time import sleep
from sys import exit
import datetime
#import MySQLdb

# Start task command
# sleep 30 && python /home/pi/Scripts/Sprinkler/Sprinkler.py > /home/pi/Scripts/Sprinkler/log.txt 2>&1

# Set GPIO output points
Zones = [17, 27, 22, 23]
StatusLED = 12

# Set GPIO input points
CancelButton = 4
WaterSensor = 18

# Water Sensor Enabled?
Sensor = False

#Is it currently raining
isRaining = False

defaultWaitDuration = 0

def setup():
	global serversocket,t

	# Setup GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(True)

	# Input Cancel Button
	GPIO.setup(CancelButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	# Input Rain Sensor
	if Sensor:
		GPIO.setup(WaterSensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	# Setup 4 zones on GPIO
	# Turn all Zones "OFF"
	for i in Zones:
		GPIO.setup(i, GPIO.OUT)
		GPIO.output(i, GPIO.HIGH)

	# Setup status LED
	GPIO.setup(StatusLED, GPIO.OUT)

	# Setup Sockets
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	host = socket.gethostname()
	port = 9999

	serversocket.bind((host, port))
	serversocket.listen(5)

	addLog("System", "Setup complete")
	
def mainRun():
	global isRaining
	addLog("System", "Main Thread started")
	 
	 # Always check the switch
	_thread.start_new_thread(checkSwitch, ((),))
	
	while True:
		global serversocket

		clientsocket,addr = serversocket.accept()

		fromClient = clientsocket.recv(1024)
		clientsocket.close()
		strFromClient = str(fromClient.decode("ascii"))
		addLog("Recived", strFromClient)

		# Split incoming message
		requestType = strFromClient.split(":")
		
		# Do something with that message
		# What was the command?
		if(requestType[0] == "WATER"):
			
			# Is it raining
			if(isRaining == False):
				# Turn off LED if it was raining
				statusLED("off")
				# Start watering
				_thread.start_new_thread(water, (requestType[1], requestType[2], ) )
				
		elif(requestType[0] == "ZONE"):
			if(requestType[1] == "ON"):
				zone(int(requestType[2]), "ON")
			else:
				zone(int(requestType[2]), "OFF")
				
		elif(requestType[0] == "RainStatus"):
			# Some day we will send something back
			print("nothing")
			
		elif(requestType[0] == "QUIT"):
			destroy()
			
# Check switch
def checkSwitch(self):
	global isRaining
	
	while True:
		state = GPIO.input(CancelButton)
		if(state):
			if(state != isRaining):
				addLog("System", "Switch TRUE")
				statusLED("solid")
				isRaining = True
		else:
			if(state != isRaining):
				addLog("System", "Switch FALSE")
				statusLED("off")
				isRaining = False
		sleep(2)
	
# Water the lawn
def water(zoneNum, duration):
	# Turn on zone
	zone(int(zoneNum), "ON")
	statusLED("on")
	
	# Sleep for that amount
	sleep(int(duration) * 60)
	
	# Turn off zone
	zone(int(zoneNum), "OFF")
	statusLED("off")
	
# Zone Control Setup
def zone(zoneSelect, onoff):
	if(onoff == "ON"):
		GPIO.output(Zones[zoneSelect], 0)
		addLog('Zone ' + str(zoneSelect), 'ON')
	else:
		GPIO.output(Zones[zoneSelect], 1)
		addLog('Zone ' + str(zoneSelect), 'OFF')

def rain():
	global isRaining
	# Check if it's raining
	if Sensor:
		if GPIO.input(WaterSensor):
			isRaining = True
		else:
			isRaining = False

def statusLED(status):
	if status == "blink":
		GPIO.output(StatusLED, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(StatusLED, GPIO.LOW)
		sleep(0.5)
	elif status == "solid":
		GPIO.output(StatusLED, GPIO.HIGH)
	elif status == "off":
		GPIO.output(StatusLED, GPIO.LOW)

def addLog(currentZone, addedText):
	now = datetime.datetime.now()
	print ("{0}: {1}: {2}".format(now, currentZone, addedText))

def destroy():
	global serversocket
	serversocket.shutdown(socket.SHUT_RDWR)
	
	for i in Zones:
		GPIO.output(i, GPIO.LOW)
	GPIO.output(StatusLED, GPIO.LOW)
	addLog('System', 'Sprinkler Script OFF')
	exit()

if __name__ == '__main__':
	setup()
	try:
		mainRun()
	except KeyboardInterrupt:
		destroy()
	finally:
		GPIO.cleanup()
		exit()
else:
	destroy()
