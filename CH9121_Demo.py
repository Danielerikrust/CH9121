"""Demo file for using CH9121.py with a Waveshare uart to ethernet device"""
from CH9121 import CH9121


"""CH9121 Ethernet Setup Section"""
eth = CH9121(uarts=1, config=False) # Initialize the CH9121 device for Uart0 only, manual config()
#eth = CH9121(uarts=2, config=False) # Initialize the CH9121 device for both Uart0 & Uart1, manual config()


"""Set these ethernet variables to suit your application
Separate IP addresses with commas as a Micropython List"""
#Constants for use in variables below
NO = b'\x00'
YES = b'\x01'

#Variables specific to CH9121
eth.gateway = (192,168,1,1)         # gateway / Router of LAN (Duplicate localip for LAN)
eth.subnet = (255,255,254,0)        # subnet for LAN
eth.localip = (192,168,1,10)        # local IP of CH9121 on LAN, for both Uart0 & Uart1 
eth.usedhcp = NO                    # turn on DHCP auto-obtained IP and DNS domain access, NO/YES
eth.cabledis = NO                   # set to disconnect network cable by software command, NO/YES (Optional)
eth.domainname = b''                # domain name of CH9121 (Optional) (maximum length 28 bytes)
              
#Variables specific to UART0 serial port 
eth.u0mode = 1                      # Mode 0:TCP Server, Mode 1:TCP Client, Mode 2:UDP Server, Mode 3:UDP Client
eth.u0targetip = (192,168,1,100)    # IP of destination for UART0
eth.u0targetport = 3500             # port of destination for UART0
eth.u0localport = 7500              # the local port for UART0, each uart shares the local IP but has a unique port, maximum 65535
eth.u0portauto = NO                 # local port number set randomly instead of static port, NO/YES
eth.u0baud = 115200                 # baud rate of UART0 serial Port once configuration is complete
eth.u0cleardata = YES               # set whether to clear old serial port data once connected to the network, NO/YES
   
#Variables specific to UART1 serial port 
eth.u1on = NO                       # Turn on UART1 for use on CH9121, NO/YES - Best to initialize by 'eth = CH9121(2)'
eth.u1mode = 3                      # Mode 0:TCP Server, Mode 1:TCP Client, Mode 2:UDP Server, Mode 3:UDP Client
eth.u1targetip = (192,168,1,75)     # IP of destination for UART1
eth.u1targetport = 3000             # port of destination for UART1
eth.u1localport = 6000              # local port of UART1, each uart shares the local IP but has a unique port, maximum 65535
eth.u1portauto = NO                 # local port number set randomly instead of static port, NO/YES
eth.u1baud = 115200                 # baud rate of UART1 serial port
eth.u1cleardata = YES               # set whether to clear old serial port data once connected to the network, NO/YES

#Variables to save the readsettings() data to a file
eth.readtofile = True               # readsettings() will also write the data to ethfile when readtofile = True
eth.ethfile = "CH9121config.txt"    # readsettings() will also write the data to ethfile when readtofile = True

print(eth)                          # prints current settings as held in the CH9121 Class

"""Manual Config() to incorporate any new settings from above"""
#First configure the CH9121 for 1 channel uart
eth.config()
eth.readsettings()

#Then configure it for 2 channel uart
print()
print("Now configure with UART1 Enabled and a few new settings:")
eth.u1on = YES                      
eth.u1targetip = (192,168,0,222)     
eth.u1targetport = 1578
eth.u1mode = 0
eth.config()
eth.readsettings()
