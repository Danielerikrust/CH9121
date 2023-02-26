#Waveshare Pico_ETH_CH9121 
#Waveshare 2-Ch Uart to Eth
#Pico GPIO pins in use: 0, 1, 14, 17, GND & VSYS power (also 4 & 5 if UART1 enabled)

from machine import UART, Pin
from time import sleep    

    
class CH9121:
    """Constants & Variables for CH9121"""
    #If not using Rpi Pico, change the following RST & CFG Pin numbers to suit your device
    RST = Pin(17, Pin.OUT, Pin.PULL_UP) #CH9121 external reset input pin, low active
    CFG = Pin(14, Pin.OUT, Pin.PULL_UP) #CH9121 configuration pin, 0 to config, 1 to exit
        
    #Add the following constants to main.py for easier access, or else use "eth.YES"
    NO = b'\x00'
    YES = b'\x01'

    #Variables specific to CH9121
    gateway = (192,168,1,1)         # gateway / Router of LAN
    subnet = (255,255,254,0)        # subnet for LAN
    localip = (192,168,1,10)        # local IP of CH9121 on LAN, for both Uart0 & Uart1 
    usedhcp = NO                    # turn on DHCP auto-obtained IP and DNS domain access, NO/YES
    cabledisconnect = NO            # set to disconnect network cable by software command, NO/YES (Optional)
    devicename = b'PicoEth'         # devicename of CH9121 as seen on the network, replace "PicoEth". (Optional) (maximum length 28 bytes)
              
    #Variables specific to UART0 serial port - TCP Client mode by default
    u0mode = 1                      # Mode 0:TCP Server, Mode 1:TCP Client, Mode 2:UDP Server, Mode 3:UDP Client
    u0targetip = (192,168,1,100)    # IP of destination for UART0
    u0targetport = 3500             # port of destination for UART0
    u0localport = 7500              # the local port for UART0, each uart shares the local IP but has a unique port, maximum 65535
    u0portauto = NO                 # local port number set randomly instead of static port, NO/YES
    u0baud = 115200                 # baud rate of UART0 serial Port once configuration is complete
    u0cleardata = YES               # set whether to clear old serial port data once connected to the network, NO/YES
   
    #Variables specific to UART1 serial port - UART1 disabled by default
    u1on = NO                       # Turn on UART1 for use on CH9121, NO/YES - Best to initialize by 'eth = CH9121(2)'
    u1mode = 3                      # Mode 0:TCP Server, Mode 1:TCP Client, Mode 2:UDP Server, Mode 3:UDP Client
    u1targetip = (192,168,1,75)     # IP of destination for UART1
    u1targetport = 3000             # port of destination for UART1
    u1localport = 6000              # local port of UART1, each uart shares the local IP but has a unique port, maximum 65535
    u1portauto = NO                 # local port number set randomly instead of static port, NO/YES
    u1baud = 115200                 # baud rate of UART1 serial port
    u1cleardata = YES               # set whether to clear old serial port data once connected to the network, NO/YES
      
    #Variables to save the readsettings() data to a file
    readtofile = True               # readsettings() will also write the data to ethfile when readtofile = True
    ethfile = "CH9121settings.txt"  # readsettings() will also write the data to ethfile when readtofile = True

    
    """Functions for CH9121"""
    def __init__(self, uarts = 1):  #uarts are the number of uarts in use: 1 or 2
              
        self.RST.value(1) #CH9121 external reset input pin 17, (0 active, 1 inactive)
        self.CFG.value(1) #CH9121 configuration pin, 0 to config, 1 to exit
        
        #Setup the uarts
        self.u1on = self.NO
        u0 = UART(0, baudrate=self.u0baud, tx=Pin(0), rx=Pin(1), timeout = 10, timeout_char = 10) #uart0 baud=115200, data bits=8, parity=None, stop bit=1
        if uarts > 1:
            self.u1on = self.YES
            u1 = UART(1, baudrate=self.u1baud, tx=Pin(4), rx=Pin(5), timeout = 10, timeout_char = 10) #uart1 baud=115200, data bits=8, parity=None, stop bit=1
            
   
    def wait(self, i):
        sleep(i)
        print("..", end="")

    def config(self):    
        self.u0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)) #configuration commands required to be sent at a fixed rate of 9600 baud on UART0 only
        
        W = .4
        
        print("Updating CH9121", end="")
        self.CFG.value(0) #CH9121 configuration pin 14, 0 to config, 1 to exit
        self.wait(W)
        x=self.u0.read(self.u0.any()) #clear any old UART0 data

        #Global network settings for CH9121
        self.u0.write(b'\x57\xab\x11'+bytes(bytearray(self.localip))) #CH9121 set local IP
        self.wait(W)
        self.u0.write(b'\x57\xab\x12'+bytes(bytearray(self.subnet))) #CH9121 set subnet mask
        self.wait(W)
        self.u0.write(b'\x57\xab\x13'+bytes(bytearray(self.gateway))) #CH9121 set gateway
        self.wait(W)
        self.u0.write(b'\x57\xab\x24'+self.cabledisconnect) #CH9121 set to disconnect network cable by software command, NO/YES (Optional)
        self.wait(W)
        self.u0.write(b'\x57\xab\x33'+self.usedhcp) #CH9121 turn on DHCP auto-obtained IP and DNS domain access, NO/YES
        self.wait(W)
        self.u0.write(b'\x57\xab\x34'+self.devicename) #CH9121 devicename as seen on the network, replace "PicoEth". (Optional) (maximum length 28 bytes)
        self.wait(W)    

        #Set up UART0 on CH9121
        self.u0.write(b'\x57\xab\x10'+self.u0mode.to_bytes(1, 'little')) #uart0 network mode
        self.wait(W) 
        self.u0.write(b'\x57\xab\x14'+self.u0localport.to_bytes(2, 'little')) #uart0 local port number set as static port (Either x14 or x17)
        self.wait(W)
        self.u0.write(b'\x57\xab\x15'+bytes(bytearray(self.u0targetip))) #uart0 destination IP
        self.wait(W)
        self.u0.write(b'\x57\xab\x16'+self.u0targetport.to_bytes(2, 'little')) #uart0 destination port
        self.wait(W)
        self.u0.write(b'\x57\xab\x17'+self.u0portauto) #uart0 local port number set randomly instead of static port, NO/YES (Either x14 or x17)
        self.wait(W)
        self.u0.write(b'\x57\xab\x21'+self.u0baud.to_bytes(4, 'little')) #uart0 serial port Baud Rate once configuration is complete
        self.wait(W)
        self.u0.write(b'\x57\xab\x22\x01\x04\x08') #uart0 serial port settings (\x01 1 stop bit, \x04 parity none, \x08 8 data bits)  \x00:even , \x01:odd , \x02:mark , \x03:space , \x04:none
        self.wait(W)
        self.u0.write(b'\x57\xab\x23\x02\x00\x00\x00') #uart0 serial port setting (Serial timeout \x02\x00\x00\x00 = 1*5ms = 10ms, after \x46 four bytes need to be filled, and the spaces filled with \x00)
        self.wait(W)
        self.u0.write(b'\x57\xab\x25\x00\x02\x00\x00') #uart0 set receiving packet length (Packing length \x00\x02\x00\x00 = 2*256 = 512 bytes)
        self.wait(W)
        self.u0.write(b'\x57\xab\x26'+self.u0cleardata) #uart0 set whether to clear old serial port data once connected to the network, NO/YES
        self.wait(W)

        #Set up UART1 on CH9121
        self.u0.write(b'\x57\xab\x39'+self.u1on) #uart1 turn on, NO/YES - UART1 disabled by default
        self.wait(W)
        self.u0.write(b'\x57\xab\x40'+self.u1mode.to_bytes(1, 'little')) #uart1 network mode
        self.wait(W)
        self.u0.write(b'\x57\xab\x41'+self.u1localport.to_bytes(2, 'little')) #uart1 local port number set as static port (Either x41 or x47) 
        self.wait(W)
        self.u0.write(b'\x57\xab\x42'+bytes(bytearray(self.u1targetip))) #uart1 destination IP
        self.wait(W)
        self.u0.write(b'\x57\xab\x43'+self.u1targetport.to_bytes(2, 'little')) #uart1 destination port
        self.wait(W)
        self.u0.write(b'\x57\xab\x44'+self.u1baud.to_bytes(4, 'little')) #uart1 serial port Baud Rate
        self.wait(W)
        self.u0.write(b'\x57\xab\x45\x01\x04\x08') #uart1 serial port settings (\x01 1 stop bit, \x04 parity none {\x00:even , \x01:odd , \x02:mark , \x03:space , \x04:none}, \x08 8 data bits)  
        self.wait(W)
        self.u0.write(b'\x57\xab\x46\x02\x00\x00\x00') #uart1 serial port setting (Serial timeout \x02\x00\x00\x00 = 1*5ms = 10ms, after \x46 four bytes need to be filled, and the spaces filled with \x00)
        self.wait(W)
        self.u0.write(b'\x57\xab\x47'+self.u1portauto) #uart1 local port number set randomly instead of static port, NO/YES (Either x41 or x47) 
        self.wait(W)
        self.u0.write(b'\x57\xab\x48\x00\x02\x00\x00') #uart1 set receiving packet length (Packing length \x00\x02\x00\x00 = 2*256 = 512 bytes)
        self.wait(W)
        self.u0.write(b'\x57\xab\x26'+self.u1cleardata) #uart1 set whether to clear old serial port data once connected to the network, NO/YES
        self.wait(W)

        #End Configuration and restart CH9121
        self.u0.write(b'\x57\xab\x0D') #Save parameters to EEPROM
        self.wait(W)
        self.u0.write(b'\x57\xab\x0E') #Execute the configuration command and reset CH9121
        self.wait(W)
        self.u0.write(b'\x57\xab\x5E') #Leave Serial port configuration mode
        self.wait(W)
        self.CFG.value(1) #CH9121 configuration pin 14, 0 to config, 1 to exit

        print("done")
        print("CH9121 memory set to new parameters")
        print()
        
        self.u0 = UART(0, baudrate=self.u0baud, tx=Pin(0), rx=Pin(1), timeout = 10, timeout_char = 10)
        
  

    def readsettings(self):
        self.u0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)) #configuration commands required to be sent at a fixed rate of 9600 baud on UART0 only

        W = .4
        chmode = ["TCP Server", "TCP Client", "UDP Server", "UDP Client"]
        spsettings = ["Even", "Odd", "Mark", "Space", "None"]

        print("Reading CH9121..", end="")
        self.CFG.value(0) #CH9121 configuration pin 14, 0 to config, 1 to exit
        self.wait(W)
        x=self.u0.read(self.u0.any()) #clear the data

        #CH9121 network settings
        self.u0.write(b'\x57\xab\x60') #1 byte reply for uart0 working mode
        self.wait(W)
        self.u0.write(b'\x57\xab\x61') #4 bytes reply for CH9121 local IP
        self.wait(W)
        self.u0.write(b'\x57\xab\x62') #4 bytes reply for CH9121 subnet mask
        self.wait(W)
        self.u0.write(b'\x57\xab\x63') #4 bytes reply for CH9121 gateway
        self.wait(W)
        self.u0.write(b'\x57\xab\x64') #2 bytes reply for uart0 local port
        self.wait(W)
        self.u0.write(b'\x57\xab\x65') #4 bytes reply for uart0 destination IP
        self.wait(W)

        #Default UART read buffer is 64 bites, so reading & recording periodically
        x=self.u0.read(self.u0.any())
        u0mode = chmode[x[0]]
        ch9121localip = f"{x[1]}.{x[2]}.{x[3]}.{x[4]}"
        ch9121subnet = f"{x[5]}.{x[6]}.{x[7]}.{x[8]}"
        ch9121gateway = f"{x[9]}.{x[10]}.{x[11]}.{x[12]}"
        u0localport = f"{(x[14] <<8) + x[13]}"
        # for all Ports shift highbyte 8 bits to the left, then add lowbyte to obtain 16-bit 'bytes' object. Doing them in reverse order to account for 'little'
        u0targetip = f"{x[15]}.{x[16]}.{x[17]}.{x[18]}"

        self.u0.write(b'\x57\xab\x66') #2 bytes reply for uart0 target port
        self.wait(W)
        self.u0.write(b'\x57\xab\x71') #4 bytes reply for uart0 baud
        self.wait(W)
        self.u0.write(b'\x57\xab\x72') #3 bytes reply for uart0 serial parameters
        self.wait(W)
        self.u0.write(b'\x57\xab\x73') #4 bytes reply for uart0 timeout
        self.wait(W)
        self.u0.write(b'\x57\xab\x81') #6 bytes reply for CH9121 mac address
        self.wait(W)
        self.u0.write(b'\x57\xab\x90') #1 byte reply for uart1 mode
        self.wait(W)

        x=self.u0.read(self.u0.any())
        u0targetport = f"{(x[1] <<8) + x[0]}"
        u0baud = f"{(x[5] <<24) + (x[4] <<16) + (x[3] <<8) + x[2]}"
        # For all bauds shift highbyte 24 bits to the left. Shift 3rd byte 16 to the left. Shift 2nd byte 8 to the left. Then add lowbyte to obtain 64-bit 'bytes' object. Doing them in reverse order to account for 'little'
        u0serialsettings = f"data bits={x[8]}, parity={spsettings[x[7]]}, stop bit={x[6]}"
        u0timeout = f"{x[9] * 5} ms" 
        ch9121mac = f"{'%02x' % x[10]}:{'%02x' % x[11]}:{'%02x' % x[12]}:{'%02x' % x[13]}:{'%02x' % x[14]}:{'%02x' % x[15]}"
        u1mode = chmode[x[16]]

        self.u0.write(b'\x57\xab\x91') #2 bytes reply for uart1 local port
        self.wait(W)
        self.u0.write(b'\x57\xab\x92') #4 bytes reply for uart1 target IP
        self.wait(W)
        self.u0.write(b'\x57\xab\x93') #2 bytes reply for uart1 target port
        self.wait(W)
        self.u0.write(b'\x57\xab\x94') #4 bytes reply for uart1 baud
        self.wait(W)
        self.u0.write(b'\x57\xab\x95') #3 bytes reply for uart1 serial parameters
        self.wait(W)
        self.u0.write(b'\x57\xab\x96') #1 byte reply for uart1 timeout
        self.wait(W)

        x=self.u0.read(self.u0.any())
        u1localport = f"{(x[1] <<8) + x[0]}"
        u1targetip = f"{x[2]}.{x[3]}.{x[4]}.{x[5]}"
        u1targetport = f"{(x[7] <<8) + x[6]}"
        u1baud = f"{(x[11] <<24) + (x[10] <<16) + (x[9] <<8) + x[8]}"
        u1serialsettings = f"data bits={x[14]}, parity={spsettings[x[13]]}, stop bit={x[12]}"
        u1timeout = f"{x[15] * 5} ms"

        self.u0.write(b'\x57\xab\x01') #1 byte reply for CH9121 chip version number
        self.wait(W)
        self.u0.write(b'\x57\xab\x03') #1 byte reply for uart0 TCP client connection status? 
        self.wait(W)
        self.u0.write(b'\x57\xab\x04') #1 byte reply for uart1 TCP client connection status?
        self.wait(W)
        self.u0.write(b'\x57\xab\x67') #1 byte reply for reading number of reconnections
        self.wait(W)

        x=self.u0.read(self.u0.any())
        ch9121chipnum = f"{x[0]}"
        u0connected = "TCP Disconnected"
        u1connected = "TCP Disconnected"
        if x[1]>0:
            u0connected = "TCP Connected"
        if x[2]>0:
            u1connected = "TCP Connected"
        if u0mode != chmode[1]:
            u0connected = "Not in TCP Client Mode"
        if u1mode != chmode[1]:
            u1connected = "Not in TCP Client Mode"
        CH9121reconnections = f"{x[3]}"
    
        #End Configuration Mode
        self.u0.write(b'\x57\xab\x5E') #Leave Serial port configuration mode
        self.wait(W)
        self.CFG.value(1) #CH9121 configuration pin 14, 0 to config, 1 to exit
        self.wait(W)
        print("done")
        
        """Display of readings"""
        u1enabled = "Disabled"
        if self.u1on == self.YES:
            u1enabled = "Enabled"
            
        if self.readtofile: # Erases the file for a new reading of CH9121
            file = open(self.ethfile, 'w') # Open File: Write "w", Append "a", Read "r", Read-Write "r+"
                 
        def report(txt):
            print(txt)
            if self.readtofile:
                file = open(self.ethfile, 'a') # Open File: Write "w", Append "a", Read "r", Read-Write "r+"
                file.write(txt + "\r\n")
                file.close()
                 
        report("")
        report(f"               *CH9121 General Settings*")
        report(f"       CH9121 Chip Version: {ch9121chipnum}")
        report(f"        CH9121 Mac Address: {ch9121mac}")
        report(f"            CH9121 Gateway: {ch9121gateway}")
        report(f"        CH9121 Subnet Mask: {ch9121subnet}")
        report(f"           CH9121 Local IP: {ch9121localip}")
        report(f"CH9121 Reconnections Count: {CH9121reconnections}")
        report("")

        report(f"                *CH9121 UART0 Settings*")
        report(f"                UART0 Mode: {u0mode}")
        report(f"   UART0 TCP Client Status: {u0connected}")
        report(f"           UART0 Target IP: {u0targetip}")
        report(f"         UART0 Target Port: {u0targetport}")
        report(f"          UART0 Local Port: {u0localport}")
        report(f"    UART0 Serial Baud Rate: {u0baud}") 
        report(f"     UART0 Serial Settings: {u0serialsettings}")
        report(f"      UART0 Serial Timeout: {u0timeout}")
        report("")
        
        self.u0 = UART(0, baudrate=self.u0baud, tx=Pin(0), rx=Pin(1), timeout = 10, timeout_char = 10) 
        report(f"                 *Pico UART0 Settings*")
        report(f"{self.u0}")
        report("")        
        
        report(f"                *CH9121 UART1 Settings*")
        report(f"                     UART1: {u1enabled}")
        report(f"                UART1 Mode: {u1mode}")
        report(f"   UART1 TCP Client Status: {u1connected}")
        report(f"           UART1 Target IP: {u1targetip}")
        report(f"         UART1 Target Port: {u1targetport}")
        report(f"          UART1 Local Port: {u1localport}")
        report(f"    UART1 Serial Baud Rate: {u1baud}")
        report(f"     UART1 Serial Settings: {u1serialsettings}")
        report(f"      UART1 Serial Timeout: {u1timeout}")
        report("")

        if self.u1on == self.YES:
            self.u1 = UART(1, baudrate=self.u1baud, tx=Pin(4), rx=Pin(5), timeout = 10, timeout_char = 10)
            report(f"                 *Pico UART1 Settings*")
            report(f"{self.u1}")
            report("")
        
        print("")
        print(f"CH9121 settings written to: {self.ethfile}.")
            

    
