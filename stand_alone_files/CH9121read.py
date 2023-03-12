"""Add this file to the Pico /lib directory"""
"""Modify to your network settings in the constants below"""
"""Add 'import CH9121read' to main.py to read on boot"""

#Waveshare Pico_ETH_CH9121 
#Waveshare 2-Ch Uart to Eth
#GPIO pins in use: 0, 1, 14, 17, GND & VSYS power (also 4 & 5 if UART1 enabled)


from machine import UART, Pin
from time import sleep
   
def cmd(i):
    uart0.write(b'\x57\xab'+i)
    sleep(.2)
    print("..", end="")
    
ethfile = "CH9121config.txt" #The file which will contain a copy of the read on the Pico
    
CFG = Pin(14, Pin.OUT,Pin.PULL_UP) #CH9121 configuration pin, 0 to config, 1 to exit
RST = Pin(17, Pin.OUT,Pin.PULL_UP) #CH9121 external reset input pin, low active
RST.value(1) #CH9121 external reset input pin 17, (0 active, 1 inactive)

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)) #configuration commands required to be sent at a fixed rate of 9600 baud on UART0 only

chmode     = ["TCP Server", "TCP Client", "UDP Server", "UDP Client"]
spsettings = ["Even", "Odd", "Mark", "Space", "None"]

print("Reading CH9121..", end="")
CFG.value(0) #CH9121 configuration pin 14, 0 to config, 1 to exit
sleep(.1)
x=uart0.read(uart0.any()) #clear the data

#CH9121 network settings
cmd(b'\x60')     #1 byte reply for uart0 working mode
cmd(b'\x61')     #4 bytes reply for CH9121 local IP
cmd(b'\x62')     #4 bytes reply for CH9121 subnet mask
cmd(b'\x63')     #4 bytes reply for CH9121 gateway
cmd(b'\x64')     #2 bytes reply for uart0 local port
cmd(b'\x65')     #4 bytes reply for uart0 destination IP

#Default Pico UART read buffer is 64 bites, so reading & recording periodically
x=uart0.read(uart0.any())
u0mode = chmode[x[0]]
ch9121localip    = f"{x[1]}.{x[2]}.{x[3]}.{x[4]}"
ch9121subnet     = f"{x[5]}.{x[6]}.{x[7]}.{x[8]}"
ch9121gateway    = f"{x[9]}.{x[10]}.{x[11]}.{x[12]}"
u0localport      = f"{(x[14] <<8) + x[13]}"
# for all Ports shift highbyte 8 bits to the left, then add lowbyte to obtain 16-bit 'bytes' object. Doing them in reverse order to account for 'little'
u0targetip       = f"{x[15]}.{x[16]}.{x[17]}.{x[18]}"

cmd(b'\x66')     #2 bytes reply for uart0 target port
cmd(b'\x71')     #4 bytes reply for uart0 baud
cmd(b'\x72')     #3 bytes reply for uart0 serial parameters
cmd(b'\x73')     #4 bytes reply for uart0 timeout
cmd(b'\x81')     #6 bytes reply for CH9121 mac address
cmd(b'\x90')     #1 byte reply for uart1 mode

x=uart0.read(uart0.any())
u0targetport     = f"{(x[1] <<8) + x[0]}"
u0baud           = f"{(x[5] <<24) + (x[4] <<16) + (x[3] <<8) + x[2]}"
# For all bauds shift highbyte 24 bits to the left. Shift 3rd byte 16 to the left. Shift 2nd byte 8 to the left. Then add lowbyte to obtain 64-bit 'bytes' object. Doing them in reverse order to account for 'little'
u0serialsettings = f"data bits={x[8]}, parity={spsettings[x[7]]}, stop bit={x[6]}"
u0timeout        = f"{x[9] * 5} ms" 
ch9121mac        = f"{'%02x' % x[10]}:{'%02x' % x[11]}:{'%02x' % x[12]}:{'%02x' % x[13]}:{'%02x' % x[14]}:{'%02x' % x[15]}"
u1mode           = chmode[x[16]]

cmd(b'\x91')     #2 bytes reply for uart1 local port
cmd(b'\x92')     #4 bytes reply for uart1 target IP
cmd(b'\x93')     #2 bytes reply for uart1 target port
cmd(b'\x94')     #4 bytes reply for uart1 baud
cmd(b'\x95')     #3 bytes reply for uart1 serial parameters
cmd(b'\x96')     #1 byte reply for uart1 timeout

