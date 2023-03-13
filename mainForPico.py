"""
For use with the Rpi Pico & Pico-ETH-CH9121 hat.
Copy CH9121.py to the Pico /lib directory and run this file.
Pico writes its internal temperature every 4 seconds, and looks
for incoming transmission every 2 seconds.
For Pico to Pico communication NAME one Pico#1, and the other Pico#2."""

NAME = "Pico#1"

from time import sleep
from machine import Pin, Timer, ADC
from CH9121 import CH9121

led=Pin(25,Pin.OUT,value=0) #LED off by default
 

"""CH9121 Ethernet Setup Section"""
eth = CH9121(uarts=1, config=False)    # Initialize the CH9121 device for both Uart0 & Uart1, manual config()

eth.domainname    = b''                # Needs to be b'' for UDP Server Mode
eth.localip       = (192,168,0,91)     # local IP of CH9121 on LAN, for both Uart0 & Uart1 
eth.gateway       = (192,168,0,91)     # gateway / Router (If LAN duplicate the device IP as the Gateway)

eth.u0mode        = 1                  # Mode 0:TCP Server, Mode 1:TCP Client, Mode 2:UDP Server, Mode 3:UDP Client
eth.u0targetip    = (192,168,0,81)     # IP of destination for UART0, maximum 65535
eth.u0localport   = 4000               # the local port for UART0, each uart shares the local IP but has a unique port, maximum 65535
eth.u0targetport  = 4000               # port of destination for UART0

eth.u1mode        = 1                  # Mode 0:TCP Server, Mode 1:TCP Client, Mode 2:UDP Server, Mode 3:UDP Client
eth.u1targetip    = (192,168,0,81)     # IP of destination for UART1, maximum 65535
eth.u1localport   = 5000               # the local port for UART1, each uart shares the local IP but has a unique port, maximum 65535
eth.u1targetport  = 5000               # port of destination for UART1


eth.config()
print("Ethernet Connecting")
sleep(10) #Sometimes takes the CH9121 about 10 seconds to fully connect
print("Ethernet Connected")
print()
led.toggle() #Pico LED on once connected
eth.readsettings()
print(f'Writing & Reading Temps')


"""Communication Section"""
def blink(times=3): #Blinks three times by default
    for x in range(times*2):
        led.toggle()
 
def picotempF():
    adc  = ADC(4)
    adc_voltage = adc.read_u16() * (3.3 / 65535)
    temp = 27 - (adc_voltage - 0.706) / 0.001721
    temp = 32 + (1.8 * temp) # Convert from C to F
    return (f'{temp:.2f}{chr(176)}F')

def eth0write():    
    data = f'{NAME} u0 is {picotempF()}'
    print(data)
    data.encode('utf-8')
    eth.u0.write(data)
    #End eth0write()

def eth1write():    
    if eth.u1on == eth.YES:
        data = f'{NAME} u1 is {picotempF()}'
        print(data)
        data.encode('utf-8')
        eth.u1.write(data)
    #End eth1write()

def eth0read():     
    if eth.u0.any() > 0:
        data = eth.u0.read(eth.u0.any())
        data = data.decode('utf-8')
        print(f'{NAME} u0 reads: {data}')   
        blink() #Pico led will Blink when it recieves a message
    else:
        print(f'{NAME} u0 listening')
    #End eth0read()

def eth1read():     
    if (eth.u1on == eth.YES) and (eth.u1.any() > 0):
        data = eth.u1.read(eth.u1.any())
        data = data.decode('utf-8')
        print(f'{NAME} u1 reads: {data}')   
        blink() #Pico led will Blink when it recieves a message
    else:
        print(f'{NAME} u1 listening')
    #End eth1read()

"""Main Operating Section"""
# Timer repeats its function in periods of milliseconds, period=1000 = 1 sec recurrance
# Timer can only pass a Timer object to the function it calls. Thus the read & write functions are designed not call other variables.

write0timer = Timer(-1, period=4000, mode=Timer.PERIODIC, callback=lambda w0:eth0write())
read0timer  = Timer(-1, period=2000, mode=Timer.PERIODIC, callback=lambda r0:eth0read())

if eth.u1on == eth.YES: # Set Uart1 Timers if it has been configured
    write1timer = Timer(-1, period=4000, mode=Timer.PERIODIC, callback=lambda w1:eth1write())
    read1timer  = Timer(-1, period=2000, mode=Timer.PERIODIC, callback=lambda r1:eth1read())    
