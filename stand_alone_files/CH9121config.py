"""Add this file to the Pico /lib directory"""
"""Modify to your network settings in the constants below"""
"""Add 'import CH9121config' to main.py"""

from machine import UART, Pin
from time import sleep

#Waveshare Pico_ETH_CH9121 
#Waveshare 2-Ch Uart to Eth
#GPIO pins in use: 0, 1, 14, 17, GND & VSYS power (also 4 & 5 if UART1 enabled)

def cmd(i):
    uart0.write(b'\x57\xab'+i)
    sleep(.2)
    print("..", end="")

NO                = b'\x00'
YES               = b'\x01'

CFG = Pin(14, Pin.OUT,Pin.PULL_UP) #CH9121 configuration pin, 0 to config, 1 to exit
RST = Pin(17, Pin.OUT,Pin.PULL_UP) #CH9121 external reset input pin, low active
RST.value(1) #CH9121 external reset input pin 17, (0 active, 1 inactive)

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)) #configuration commands required to be sent at a fixed rate of 9600 baud on UART0 only

#Constants specific to CH9121 hat
GATEWAY           = (192,168,1,1)   # GATEWAY / Router for LAN (Set same as LOCAL_IP for LAN)
SUBNET_MASK       = (255,255,255,0) # SUBNET_MASK for LAN
LOCAL_IP          = (192,168,1,1)   # LOCAL_IP of CH9121 device on LAN
USEDHCP           = NO              # turn on DHCP auto-obtained IP and DNS domain access, NO/YES
CABLEDIS          = NO              # set to disconnect network cable by software command, NO/YES 
DOMAIN_NAME       = b''             # CH9121 network domain name (maximum length 28 bytes) (b'' for LAN uasge) 

#Constants specific to UART0 serial port
UART0_MODE        = 1               # Mode 0:TCP Server, Mode 1:TCP Client, Mode 2:UDP Server, Mode 3:UDP Client
UART0_TARGET_IP   = (192,168,1,100) # TARGET_IP of destination
UART0_TARGET_PORT = 1000            # TARGET_PORT of destination
UART0_LOCAL_PORT  = 2000            # LOCAL_PORT of UART0, each uart shares local IP but has a unique port, maximum 65535
UART0_BAUD_RATE   = 115200          # BAUD_RATE of UART0 serial Port 
UART0_PORTAUTO    = NO              # local port number set randomly instead of static port, NO/YES
UART0_CLEARDATA   = NO              # set whether to clear old serial port data once connected to the network, NO/YES

#Constants specific to UART1 serial port - UART1 disabled by default
UART1_TURNON      = YES              # UART1, turn on, NO/YES 
UART1_MODE        = 3               # Mode 0:TCP Server, Mode 1:TCP Client, Mode 2:UDP Server, Mode 3:UDP Client
UART1_TARGET_IP   = (192,168,1,100) # TARGET_IP of destination
UART1_TARGET_PORT = 2000            # TARGET_PORT of destination
UART1_LOCAL_PORT  = 3000            # LOCAL_PORT of UART1, each uart shares local IP but has a unique port, maximum 65535
UART1_BAUD_RATE   = 115200          # BAUD_RATE of UART1 serial port
UART1_PORTAUTO    = NO              # local port number set randomly instead of static port, NO/YES
UART1_CLEARDATA   = NO              # set whether to clear old serial port data once connected to the network, NO/YES

#Use the following UART settings with PICO_ETH_CH9121 outside of this configuration file:
    #uart0 = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1)) #uart0 baud=115200, data bits=8, parity=None, stop bit=1
    #uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5)) #uart1 baud=115200, data bits=8, parity=None, stop bit=1  #if enabled at \x39

NO  = b'\x00'
YES = b'\x01'

print("Configuring CH9121", end="")
CFG.value(0) #CH9121 configuration pin 14, 0 to config, 1 to exit
sleep(.1)

