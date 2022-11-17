#the combined script for the pico w's, containing a webserver, communication with the  ICM 20948 over I2C and reading out the pots
import network
import time
import struct
from machine import Pin
from umqtt.simple import MQTTClient

#####Constants######
deviceID = 0xEA
regBank = 0x7F

mqtt_server = 'test.mosquitto.org'
client_id = 'armankoc'
topic_sub = b'TomsHardware'

########WIFI#########
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Nokia","HiGithub")
time.sleep(5)
print(wlan.isconnected())

######settings#######
#I2C Address of the  ICM-20948
IMU = 0x69 #alternatively 0x68 if the fuse on the back is shorted

#innit pins for the I2C connection, frequency in herz
i2c = machine.I2C(0, scl = machine.Pin(1), sda = machine.Pin(0), freq = 40000)

#####Functions#####
#WiFi
def sub_cb(topic, msg):
    print("New message on topic {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    if msg == "on":
        LED.on()
    elif msg == "off":
        LED.off()

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=60)
    client.set_callback(sub_cb)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

#sensor
def ToSignedInt(unsigned):

    if unsigned > 32767:
        unsigned -= 65536
    return unsigned



def ReadReg(regAddr, nBytes):

        if nBytes <1:
            return bytearray()
        time.sleep(0.001)
        data = i2c.readfrom_mem(IMU, regAddr, nBytes)
        #print('d =', data)
        return data

def WriteReg(regAddr, data):
        convData = bytearray()
        convData.append(data)
        time.sleep(0.0001)

        i2c.writeto_mem(IMU, regAddr, convData)

    #single regAddr has multiple functionalities, therefore 4 user banks exist,
def SetBank(i2c, bank):
        if bank > 3:
                print('invalid bank id')

        bank = ((bank << 4)) #add 4 zero's after bank val for wri>         i2c.writeto_mem(devAddr, regAddr, bank)
        WriteReg(regBank, bank)



######Main Code######          
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

realAddr = ReadReg(0x00, 1)
if (realAddr != bytearray((deviceID,))):
    print('communication not established, device id is', realAddr, 'and should be', deviceID)




SetBank(i2c, 0)

time.sleep(0.1)
WriteReg(0x06, 0x01) #slaapstand uitzetten; standaard aan


time.sleep(0.1)
ReadReg(0x05, 1) #sens stand lezen
time.sleep(0.1)
WriteReg(0x05, 0x38) #sensors aanzetten
time.sleep(0.1)
ReadReg(0x05, 1) #sens stand lezen
time.sleep(0.1)

SetBank(i2c, 2)
time.sleep(0.1)
WriteReg(0x01, 0x01)#set gyro snelheid
time.sleep(0.0)
print('gyrosnelheid',ReadReg(0x01, 1))
time.sleep(0.1)
WriteReg(0x14, 0x01)#accel config
time.sleep(0.0)
print('accelsnelheid',ReadReg(0x14, 1))
time.sleep(0.1)
SetBank(i2c, 0)
time.sleep(0.1)

#sensors lezen
while True:
    time.sleep(0.1)
    block = ReadReg(0x2D, 12)
    
    
    axr = ((block[0]<<8) | (block[1] & 0xFF))
    ayr = ((block[2]<<8) | (block[3] & 0xFF))
    azr = ((block[4]<<8) | (block[5] & 0xFF))

    
    gxr = ((block[6]<<8) | (block[7] & 0xFF))
    gyr = ((block[8]<<8) | (block[9] & 0xFF))
    gzr = ((block[10]<<8) | (block[11] & 0xFF))


    axr = ToSignedInt(axr)
    ayr = ToSignedInt(ayr)
    azr = ToSignedInt(azr)
    gxr = ToSignedInt(gxr)
    gyr = ToSignedInt(gyr)
    gzr = ToSignedInt(gzr)

    gx = gxr / 250
    gy = gyr / 250
    gz = gzr / 250
    
    ax = axr/2
    ay = ayr/2
    az = azr/2
    
    print('gx', gx)
    print('gy', gy)
    print('gz', gz)
    combinedData = str(gx) + "_" + str(gy) + "_" + str(gz)
    client.publish(b"arman", combinedData.encode("UTF-8"))
    time.sleep(1)
time.sleep(0.1)
SetBank(i2c, 0)








