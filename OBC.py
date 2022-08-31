#Librerias importadas control sensores
import smbus#Libreria de i2c
import bmpsensor#Libreria BMP180 altura, presiones, temperatura
import time
import math
import Adafruit_ADS1x15#Libreria convertor analogico digital
import serial
##############################################
#Control de sensor MPU6050
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
    value = ((high << 8) | low)
        
        #to get signed value from mpu6050
    if(value > 32768):
            value = value - 65536
    return value
############################################

#Control de Bus i2c
bus = smbus.SMBus(1)
#Direccion de MPU6050
Device_Address = 0x68   
MPU_Init()
#Control de adc115
adc = Adafruit_ADS1x15.ADS1115()
#Ganancia de voltaje de salida
#  -   4 = +/-1.024V
GAIN = 4

temp, pressure, altura_inicial = bmpsensor.readBmp180()
print(altura_inicial)
while True:
    #Lectura de los Valores del acelerometro
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    #Lectura de los valores del bmp180
    temp, pressure, altitude = bmpsensor.readBmp180()
    altura_sns = altitude - altura_inicial
    
    #Lectura del valor en m/s2
    Ax = acc_x/1670.1325
    Ay = acc_y/1670.1325
    Az = acc_z/1670.1325
    AT = math.sqrt(pow(Ax,2)+pow(Ay,2)+pow(Az,2))
    
    #Lectura de los valores de Sensor de Gas
    NO2 = (10)(adc.read_adc(0, gain=GAIN)(0.512/32767))
    NH3 = (100)(adc.read_adc(1, gain=GAIN)(0.512/32767))
    C0 = (1000)(adc.read_adc(2, gain=GAIN)(0.512/32767))
        
#Impresion de valores
    print ("Ax=%.4f " %Ax, "Ay=%.4f " %Ay, "Az=%.4f " %Az)
    print ("AT=%.4f " %AT)
    print("Temperature is ",temp)
    print("Pressure is ",pressure)
    print("Altitude is ",altitude)
    print("Altura SNS = %.4f" %altura_sns)
    print("N02=%.4f ppm " %NO2, "NH3=%.4f ppm " %NH3, "C0=%.4f ppm " %C0)
    
    mensaje = str(("%.4f "%Ax)) + str(("%.4f "%Ay)) + str(("%.4f "%Az)) + str(("%.4f "%AT)) + str(temp) + str((" %d "%pressure)) + str(("%.2f "%altitude)) + str(("%.2f "%altura_sns)) + str(("%.4f "%NO2)) + str(("%.4f "%NH3)) + str(("%.4f "%C0))
    print(mensaje)
#   PROGRAMA PARA EL COORDINADOR

    #Aqui van los datos fijos

    direcciones = {'Charly':[0x00,0x13,0xA2,0x00,0x41,0x02,0x01,0x49]}
    inicio = 0x7E
    Cadena1 = [0x00,0x01]
    Cadena2 = 0x00
    n = 'Charly'
    mac = direcciones[n]

    #Aqui va la longitud

    Tamanio = len(mensaje)+14 #El # de letras del mensaje + 14 espacios
    Lenght1 = int(Tamanio/255)
    Lenght2 = (Tamanio%255)-3

    #Aqui vamos a calcular el checksum
    m = list(mensaje)

    m1 = []

    for i in m:
                
        m1.append(ord(i))

    mac.append(Cadena2)
    #Aqui juntamos las cadenas y las sumamos.

    f1 = Cadena1+mac+m1

    chksm = 0 #Iniciamos la variable del cheksum en 0

    for h in f1:
        chksm = chksm+h
        
    chksm &= 0xFF
    chksm = 0xFF - chksm

    #print(inicio)
    #print(Lenght1)
    #print(Lenght2)
    #print(f1)
    #print(chksm)

    Final = [inicio,Lenght1,Lenght2]+f1+[chksm]
    print(Final)

    xbee = serial.Serial("/dev/ttyUSB0", 9600)

    for w in Final:
        r = w.to_bytes(1,'big')
        xbee.write(r)
        print(r)

    xbee.close()

#Tiempo de Lectura
    time.sleep(1)
