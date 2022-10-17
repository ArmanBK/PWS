#the combined script for the pico w's, containing a webserver, communication with the  ICM 20948 over I2C and reading out the pots
import machine

#####Constants######


#Registers

regBank = 0x7F
deviceID = 0xEA
######settings#######

#I2C Address of the  ICM-20948
IMU = 0x69 #alternatively 0x68 if the fuse on the back is shorted

#innit pins for the I2C connection, frequency in herz
i2c = machine.I2C(0, scl = machine.Pin(1), sda = machine.Pin(0), freq = 40000)

#####Functions#####

def ReadReg(i2c, devAddr, regAddr, nBytes=1):
        data = i2c.readfrom_mem(devAddr, regAddr, nBytes)
        return data

def WriteReg(i2c, devAddr, regAddr, data):
        convData = bytearray()
        convData.append(data)
        i2c.writeto_mem(devAddr, regAddr, convData)

#single regAddr has multiple functionalities, therefore 4 user banks exist,
def SetBank(i2c, bank):
        if bank > 3:
                print('invalid bank id')

        bank = ((bank << 4) & 0b11000) #add 4 zero's after bank val for wri>         i2c.writeto_mem(devAddr, regAddr, bank)




######Main Code######
realAddr = ReadReg(i2c, IMU, 0x00)
if (realAddr != bytearray((deviceID,))):
    print('communication not established, device id is', realAddr, 'and should be', deviceID)
