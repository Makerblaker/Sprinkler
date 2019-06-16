#!/usr/bin/python3
from threading import Thread
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
Sensor = True

#Is it currently raining
isRaining = False

def setup():
	global serversocket,t

	# Setup GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(True)

	# Input Cancel Button
	GPIO.setup(CancelButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	# Input Rain Sensor
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
	addLog("System", "Main Thread started")
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
		# Is it raining
		if(isRaining == False):
			# Turn off LED if it was raining
			statusLED("off")

			# What was the command?
			if(requestType[0] == "ZONE"):
				# Turn on zone
				zone(int(requestType[1]), "ON")

				# Sleep for that amount
				sleep(int(requestType[2]) * 60)

				# Turn off zone
				zone(int(requestType[1]), "OFF")
			elif(requestType[0] == "QUIT"):
				destroy()
		else:
			while isRaining:
				statusLED("blink")
				rain()
				sleep(2)


# Zone Control Setup
def zone(zoneSelect, onoff):
	if(onoff == "ON"):
		GPIO.output(Zones[zoneSelect], 0)
		addLog('Zone ' + str(zoneSelect), 'ON')
	else:
		GPIO.output(Zones[zoneSelect], 1)
		addLog('Zone ' + str(zoneSelect), 'OFF')

def rain():
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
	for i in Zones:
		GPIO.output(i, GPIO.LOW)
	GPIO.output(StatusLED, GPIO.LOW)
	addLog('System', 'Sprinkler Script OFF')
	sleep(2)

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
