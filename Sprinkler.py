#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
from time import sleep
from sys import exit
import datetime
import MySQLdb
import thread

sleep(10)

# Set GPIO output points
Zones = [17, 27, 22, 23]
StatusLED = 12

# Set GPIO input points
CancelButton = 4
WaterSensor = 18

# Set Start time
startTime = '12:24:00'.split(':')

# Set Duration for each zone HH:MM:SS 
durationTime = '00:30:00'

# Set odd or even (even = True or odd = False)
iseven = True

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(True)
	
	# Input Cancel Button
	GPIO.setup(CancelButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
	# Input Rain Sensor
	GPIO.setup(WaterSensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
	# Setup 4 zones on GPIO
	# Turn all relays "OFF"
	for i in Zones:
		GPIO.setup(i, GPIO.OUT)
		GPIO.output(i, GPIO.HIGH)
	
	# Setup status LED
	GPIO.setup(StatusLED, GPIO.OUT)

# Zone Control Setup
def zone(zoneSelect, onoff):
	if zoneSelect == '1':
		if onoff == 'ON':
			GPIO.output(Zones[0], 0)
			#print 'Zone ' + zoneSelect + ' is ON'
			addLog('Zone ' + zoneSelect, 'ON')
		elif onoff == 'OFF': 
			GPIO.output(Zones[0], 1)
			addLog('Zone ' + zoneSelect, 'OFF')
	elif zoneSelect == '2':
		if onoff == 'ON':
			GPIO.output(Zones[1], 0)
			#print 'Zone ' + zoneSelect + ' is ON'
			addLog('Zone ' + zoneSelect, 'ON')
		elif onoff == 'OFF': 
			GPIO.output(Zones[1], 1)
			#print 'Zone ' + zoneSelect + ' is OFF'
			addLog('Zone ' + zoneSelect, 'OFF')
	elif zoneSelect == '3':
		if onoff == 'ON':
			GPIO.output(Zones[2], 0)
			#print 'Zone ' + zoneSelect + ' is ON'
			addLog('Zone ' + zoneSelect, 'ON')
		elif onoff == 'OFF': 
			GPIO.output(Zones[2], 1)
			#print 'Zone ' + zoneSelect + ' is OFF'
			addLog('Zone ' + zoneSelect, 'OFF')
	elif zoneSelect == '4':
		if onoff == 'ON':
			GPIO.output(Zones[3], 0)
			#print 'Zone ' + zoneSelect + ' is ON'
			addLog('Zone ' + zoneSelect, 'ON')
		elif onoff == 'OFF': 
			GPIO.output(Zones[3], 1)
			#print 'Zone ' + zoneSelect + ' is OFF'
			addLog('Zone ' + zoneSelect, 'OFF')
	
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
		
def water():
	
	# Convert people time to seconds
	duration = time.strptime(durationTime,'%H:%M:%S')
	totalDuration = datetime.timedelta(hours=duration.tm_hour,minutes=duration.tm_min,seconds=duration.tm_sec).total_seconds()
	
	zone('1', 'ON')
	sleep(totalDuration)
	zone('1', 'OFF')
	sleep(2)
	
	zone('2', 'ON')
	sleep(totalDuration)
	zone('2', 'OFF')
	sleep(2)
	
	zone('3', 'ON')
	sleep(totalDuration)
	zone('3', 'OFF')
	sleep(2)
	
	zone('4', 'ON')
	sleep(totalDuration)
	zone('4', 'OFF')
	sleep(2)
	
def addLog(currentZone, addedText):
	print time.strftime("%x %X") + ": " + currentZone + ": " + addedText
	try:
		thread.start_new_thread( dbLog, (currentZone, addedText, ) )
	except:
		print ("Error: unable to start thread")
	
# Add log to database
# Seperated so we can run this in another Thread
def dbLog(currentZone, addedText):
	
	# Connect to database
	db = MySQLdb.connect(host="192.168.1.2",    # your host, usually localhost
                     user="Sprinkler",        	# your username
                     passwd="Sprinkler",  		# your password
                     db="Sprinkler")        	# name of the data base
	cur = db.cursor()
	
	# Use all the SQL you like
	cur.execute("INSERT INTO sprinkler.tbllogs (zone, description) VALUES (\"" + currentZone + "\", \"" + addedText + "\")")
	db.commit()
	cur.close()
	db.close()
	
def mainRun():
	while True:
		#sleep(5)
		Watering = False

		# Has the time been met?
		currentTime = time.strftime("%X").split(':')
		if (currentTime[0] == startTime[0]) and (currentTime[1] == startTime[1]) and (currentTime[2] == startTime[2]):
			if iseven:
				if int(time.strftime("%d")) % 2 == 0:
					Watering = True
			
		# Has the Cancel button been pressed?
		if GPIO.input(CancelButton):
			addLog('System', 'Cancel Button ON')
			active = True
			while active:
				sleep(2)
				statusLED("blink")
				
				# If button position changes, continue
				if GPIO.input(CancelButton) == False:
					active = False
					addLog('System', 'Cancel Button OFF')
		
		# Is the water sensor tripped?
		if GPIO.input(WaterSensor):
			addLog('System', 'Water Sensor is ON')
			active = True
			while active:
				sleep(2)
				statusLED('solid')
				
				# If button position changes, continue
				if GPIO.input(WaterSensor) == False:
					active = False
					statusLED('off')
					addLog('System', 'Water Sensor is OFF')
		
		# Start Watering
		if Watering:
			addLog("System", "Watering")
			water()
			addLog("System", "Watering Complete")
		else:
			sleep(10)
def destroy():
	for i in Zones:
		GPIO.output(i, GPIO.LOW)
		
	GPIO.output(StatusLED, GPIO.LOW)
	GPIO.cleanup()
	addLog('System', 'Sprinkler Script OFF')
	sleep(2)

if __name__ == '__main__':
    setup()
    try:
        mainRun()
    except KeyboardInterrupt:
        destroy()
