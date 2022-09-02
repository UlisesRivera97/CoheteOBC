import serial 

xbee=serial.Serial("COM8", 9600)

direcciones = {'Charly_END':[0x00,0x13,0xA2,0x00,0x41,0x02,0x01,0x49]}  # de donde recibo
#"""
while True:
    
    print(xbee.read(93))

xbee.close()
