from machine import UART, Pin
import time

def wait():
    time.sleep(0.1)
    print("..", end="")
    

#Waveshare Pico_ETH_CH9121 GPIO pins in use: 0, 1, 14, 17, GND & VSYS power (also 4 & 5 if UART1 enabled at x39)

CFG = Pin(14, Pin.OUT,Pin.PULL_UP) #CH9121 configuration pin, 0 to config, 1 to exit
RST = Pin(17, Pin.OUT,Pin.PULL_UP) #CH9121 external reset input pin, low active
RST.value(1) #CH9121 external reset input pin 17, (0 active, 1 inactive)
uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)) #configuration commands required to be sent at a fixed rate of 9600 baud on UART0 only

chmode = ["TCP Server", "TCP Client", "UDP Server", "UDP Client"]
spsettings = ["Even", "Odd", "Mark", "Space", "None"]

print("Reading CH9121..", end="")
CFG.value(0) #CH9121 configuration pin 14, 0 to config, 1 to exit
wait()
x=uart0.read(uart0.any()) #clear the data

#CH9121 network settings
uart0.write(b'\x57\xab\x60') #1 byte reply uart0 working mode
wait()
uart0.write(b'\x57\xab\x61') #4 bytes reply uart0 local IP
wait()
uart0.write(b'\x57\xab\x62') #4 bytes reply uart0 subnet mask
wait()
uart0.write(b'\x57\xab\x63') #4 bytes reply uart0 ch9121 gateway
wait()
uart0.write(b'\x57\xab\x64') #2 bytes reply uart0 local port
wait()
uart0.write(b'\x57\xab\x65') #4 bytes reply uart0 destination IP
wait()

#Default UART read buffer is 64 bites, so reading periodically
x=uart0.read(uart0.any())
u0mode = chmode[x[0]]
ch9121localip = str(x[1])+"."+str(x[2])+"."+str(x[3])+"."+str(x[4])
ch9121subnet = str(x[5])+"."+str(x[6])+"."+str(x[7])+"."+str(x[8])
ch9121gateway = str(x[9])+"."+str(x[10])+"."+str(x[11])+"."+str(x[12])
word16bit = ((x[14] <<8) + x[13]) # Shift highbyte 8 bits to the left, then add lowbyte to obtain 16-bit 'bytes' object. Do them in reverse order to account for 'little'
u0localport = str((word16bit))
u0targetip = str(x[15])+"."+str(x[16])+"."+str(x[17])+"."+str(x[18])


uart0.write(b'\x57\xab\x66') #2 bytes reply uart0 target port
wait()
uart0.write(b'\x57\xab\x71') #4 bytes reply uart0 baud
wait()
uart0.write(b'\x57\xab\x72') #3 bytes reply uart0 serial parameters
wait()
uart0.write(b'\x57\xab\x73') #4 bytes reply uart0 timeout
wait()
uart0.write(b'\x57\xab\x81') #6 bytes reply CH9121 mac address
wait()
uart0.write(b'\x57\xab\x90') #1 byte reply uart1 mode
wait()

x=uart0.read(uart0.any())
word16bit = ((x[1] <<8) + x[0])
u0targetport = str(word16bit)
word64bit = ((x[5] <<24) + (x[4] <<16) + (x[3] <<8) + x[2])
u0baud = str(word64bit)
u0serialsettings = (str(x[6])+ " stop bit, " + "parity: " + spsettings[x[7]] + ", " + str(x[8]) + " data bits")
u0timeout = str(x[9]) + "*5 ms" 
ch9121mac = '%02x' % x[10] + ":" + '%02x' % x[11] + ":" + '%02x' % x[12] + ":" + '%02x' % x[13] + ":" + '%02x' % x[14] + ":" + '%02x' % x[15]
u1mode = chmode[x[16]]


uart0.write(b'\x57\xab\x91') #2 bytes reply uart1 local port
wait()
uart0.write(b'\x57\xab\x92') #4 bytes reply uart1 target IP
wait()
uart0.write(b'\x57\xab\x93') #2 bytes reply uart1 target port
wait()
uart0.write(b'\x57\xab\x94') #4 bytes reply uart1 baud
wait()
uart0.write(b'\x57\xab\x95') #3 bytes reply uart1 serial parameters
wait()
uart0.write(b'\x57\xab\x96') #1 byte reply uart1 timeout
wait()

x=uart0.read(uart0.any())
word16bit = ((x[1] <<8) + x[0])
u1localport = str((word16bit))
u1targetip = str(x[2])+"."+str(x[3])+"."+str(x[4])+"."+str(x[5])
word16bit = ((x[7] <<8) + x[6])
u1targetport = str(word16bit)
word64bit = ((x[11] <<24) + (x[10] <<16) + (x[9] <<8) + x[8])
u1baud = str(word64bit)
u1serialsettings = (str(x[12])+ " stop bit, " + "parity: " + spsettings[x[13]] + ", " + str(x[14]) + " data bits")
u1timeout = str(x[15]) + "*5 ms"


uart0.write(b'\x57\xab\x01') #1 byte reply CH9121 chip version number
wait()
uart0.write(b'\x57\xab\x03') #1 byte reply uart0 TCP client connection status? 
wait()
uart0.write(b'\x57\xab\x04') #1 byte reply uart1 TCP client connection status?
wait()
#uart0.write(b'\x57\xab\x67') #1 byte reply read number of reconnections
#wait()

x=uart0.read(uart0.any())
ch9121chipnum = str((x[0]))
u0connected = "TCP Disconnected"
u1connected = "TCP Disconnected"
if x[1]>0:
    u0connected = "TCP Connected"
if x[2]>0:
    u1connected = "TCP Connected"
#CH9121reconnections = str((x[3]))


#End Configuration Mode
uart0.write(b'\x57\xab\x5E') #Leave Serial port configuration mode
time.sleep(0.1)
CFG.value(1) #CH9121 configuration pin 14, 0 to config, 1 to exit


print("done")
time.sleep(0.2)

print()
print("CH9121 Chip version number: "+ch9121chipnum)
print("            CH9121 Gateway: "+ch9121gateway)
print("        CH9121 Subnet Mask: "+ch9121subnet)
print("           CH9121 Local IP: "+ch9121localip)
print("        CH9121 Mac Address: "+ch9121mac)
#print("      CH9121 reconnections: "+ch9121reconnections)
print()

print("                UART0 Mode: "+u0mode)
print("UART0 TCP Client Connected: "+u0connected)
print("           UART0 Target IP: "+u0targetip)
print("         UART0 Target Port: "+u0targetport)
print("          UART0 Local Port: "+u0localport)
print("    UART0 Serial Baud Rate: "+u0baud) 
print("     UART0 Serial Settings: "+u0serialsettings)
print("      UART0 Serial Timeout: "+u0timeout)
print()

print("                UART1 Mode: "+u1mode)
print("UART1 TCP Client Connected: "+u1connected)
print("           UART1 Target IP: "+u1targetip)
print("         UART1 Target Port: "+u1targetport)
print("          UART1 Local Port: "+u1localport)
print("    UART1 Serial Baud Rate: "+u1baud)
print("     UART1 Serial Settings: "+u1serialsettings)
print("      UART1 Serial Timeout: "+u1timeout)
print()
