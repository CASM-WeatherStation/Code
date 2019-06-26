'''
receiveData.py

Mohamed Ebsim

Contact Jesse Rogerson, @ jrogerson@ingeniumcanada.org

Originally created on Jully 11, 2018
-------------------------------------

This program is made to read from the serial port and
decode it in order for future use. It currently saves
the data to a file for testing purposes and might
change as the project progresses.

'''

#Import Libraries
import serial
import time
import pymysql

#Setting up serial connection through port ACM0 with a rate of 9600 baud
ser = serial.Serial('/dev/ttyUSB0', 9600)    

# set basic values for the variables
temp = 0 # temperature
pres = 0 # pressure
altitude = 0 # altitude
sV = 0 # sensor Voltage (for the humidity sensor)
hum = 0 # relative humidity
truhum = 0 # true relative humidity
rain = 0 # amount of rain
speed = 0
gust = 0
direction = 0

#Setting up for use of MySQL database
username = "casm"
password = "planes"
databaseName = "temp_database"

database = pymysql.connect("localhost",username,password,databaseName)
cursor = database.cursor()

'''
This function has the job of recieving data from the serial port
and decoding it. Along with that it checks for significant changes
to the information in order to minimize relatively insignificant
changes to the data.
'''
def updateData():
    # bring the variables into the method
    global temp
    global pres
    global altitude
    global sV
    global hum
    global truhum
    global rain
    global speed
    global gust
    global direction
    
    # Reads data that is coming in
    data = ser.readline()
    
    # decodes it for use
    data = data.decode('utf-8')
    
    '''
    The following lines determine if the data that is coming in
    is of which type. It then removes the extra data until only
    the number remains. It then checks if it is a significant
    enough of a change to be worth changing the variable.
    '''
    #print(data)
    if data.startswith('Temperature = '): #14 characters long
        temp = float(data[14:-4])
    if data.startswith('Altitude = '): #11 characters long
        altitude = float(data[11:-9])
    if data.startswith('Pressure = '): #11 characters long
        pres = float(data[11:-6])
    if data.startswith('Sensor Voltage = '): #17 characters long
        sV = float(data[17:-4])
    if data.startswith('Relative Humidity = '): #19 characters long
        hum = float(data[19:-4])
    if data.startswith('True Relative Humidity = '): #24 characters long
        truhum = float(data[24:-4])
    
    if data.startswith('Rain Total = '): #13 characters long
        rain = float(data[13:])
    if data.startswith('Wind Speed = '): #13 characters long
        speed = float(data[13:-6])
    if data.startswith('Wind Gust = '): #12 characters long
        gust = float(data[12:-6])
    if data.startswith('Wind Direction = '): #17 characters long
        direction = float(data[17:])

x = 0

print("Running")

# This python program currently only runs 600 times.
while True:
    # Calls to update the data
    updateData()
    if(x % 6 == 0):
        #Finds time
        timeDate = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
        
        # Command to add to table "log" the data
        sql = ("""INSERT INTO finalLog (datetime, temperature, pressure, altitude, sensorVoltage, humidity, trueHumidity, rain, windSpeed, windGust, windDirection) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(timeDate,temp,pres,altitude,sV,hum,truhum,rain,speed,gust,direction))
        
        # Tries to run command and prints outcome
        try:
            print("Writing to database...")
            cursor.execute(*sql)
            database.commit()
            print("Write Complete")
        except:
            database.rollback()
            print("Failed writing to database")

            
          
    
    # Increases 50 until the loop breaks
    x+=1

# Closes/terminates variables for database
cursor.close()
database.close()

# Prints out the final data
print(temp)
print(pres)
print(altitude)
print(sV)
print(hum)
print(truhum)
