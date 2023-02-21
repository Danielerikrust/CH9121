#Waveshare Pico_ETH_CH9121 
#Waveshare 2-Ch Uart to Eth
#GPIO pins in use: 0, 1, 14, 17, GND & VSYS power (also 4 & 5 if UART1 enabled)

#Use the following UART settings with PICO_ETH_CH9121 outside of this configuration file:
    #uart0 = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1)) #uart0 baud=115200, data bits=8, parity=None, stop bit=1
    #uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5)) #uart1 baud=115200, data bits=8, parity=None, stop bit=1  #if enabled at \x39

from machine import UART, Pin
from time import sleep    
    
def wait(i):
    time.sleep(i)
    print("..", end="")
    

    
class CH9121:
    
    RST = Pin(17, Pin.OUT, Pin.PULL_UP) #CH9121 external reset input pin, low active
    CFG = Pin(14, Pin.OUT, Pin.PULL_UP) #CH9121 configuration pin, 0 to config, 1 to exit
        
    NO = b'\x00'
    YES = b'\x01'

    #Variables specific to CH9121
    GATEWAY = (192,168,1,1)             # GATEWAY / Router of LAN
    SUBNET_MASK = (255,255,254,0)       # SUBNET_MASK for LAN
    LOCAL_IP =  (192,168,1,10)          # LOCAL_IP of CH9121 on LAN, for both Uart0 & Uart1 
    USE_DHCP = self.NO                  # turn on DHCP auto-obtained IP and DNS domain access, NO/YES
    CABLE_DISCONNECT = self.NO          # Set to disconnect network cable by software command, NO/YES (Optional)
    DEVICE_NAME = b'PicoEth'            # DEVICE_NAME of CH9121 as seen on the network, replace "PicoEth". (Optional) (maximum length 28 bytes)
              
    #Variables specific to UART0 serial port - TCP Client mode by default
    UART0_MODE = 1                      # Mode 0:TCP Server, Mode 1:TCP Client, Mode 2:UDP Server, Mode 3:UDP Client
    UART0_TARGET_IP = (192,168,1,100)   # TARGET_IP of destination
    UART0_TARGET_PORT = 3500            # TARGET_PORT of destination
    UART0_LOCAL_PORT = 7500             # LOCAL_PORT of UART0, each uart shares local IP but has a unique port, maximum 65535
    UART0_LOCAL_PORT_AUTO = self.NO     # local port number set randomly instead of static port, NO/YES
    UART0_BAUD_RATE = 115200            # BAUD_RATE of UART0 serial Port once configuration is complete
    UART0_CLEAR_DATA = self.YES         # Set whether to clear old serial port data once connected to the network, NO/YES
   
    #Variables specific to UART1 serial port - UART1 disabled by default
    UART1_TURN_ON = self.NO             # Turn on UART1 for use on CH9121, NO/YES - UART1 disabled by default
    UART1_MODE = 1                      # Mode 0:TCP Server, Mode 1:TCP Client, Mode 2:UDP Server, Mode 3:UDP Client
    UART1_TARGET_IP = (192,168,1,75)    # TARGET_IP of destination
    UART1_TARGET_PORT = 3000            # TARGET_PORT of destination
    UART1_LOCAL_PORT = 6000             # LOCAL_PORT of UART1, each uart shares local IP but has a unique port, maximum 65535
    UART1_LOCAL_PORT_AUTO = self.NO     # local port number set randomly instead of static port, NO/YES
    UART1_BAUD_RATE = 115200            # BAUD_RATE of UART1 serial port
    UART1_CLEAR_DATA = self.YES         # Set whether to clear old serial port data once connected to the network, NO/YES
      
        
    def __init__(self):  
        self.RST.value(1) #CH9121 external reset input pin 17, (0 active, 1 inactive)
        self.CFG.value(1) #CH9121 configuration pin, 0 to config, 1 to exit
    
    def configure(self): 
        uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)) #configuration commands required to be sent at a fixed rate of 9600 baud on UART0 only
        
        print("Updating CH9121", end="")
        self.CFG.value(0) #CH9121 configuration pin 14, 0 to config, 1 to exit
        wait()
        x=uart0.read(uart0.any()) #clear any old UART0 data

        #Global network settings for CH9121
        uart0.write(b'\x57\xab\x11'+bytes(bytearray(self.LOCAL_IP))) #CH9121 set local IP
        wait()
        uart0.write(b'\x57\xab\x12'+bytes(bytearray(self.SUBNET_MASK))) #CH9121 set subnet mask
        wait()
        uart0.write(b'\x57\xab\x13'+bytes(bytearray(self.GATEWAY))) #CH9121 set gateway
        wait()
        uart0.write(b'\x57\xab\x24'+self.CABLE_DISCONNECT) #CH9121 set to disconnect network cable by software command, NO/YES (Optional)
        wait()
        uart0.write(b'\x57\xab\x33'+self.USE_DCHP) #CH9121 turn on DHCP auto-obtained IP and DNS domain access, NO/YES
        wait()
        uart0.write(b'\x57\xab\x34'+self.DEVICE_NAME) #CH9121 DEVICE_NAME as seen on the network, replace "PicoEth". (Optional) (maximum length 28 bytes)
        wait()    

        #Set up UART0 on CH9121
        uart0.write(b'\x57\xab\x10'+self.UART0_MODE.to_bytes(1, 'little')) #uart0 network mode
        wait() 
        uart0.write(b'\x57\xab\x14'+self.UART0_LOCAL_PORT.to_bytes(2, 'little')) #uart0 local port number set as static port (Either x14 or x17)
        wait()
        uart0.write(b'\x57\xab\x15'+bytes(bytearray(self.UART0_TARGET_IP))) #uart0 destination IP
        wait()
        uart0.write(b'\x57\xab\x16'+self.UART0_TARGET_PORT.to_bytes(2, 'little')) #uart0 destination port
        wait()
        uart0.write(b'\x57\xab\x17'+self.UART0_LOCAL_PORT_AUTO) #uart0 local port number set randomly instead of static port, NO/YES (Either x14 or x17)
        wait()
        uart0.write(b'\x57\xab\x21'+self.UART0_BAUD_RATE.to_bytes(4, 'little')) #uart0 serial port Baud Rate once configuration is complete
        wait()
        uart0.write(b'\x57\xab\x22\x01\x04\x08') #uart0 serial port settings (\x01 1 stop bit, \x04 parity none, \x08 8 data bits)  \x00:even , \x01:odd , \x02:mark , \x03:space , \x04:none
        wait()
        uart0.write(b'\x57\xab\x23\x01\x00\x00\x00') #uart0 serial port setting (Serial timeout \x01\x00\x00\x00 = 1*5ms, after \x46 four bytes need to be filled, and the spaces filled with \x00)
        wait()
        uart0.write(b'\x57\xab\x25\x00\x02\x00\x00') #uart0 set receiving packet length (Packing length \x00\x02\x00\x00 = 2*256 = 512 bytes)
        wait()
        uart0.write(b'\x57\xab\x26'+self.UART0_CLEAR_DATA) #uart0 set whether to clear old serial port data once connected to the network, NO/YES
        wait()

        #Set up UART1 on CH9121
        uart0.write(b'\x57\xab\x39'+self.UART1_TURN_ON) #uart1 turn on, NO/YES - UART1 disabled by default
        wait()
        uart0.write(b'\x57\xab\x40'+self.UART1_MODE.to_bytes(1, 'little')) #uart1 network mode
        wait()
        uart0.write(b'\x57\xab\x41'+self.UART1_LOCAL_PORT.to_bytes(2, 'little')) #uart1 local port number set as static port (Either x41 or x47) 
        wait()
        uart0.write(b'\x57\xab\x42'+bytes(bytearray(self.UART1_TARGET_IP))) #uart1 destination IP
        wait()
        uart0.write(b'\x57\xab\x43'+self.UART1_TARGET_PORT.to_bytes(2, 'little')) #uart1 destination port
        wait()
        uart0.write(b'\x57\xab\x44'+self.UART1_BAUD_RATE.to_bytes(4, 'little')) #uart1 serial port Baud Rate
        wait()
        uart0.write(b'\x57\xab\x45\x01\x04\x08') #uart1 serial port settings (\x01 1 stop bit, \x04 parity none {\x00:even , \x01:odd , \x02:mark , \x03:space , \x04:none}, \x08 8 data bits)  
        wait()
        uart0.write(b'\x57\xab\x46\x01\x00\x00\x00') #uart1 serial port setting (Serial timeout \x01\x00\x00\x00 = 1*5ms, after \x46 four bytes need to be filled, and the spaces filled with \x00)
        wait()
        uart0.write(b'\x57\xab\x47'+self.UART1_LOCAL_PORT_AUTO) #uart1 local port number set randomly instead of static port, NO/YES (Either x41 or x47) 
        wait()
        uart0.write(b'\x57\xab\x48\x00\x02\x00\x00') #uart1 set receiving packet length (Packing length \x00\x02\x00\x00 = 2*256 = 512 bytes)
        wait()
        uart0.write(b'\x57\xab\x26'+self.UART1_CLEAR_DATA) #uart1 set whether to clear old serial port data once connected to the network, NO/YES
        wait()

        #End Configuration and restart CH9121
        uart0.write(b'\x57\xab\x0D') #Save parameters to EEPROM
        wait()
        uart0.write(b'\x57\xab\x0E') #Execute the configuration command and reset CH9121
        wait()
        uart0.write(b'\x57\xab\x5E') #Leave Serial port configuration mode
        wait()
        self.CFG.value(1) #CH9121 configuration pin 14, 0 to config, 1 to exit

        print("CH9121 memory set to new parameters")
        print()
        
        uart0 = UART(0, baudrate=self.UART0_BAUD_RATE, tx=Pin(0), rx=Pin(1))
        
   

   def read_settings(self):
        uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)) #configuration commands required to be sent at a fixed rate of 9600 baud on UART0 only

        chmode = ["TCP Server", "TCP Client", "UDP Server", "UDP Client"]
        spsettings = ["Even", "Odd", "Mark", "Space", "None"]

        print("Reading CH9121..", end="")
        self.CFG.value(0) #CH9121 configuration pin 14, 0 to config, 1 to exit
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

        #Default UART read buffer is 64 bites, so reading & recording periodically
        x=uart0.read(uart0.any())
        u0mode = chmode[x[0]]
        ch9121localip = str(x[1])+"."+str(x[2])+"."+str(x[3])+"."+str(x[4])
        ch9121subnet = str(x[5])+"."+str(x[6])+"."+str(x[7])+"."+str(x[8])
        ch9121gateway = str(x[9])+"."+str(x[10])+"."+str(x[11])+"."+str(x[12])
        word16bit = ((x[14] <<8) + x[13]) # Shift highbyte 8 bits to the left, then add lowbyte to obtain 16-bit 'bytes' object. Doing them in reverse order to account for 'little'
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
        uart0.write(b'\x57\xab\x03') #1 byte reply uart0 connected? 
        wait()
        uart0.write(b'\x57\xab\x04') #1 byte reply uart1 connected?
        wait()

        x=uart0.read(uart0.any())
        ch9121chipnum = str((x[0]))
        u0connected = "Disconnected"
        u1connected = "Disconnected"
        if x[1]>0:
            u0connected = "Connected"
        if x[2]>0:
            u1connected = "Connected"
    
        #End Configuration Mode
        uart0.write(b'\x57\xab\x5E') #Leave Serial port configuration mode
        time.sleep(0.1)
        self.CFG.value(1) #CH9121 configuration pin 14, 0 to config, 1 to exit

        print("done")
        time.sleep(0.2)
        print()
        print("CH9121 Chip version number: "+ch9121chipnum)
        print("            CH9121 Gateway: "+ch9121gateway)
        print("        CH9121 Subnet Mask: "+ch9121subnet)
        print("           CH9121 Local IP: "+ch9121localip)
        print("        CH9121 Mac Address: "+ch9121mac)
        print()

        print("      UART0 TCP Connection: "+u0connected)
        print("                UART0 Mode: "+u0mode)
        print("           UART0 Target IP: "+u0targetip)
        print("         UART0 Target Port: "+u0targetport)
        print("          UART0 Local Port: "+u0localport)
        print("    UART0 Serial Baud Rate: "+u0baud) 
        print("     UART0 Serial Settings: "+u0serialsettings)
        print("      UART0 Serial Timeout: "+u0timeout)
        print()

        print("      UART1 TCP Connection: "+u1connected)
        print("                UART1 Mode: "+u1mode)
        print("           UART1 Target IP: "+u1targetip)
        print("         UART1 Target Port: "+u1targetport)
        print("          UART1 Local Port: "+u1localport)
        print("    UART1 Serial Baud Rate: "+u1baud)
        print("     UART1 Serial Settings: "+u1serialsettings)
        print("      UART1 Serial Timeout: "+u1timeout)
        print()

        uart0 = UART(0, baudrate=self.UART0_BAUD_RATE, tx=Pin(0), rx=Pin(1)) 
        
        print('Pico UART0: '+str(uart0))
        #print('Pico UART1: '+str(uart1)) #Figure out how to class Uart1 & Uart0


    
