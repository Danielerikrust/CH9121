from machine import UART, Pin
from time import sleep

def wait():
    sleep(0.1)
    print("..", end="")
    
    
#Waveshare Pico_ETH_CH9121 
#Waveshare 2-Ch Uart to Eth
#GPIO pins in use: 0, 1, 14, 17, GND & VSYS power (also 4 & 5 if UART1 enabled)

CFG = Pin(14, Pin.OUT,Pin.PULL_UP) #CH9121 configuration pin, 0 to config, 1 to exit
RST = Pin(17, Pin.OUT,Pin.PULL_UP) #CH9121 external reset input pin, low active
RST.value(1) #CH9121 external reset input pin 17, (0 active, 1 inactive)
uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)) #configuration commands required to be sent at a fixed rate of 9600 baud on UART0 only

#Variables specific to CH9121 hat
GATEWAY = (192,168,1,1)             # GATEWAY / Router for LAN
SUBNET_MASK = (255,255,255,0)       # SUBNET_MASK for LAN
LOCAL_IP = (192,168,1,200)          # LOCAL_IP of CH9121 on LAN
#DEVICE_NAME = b'name.com'          # DOMAIN_NAME of CH9121 IP, replace name.com

#Variables specific to UART0 serial port
UART0_MODE = 1                      # Mode 0:TCP Server, Mode 1:TCP Client, Mode 2:UDP Server, Mode 3:UDP Client
UART0_TARGET_IP = (192,168,1,100)   # TARGET_IP of destination
UART0_TARGET_PORT = 1000            # TARGET_PORT of destination
UART0_LOCAL_PORT = 2000             # LOCAL_PORT of UART0, each uart shares local IP but has a unique port, maximum 65535
UART0_BAUD_RATE = 115200            # BAUD_RATE of UART0 serial Port 

#Variables specific to UART1 serial port - UART1 disabled by default
UART1_MODE = 3                      # Mode 0:TCP Server, Mode 1:TCP Client, Mode 2:UDP Server, Mode 3:UDP Client
UART1_TARGET_IP = (192,168,1,150)    # TARGET_IP of destination
UART1_TARGET_PORT = 3000            # TARGET_PORT of destination
UART1_LOCAL_PORT = 6000             # LOCAL_PORT of UART1, each uart shares local IP but has a unique port, maximum 65535
UART1_BAUD_RATE = 115200            # BAUD_RATE of UART1 serial port


#Use the following UART settings with PICO_ETH_CH9121 outside of this configuration file:
    #uart0 = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1)) #uart0 baud=115200, data bits=8, parity=None, stop bit=1
    #uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5)) #uart1 baud=115200, data bits=8, parity=None, stop bit=1  #if enabled at \x39

NO = b'\x00'
YES = b'\x01'

print("Updating CH9121", end="")
CFG.value(0) #CH9121 configuration pin 14, 0 to config, 1 to exit
wait()

#Global network settings for CH9121
uart0.write(b'\x57\xab\x11'+bytes(bytearray(LOCAL_IP))) #CH9121 local IP
wait()
uart0.write(b'\x57\xab\x12'+bytes(bytearray(SUBNET_MASK))) #CH9121 set subnet mask
wait()
uart0.write(b'\x57\xab\x13'+bytes(bytearray(GATEWAY))) #CH9121 set gateway
wait()
#uart0.write(b'\x57\xab\x24'+NO) #CH9121 set to diconnect network cable NO/YES (Optional)
wait()
uart0.write(b'\x57\xab\x33'+NO) #CH9121 turn on DHCP auto-obtained IP and DNS domain access NO/YES
wait()
#uart0.write(b'\x57\xab\x34'+DEVICE_NAME) #CH9121 set domain name (maximum length 28 bytes) (Optional)
wait()