#Global network settings for CH9121
cmd(b'\x11'+bytes(bytearray(LOCAL_IP))) #CH9121 local IP
cmd(b'\x12'+bytes(bytearray(SUBNET_MASK))) #CH9121 set subnet mask
cmd(b'\x13'+bytes(bytearray(GATEWAY))) #CH9121 set gateway (Set same as LOCAL_IP for LAN)
cmd(b'\x24'+CABLEDIS) #CH9121 set to diconnect from network NO/YES (Optional)
cmd(b'\x33'+USEDHCP) #CH9121 turn on DHCP auto-obtained IP and DNS domain access NO/YES
cmd(b'\x34'+DOMAIN_NAME) #CH9121 set network domain name (maximum length 28 bytes) (b'' for LAN uasge)

#Set up UART0 on CH9121
cmd(b'\x10'+UART0_MODE.to_bytes(1, 'little')) #uart0 network mode
cmd(b'\x14'+UART0_LOCAL_PORT.to_bytes(2, 'little')) #uart0 local port number set as static port (Either x14 or x17)
cmd(b'\x15'+bytes(bytearray(UART0_TARGET_IP))) #uart0 destination IP
cmd(b'\x16'+UART0_TARGET_PORT.to_bytes(2, 'little')) #uart0 destination port
cmd(b'\x17'+UART0_PORTAUTO) #uart0 local port number set randomly instead of static port NO/YES (Either x14 or x17)
cmd(b'\x21'+UART0_BAUD_RATE.to_bytes(4, 'little')) #uart0 serial port Baud Rate once configuration is complete
cmd(b'\x22\x01\x04\x08') #uart0 serial port settings (\x01 1 stop bit, \x04 parity none, \x08 8 data bits)  \x00:even , \x01:odd , \x02:mark , \x03:space , \x04:none
cmd(b'\x23\x01\x00\x00\x00') #uart0 serial port setting (Serial timeout \x01\x00\x00\x00 = 1*5ms, after \x46 four bytes need to be filled, and the spaces filled with \x00)
cmd(b'\x25\x00\x02\x00\x00') #uart0 set receiving packet length (Packing length \x00\x02\x00\x00 = 2*256 = 512 bytes)
cmd(b'\x26'+UART0_CLEARDATA) #uart0 set whether to clear serial port data when connected to the network NO/YES

#Set up UART1 on CH9121
cmd(b'\x39'+UART1_TURNON) #uart1 turn on NO/YES - UART1 disabled by default
cmd(b'\x40'+UART1_MODE.to_bytes(1, 'little')) #uart1 network mode
cmd(b'\x41'+UART1_LOCAL_PORT.to_bytes(2, 'little')) #uart1 local port number set as static port (Either x41 or x47) 
cmd(b'\x42'+bytes(bytearray(UART1_TARGET_IP))) #uart1 destination IP
cmd(b'\x43'+UART1_TARGET_PORT.to_bytes(2, 'little')) #uart1 destination port
cmd(b'\x44'+UART1_BAUD_RATE.to_bytes(4, 'little')) #uart1 serial port Baud Rate
cmd(b'\x45\x01\x04\x08') #uart1 serial port settings (\x01 1 stop bit, \x04 parity none {\x00:even , \x01:odd , \x02:mark , \x03:space , \x04:none}, \x08 8 data bits)  
cmd(b'\x46\x01\x00\x00\x00') #uart1 serial port setting (Serial timeout \x01\x00\x00\x00 = 1*5ms, after \x46 four bytes need to be filled, and the spaces filled with \x00)
cmd(b'\x47'+UART1_PORTAUTO) #uart1 local port number set randomly instead of static port NO/YES (Either x41 or x47) 
cmd(b'\x48\x00\x02\x00\x00') #uart1 set receiving packet length (Packing length \x00\x02\x00\x00 = 2*256 = 512 bytes)
cmd(b'\x49'+UART1_CLEARDATA) #uart1 set whether to clear serial port data when connected to the network NO/YES

#End Configuration and restart CH9121
cmd(b'\x0D') #Save parameters to EEPROM
cmd(b'\x0E') #Execute the configuration command and reset CH9121
cmd(b'\x5E') #Leave Serial port configuration mode
CFG.value(1) #CH9121 configuration pin 14, 0 to config, 1 to exit
print("done")
print("CH9121 memory set to new parameters")
print()
