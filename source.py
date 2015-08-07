import RPi.GPIO as GPIO
import MySQLdb as mdb
import sys
import time
import datetime

#This part of the code makes the connection to the mySQL database. This database
#needs to be created already through the command line.
con = mdb.connect('localhost','janbrett','test623','sensordb');
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#These variables represent different quantities related to the code:
#beepDistance = the distance in inches you want the sensor to act upon the
#buzzer.
#prox = the range sensor's GPIO pin on the pi
#buzzer = the buzzer's GPIO pin on the pi
#printdb = the determinant that lets the code know when to push data to the
#database
beepDistance = 36
prox = 4
buzzer = 17
printdb = True

#This part uses the connection to recreate the Alert data table inside the
#sensordb database.
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Alert")
    cur.execute("CREATE TABLE Alert(Id INT PRIMARY KEY AUTO_INCREMENT, \
                Time CHAR(20))")

#This is where the magic happens! THis infinite loop insures that it's
#continuously running
while 1:

    #Sets the pin modes for the range sensor and buzzer. This means your setting
    #up your pins to only be able to output a signal.
    GPIO.setup(prox, GPIO.OUT)
    GPIO.setup(buzzer, GPIO.OUT)
    #Gives it a little time before sending out a signal
    time.sleep(0.000002)
    #Outputs the sound wave for the range sensor
    GPIO.output(prox,1)
    #Gives it a little time before sending out a signal
    time.sleep(0.000005)
    #Stops the sound wave from being sent
    GPIO.output(prox,0)

    #Sets the range sensor to be able to take in a signal
    GPIO.setup(prox, GPIO.IN)

    #This part measures the time that the range sensor is
    #taking in data and also outputting data
    while GPIO.input(prox) == 0:
        start = time.time()
    while GPIO.input(prox) == 1:
        end=time.time()

    #This part calculates the distance in inches according to the time it took
    #the signal to return to the sensor.
    distance = (end-start) * (17150/2.54)
    distance = round(distance, 2)

    #This if statement determines if the distance will cause the buzzer to sound.
    if (distance < beepDistance):
        if(printdb):
            #Makes the buzzer sound
            GPIO.output(buzzer, 1)
            #Using the connection to the database, it logs the moment in time
            #where the code calculated the desired distance or less.
            with con:
                moment = time.time()
                st = datetime.datetime.fromtimestamp(moment).strftime('%m-%d-%Y %H:%M:%S')
                cur.execute("INSERT INTO Alert(Time) VALUES(%s)",st)

        #Gives the pi a little time before turning off the buzzer
        time.sleep(.5)
        GPIO.output(buzzer, 0)
        #Stops the database from receiving more information
        printdb = False

    #This else statement makes sure that the buzzer does not sound when
    #the calculated distance is equal or greater than the minimum buzzer
    #distance.
    else:
        GPIO.output(buzzer, 0)
        printdb = True
