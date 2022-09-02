
#   PROGRAMA PARA EL END - DEVICE (Recibe)

import serial 

# el ord recibe un carácter y regresa un entero unicode (ascii)
# Desde el ord # 9 inicia el mensaje, hasta tamanio

xbee=serial.Serial("COM4", 9600)

direcciones = {'Charly_END':[0x00,0x13,0xA2,0x00,0x41,0x5A,0x22,0xEC]}  # de donde recibo

while True:
    
    inicio = ord(xbee.read())
    
    length1 = ord(xbee.read())
    length2 = ord(xbee.read())
   
    #hasta aqui recuperamos los primeros 3 bytes 
   
    tamanio = length2 + 10 #longitud de toda la trama
    
    print('tamanio:', tamanio)
    
    basura = []    

    for i in range(5):
        
        p = ord(xbee.read())
        basura.append(p)
       
    #Hasta aqui recuperamos los siguientes 5 bytes de la trama, en total llevamos 8 byts recuperados    
    
    print('basura:', basura)
    
    resu = ""
     
    for l in basura:
         
        resu = resu + chr(l)
     
    print("String:", str(resu))
    
    restante = (tamanio - 14) -1 #tamanio del mensaje
    print('restante:', restante)
    
    # aqui empezamos a recuperar el mensaje, que son desde el byte 8 hasta "restante"
    
    trama_msj = []
   
    for j in range(restante): # recorremos los espacios que faltan hasta uno antes del checksum 

        r = ord(xbee.read())
        trama_msj.append(r)
        
    mensaje = ""
    
    for l in trama_msj:
        
        mensaje = mensaje + chr(l)
    
    print("String:", str(mensaje))
    
        #mensaje.append(bytes.fromhex('68656c6c6f').decode('utf-8'))
        
        #mensaje.append(hex(r).replace('x','')) # aqui le quito la 'x' a '0x00', pero no se como quitarle el primer 0, en realidad quiero quitar el '0x'
        #print('Mensaje:', hex(y))
        #print(f)
        
    #mensaje.append(str(0)) # le agrego un 0 al final para que codecs.decode decodifique un hex multiplo de 2.
    #lista = "".join(mensaje)
    #final = lista.decode("hex") no sirvio
    #binary_str = codecs.decode(lista, "hex")
    #print(str(binary_str,'utf-8'))
    #print(mensaje)
    
    
    
    
    chsk = ord(xbee.read()) #ultima parte de la trama
    
    #print('Mensaje:', byte_array)

xbee.close()

"""
while True:
    a=ord(xbee.read()) #0xFE Start delimiter
    if(a==0x7e):
        print("Inicio")
        l1=ord(xbee.read())
        print('a:',hex(a))
        print('l1',hex(l1))
        l2=ord(xbee.read())
        print('l2',hex(l2))
        tama= (l1+l2)-12 #entero de "dos bits de length y restamos - 12" Length - 12
        #posiblemente tengamos que restarle otro valor que no sea 12, tal vez 11 o 10
        
        typ = ord(xbee.read())
        ID = ord(xbee.read())
        
        ch1= typ + ID #01 Frame type + Frame ID
        print('typ',hex(typ))
        print('ID',hex(ID))
        
        mc=[]
        for i in range(8): #64 - bit dest. address
            p=ord(xbee.read())
            ch1=ch1+p #Frame type + Frame ID + Mac address
            mc.append(p)
            print(hex(p))
            
        ck1=ch1+ord(xbee.read()) #(Frame type + Frame ID + Mac address)ch1 + Options(00)  
        print('ya hasta hex')
        print(ck1)
        
        print('tama:')
        print(tama)
        
        msj=(xbee.read(tama)).decode("utf-8") # creo que: msj lee hasta el valor "tama" decodificado a utf-8
        
        print('xbee.read(tama):')
        print(xbee.read(tama))
        
        mensaje=[]
        
        for w in msj:
            r = w.to_bytes(1,'big')
            mesaje = mensaje[w]+r
        
        print(mensaje)
        
        
        for j in msj: 
            ch1=ch1+ord(j) #(Frame type + Frame ID + MAC) + mensaje
            #posiblemente no sea ch1, tal vez es ck1 para que sea: #Frame type + Frame ID + Mac address + Options(00) + mensaje  
            # y talves el for va de j hasta ck1, no se si sea bueno sacar el checksum sumando todo, como si lo fueramos a transmitir.
            
        ch1 &= 0xFF
        cf = 0xFF-ch1
        
        c=ord(xbee.read())
        
        print('Aqui esta en checksum')
        print(cf)
        print(c)
        
        if(c==cf):
            print("Correcto \n")
            print(msj)
        else:
            print("Vuelve a intentarlo \n")
            print(msj)

xbee.close()

"""