#Set up UART0 on CH9121
uart0.write(b'\x57\xab\x10'+UART0_MODE.to_bytes(1, 'little')) #uart0 network mode
wait() 
uart0.write(b'\x57\xab\x14'+UART0_LOCAL_PORT.to_bytes(2, 'little')) #uart0 local port number set as static port (Either x14 or x17)
wait()
uart0.write(b'\x57\xab\x15'+bytes(bytearray(UART0_TARGET_IP))) #uart0 destination IP
wait()
uart0.write(b'\x57\xab\x16'+UART0_TARGET_PORT.to_bytes(2, 'little')) #uart0 destination port
wait()
uart0.write(b'\x57\xab\x17'+NO) #uart0 local port number set randomly instead of static port NO/YES (Either x14 or x17)
wait()
uart0.write(b'\x57\xab\x21'+UART0_BAUD_RATE.to_bytes(4, 'little')) #uart0 serial port Baud Rate once configuration is complete
wait()
uart0.write(b'\x57\xab\x22\x01\x04\x08') #uart0 serial port settings (\x01 1 stop bit, \x04 parity none, \x08 8 data bits)  \x00:even , \x01:odd , \x02:mark , \x03:space , \x04:none
wait()
uart0.write(b'\x57\xab\x23\x01\x00\x00\x00') #uart0 serial port setting (Serial timeout \x01\x00\x00\x00 = 1*5ms, after \x46 four bytes need to be filled, and the spaces filled with \x00)
wait()
uart0.write(b'\x57\xab\x25\x00\x02\x00\x00') #uart0 set receiving packet length (Packing length \x00\x02\x00\x00 = 2*256 = 512 bytes)
wait()
uart0.write(b'\x57\xab\x26'+YES) #uart0 set whether to clear serial port data when connected to the network NO/YES
wait()

#Set up UART1 on CH9121
uart0.write(b'\x57\xab\x39'+NO) #uart1 turn on NO/YES - UART1 disabled by default
wait()
uart0.write(b'\x57\xab\x40'+UART1_MODE.to_bytes(1, 'little')) #uart1 network mode
wait()
uart0.write(b'\x57\xab\x41'+UART1_LOCAL_PORT.to_bytes(2, 'little')) #uart1 local port number set as static port (Either x41 or x47) 
wait()
uart0.write(b'\x57\xab\x42'+bytes(bytearray(UART1_TARGET_IP))) #uart1 destination IP
wait()
uart0.write(b'\x57\xab\x43'+UART1_TARGET_PORT.to_bytes(2, 'little')) #uart1 destination port
wait()
uart0.write(b'\x57\xab\x44'+UART1_BAUD_RATE.to_bytes(4, 'little')) #uart1 serial port Baud Rate
wait()
uart0.write(b'\x57\xab\x45\x01\x04\x08') #uart1 serial port settings (\x01 1 stop bit, \x04 parity none {\x00:even , \x01:odd , \x02:mark , \x03:space , \x04:none}, \x08 8 data bits)  
wait()
uart0.write(b'\x57\xab\x46\x01\x00\x00\x00') #uart1 serial port setting (Serial timeout \x01\x00\x00\x00 = 1*5ms, after \x46 four bytes need to be filled, and the spaces filled with \x00)
wait()
uart0.write(b'\x57\xab\x47'+NO) #uart1 local port number set randomly instead of static port NO/YES (Either x41 or x47) 
wait()
uart0.write(b'\x57\xab\x48\x00\x02\x00\x00') #uart1 set receiving packet length (Packing length \x00\x02\x00\x00 = 2*256 = 512 bytes)
wait()
uart0.write(b'\x57\xab\x26'+YES) #uart1 set whether to clear serial port data when connected to the network NO/YES
wait()

#End Configuration and restart CH9121
uart0.write(b'\x57\xab\x0D') #Save parameters to EEPROM
wait()
uart0.write(b'\x57\xab\x0E') #Execute the configuration command and reset CH9121
wait()
uart0.write(b'\x57\xab\x5E') #Leave Serial port configuration mode
wait()
CFG.value(1) #CH9121 configuration pin 14, 0 to config, 1 to exit

print("CH9121 memory set to new parameters")
print()