x=uart0.read(uart0.any())
u1localport      = f"{(x[1] <<8) + x[0]}"
u1targetip       = f"{x[2]}.{x[3]}.{x[4]}.{x[5]}"
u1targetport     = f"{(x[7] <<8) + x[6]}"
u1baud           = f"{(x[11] <<24) + (x[10] <<16) + (x[9] <<8) + x[8]}"
u1serialsettings = f"data bits={x[14]}, parity={spsettings[x[13]]}, stop bit={x[12]}"
u1timeout        = f"{x[15] * 5} ms"

cmd(b'\x01')     #1 byte reply for CH9121 chip version number
cmd(b'\x03')     #1 byte reply for uart0 TCP client connection status? 
cmd(b'\x04')     #1 byte reply for uart1 TCP client connection status?
cmd(b'\x67')     #1 byte reply for reading number of reconnections

x=uart0.read(uart0.any())
ch9121chipnum    = f"{x[0]}"
u0connected      = "TCP Disconnected"
u1connected      = "TCP Disconnected"
if x[1]>0:
    u0connected  = "TCP Connected"
if x[2]>0:
    u1connected  = "TCP Connected"
if u0mode != chmode[0] and u0mode != chmode[1]:
    u0connected  = "Not in TCP Mode"
if u1mode != chmode[0] and u1mode != chmode[1]:
    u1connected  = "Not in TCP Mode"
ch9121reconn     = f"{x[3]}"
    
#End Configuration Mode
cmd(b'\x5E') #Leave Serial port configuration mode
CFG.value(1) #CH9121 configuration pin 14, 0 to config, 1 to exit
print("done")
        
"""Display of readings"""
            
file = open(ethfile, 'w') # Open File: Write "w", Append "a", Read "r", Read-Write "r+"
file.close()
            
def report(txt=""):
    print(txt)
    with open(ethfile, 'a') as file: # Open File: Write "w", Append "a", Read "r", Read-Write "r+"
        file.write(txt + "\r\n")
        file.close()    
                 
report()
report(f"               *CH9121 General Settings*")
report(f"       CH9121 Chip Version: {ch9121chipnum}")
report(f"        CH9121 Mac Address: {ch9121mac}")
report(f"            CH9121 Gateway: {ch9121gateway}")
report(f"        CH9121 Subnet Mask: {ch9121subnet}")
report(f"           CH9121 Local IP: {ch9121localip}")
report(f"    Ethernet Reconnections: {ch9121reconn}")
report()

report(f"                *CH9121 UART0 Settings*")
report(f"                UART0 Mode: {u0mode}")
report(f"          UART0 TCP Status: {u0connected}")
report(f"           UART0 Target IP: {u0targetip}")
report(f"         UART0 Target Port: {u0targetport}")
report(f"          UART0 Local Port: {u0localport}")
report(f"    UART0 Serial Baud Rate: {u0baud}") 
report(f"     UART0 Serial Settings: {u0serialsettings}")
report(f"      UART0 Serial Timeout: {u0timeout}")
report()
        
uart0 = UART(0, baudrate=int(u0baud), tx=Pin(0), rx=Pin(1), timeout = 10, timeout_char = 10) 
report(f"                 *Pico UART0 Settings*")
report(f"{uart0}")
report()        
        
report(f"           *CH9121 UART1 Settings if enabled*")
report(f"                UART1 Mode: {u1mode}")
report(f"          UART1 TCP Status: {u1connected}")
report(f"           UART1 Target IP: {u1targetip}")
report(f"         UART1 Target Port: {u1targetport}")
report(f"          UART1 Local Port: {u1localport}")
report(f"    UART1 Serial Baud Rate: {u1baud}")
report(f"     UART1 Serial Settings: {u1serialsettings}")
report(f"      UART1 Serial Timeout: {u1timeout}")
report()
        
uart1 = UART(1, baudrate=int(u1baud), tx=Pin(4), rx=Pin(5), timeout=10, timeout_char=10)
report(f"                 *Pico UART1 Settings*")
report(f"{uart1}")
report()
        
print("")
print(f"CH9121 settings written to: {ethfile}.")
#END CH9121read.py    

