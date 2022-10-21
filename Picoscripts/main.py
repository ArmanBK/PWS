#the combined script for the pico w's, containing a webserver, communication with the  ICM 20948 over I2C and reading out the pots
import machine
import time
import struct

#####Constants######
#IDs
accID = (1 << 0)
gyrID = (1 << 1)
magID = (1 << 2)

deviceID = 0xEA

#Registers
regBank = 0x7F

#Options
 #accel ranges
gpm2 = 0x00
gpm4 = 0x01
gpm8 = 0x02
gpm16 = 0x03

 #gyro ranges
dps250 = 0x00
dps500 = 0x01
dps1000 = 0x02
dps2000 = 0x03

######settings#######

#I2C Address of the  ICM-20948
IMU = 0x69 #alternatively 0x68 if the fuse on the back is shorted

#innit pins for the I2C connection, frequency in herz
i2c = machine.I2C(0, scl = machine.Pin(1), sda = machine.Pin(0), freq = 40000)

#####Functions#####

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
WriteReg(0x14, 0x02)#set gyro snelheid
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
    print('ax', ax)
    print('ay', ay)
    print('az', az)

time.sleep(0.1)
SetBank(i2c, 0)







