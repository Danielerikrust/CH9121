"""Demo file for using CH9121.py with a Waveshare uart to ethernet device"""
from CH9121 import CH9121


"""CH9121 Ethernet Setup Section using the default values in CH9121.py
Change the default network variables in CH9121.py if your settings are unchanging"""

#eth = CH9121(uarts=1,config=True)      #Initialize the CH9121 device for Uart0 only, auto config()
eth = CH9121(uarts=2,config=True)       #Initialize the CH9121 device for both Uart0 & Uart1, auto config()

print(eth)                              #Prints a summary of current ethernet settings held in the CH9121 Class

eth.readsettings()                      #Reads the Pico-Eth-CH9121 and prints the results as told by the chip

