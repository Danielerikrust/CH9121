# CH9121

Micropython files for the Waveshare Pico_ETH_CH9121 ethernet hat for Raspberry Pi Pico, and Waveshare 2-Ch_Uart_to_Eth board.

![The Board](/images/Pico-ETH-CH9121.jpg#center)

These files incorporate the full range of commands provided in:

https://www.waveshare.com/w/upload/e/ef/CH9121_SPCC.pdf

https://www.waveshare.com/wiki/Pico-ETH-CH9121


## Installation

Copy *Serial_Port_Parameter_Configuration_Full.py* to the /lib directory of your Pico. Create that directory in Thonny if not already present. To save the network preferences into the CH9121 chip while powered add this to *main.py*.

    import Serial_Port_Parameter_Configuration_Full

https://thonny.org/

*CH9121_read_chip_settings.py* should also be run from Thonny with the Pico attached. The read file also does not need to be part of main.py, nor stored in /lib. Just run it when you need to check. It incorporates the full range of read options laid out in:

https://www.waveshare.com/w/upload/e/ef/CH9121_SPCC.pdf

To incorporate a read into your *main.py* startup copy *CH9121_read_chip_settings.py* into the Pico's /lib directory. Then add this to *main.py*:

    import Serial_Port_Parameter_Configuration_Full
    import CH9121_read_chip_settings


## Configuration

Adjust your network settings with the variables in *Serial_Port_Parameter_Configuration_Full.py*. IP addresses are separated by comma and not periods as a micropython list. To find your gateway & subnet mask your router will usually have a sticker with a router loggin such as http://routerlogin.net or its IP Address. It will also show the default login & password. While in the router admin search for its gateway & submask, and assign your CH9121 the same static IP you assinged in the configuration variables. Otherwise your routers DHCP will try to assign it a random IP address. DHCP support can be enabled on the CH9121 with the parameter configuration file if desired. 

You can verify the CH9121 Mac address generated from *CH9121_read_chip_settings.py* against your router admin listing associated with the expected CH9121 IP address.

The Pico_ETH_CH9121 can be pinged from another computer on the LAN when the network settings are correct. And the *CH9121_read_chip_settings.py* file confirms that your Pico UART0 is set up properly for RX & TX with the CH9121 when it outputs data.


# CH9121 Specifications
Specifications for the Waveshare Pico_ETH_CH9121 ethernet hat for Raspberry Pi Pico, and Waveshare 2-Ch_Uart_to_Eth board.


## Default Parameters

Uart 1 is disabled, and Uart 0 works in *TCP CLIENT* mode by default.

Configuration of the CH9121 must be conducted through Uart 0, at 9600 baud.

The default network parameters of the CH9121
- Device/Local IP: 192.168.1.200
- Subnet mask: 255.255.255.0
- Number of reconnections: unlimited

The default parameters of CH9121 Uart 0:
- Device/Local port: 2000
- Target IP: 192.168.1.100
- Target port: 1000
- Ethernet Data cache: 6K bytes

The default serial parameters of CH9121 Uart 0 & Uart 1 (These match default Pico parameters, except baud):
- Baud rate: 9600
- Timeout: 0
- Data bit: 8
- Stop bit: 1
- Parity bit: None
- Clear buffer: Never
- Serial Flow Control: None
- Serial Cache: 2K bytes


## Reset Jumper

(Differentiated from the RST Pin, which severs and resets active ethernet connections to the chip)

I asked Waveshare technical support to explain the function of the two holes marked RESET on the bottom of the Pico-ETH-CH9121.

> Question: Could you please tell me how to use the two wire holes marked RESET on the bottom of the pico-eth-ch9121? Thank you.

> Response: They are used for resetting the setting of the module, short the holes and then powering will restore the module to factory setting.

Following this instruction I bent and inserted a 2mm wire to short the holes without soldering as seen in the picture below. 

![Reset Jumper](/images/CH9121Reset.jpg#center)

Then, upon repowering the unit the *CH9121_Read_Settings.py* confirmed factory reset to the chip parameters.

>                CH9121 Gateway: 192.168.1.1
>            CH9121 Subnet Mask: 255.255.255.0
>               CH9121 Local IP: 192.168.1.200
>  
>                    UART0 Mode: TCP Client
>               UART0 Target IP: 192.168.1.100
>             UART0 Target Port: 1000
>              UART0 Local Port: 2000
>        UART0 Serial Baud Rate: 9600
>         UART0 Serial Settings: 1 stop bit, parity: None, 8 data bits
>          UART0 Serial Timeout: 0*5 ms
>  
>                    UART1 Mode: UDP Server
>               UART1 Target IP: 192.168.1.100
>             UART1 Target Port: 2000
>              UART1 Local Port: 3000
>        UART1 Serial Baud Rate: 9600
>         UART1 Serial Settings: 1 stop bit, parity: None, 8 data bits
>          UART1 Serial Timeout: 0*5 ms

Power off the unit and remove the jumper.


## RST Pin

(Differentiated from the Reset Jumper, which restores Network settings to factory defaults)
    
    RST = Pin(17, Pin.OUT,Pin.PULL_UP)  #CH9121 external reset input pin, low active

    RST.value(0)                        #CH9121 external reset input pin 17, (0 active, 1 inactive)

The RST pin, when given a value of 0, produces the following results for the duration of the reset:
- CH9121 running status indicator led goes off. **(Image #3)**
- CH9121 power indicator led remains on. **(Image #4)**
- The left and right lights on the CH9121 RJ45 connector go off. **(Image #8)**
- On an external Switch the attached port usually shows a yellow blinking light indicating 100M/10M speed with activity. During a RST this light is off.

![The Board](/images/Pico-ETH-CH9121-Board.jpg#center)

- Pico TX GPIO0 and GPIO4 remain high (value 1).
- Pico RX GPIO1 and GPIO5 go low (value 0).
- Pico Config GPIO14 remains high (value 1).
- Pico Reset GPIO17 remains low (value 0).

![The Board](/images/Pico-ETH-CH9121-Pinout.jpg#center)

After a RST running the *CH9121_read_chip_settings.py* file shows that the user configuration settings are still in CH9121 memory. Wireshark confirms the CH9121 is still using its last configurations even after RST. The RST severs and resets active ethernet connections to the chip.


## UDP Server Mode
Starting from a freshly Reset Pico-ETH-CH9121 chip I changed the following parameters only, before running the *parameters...py* file:

>                        UART0_MODE = 2 

*Read_Settings.py* shows this new change:

>                        UART0 Mode: UDP Server
>        UART0 TCP Client Connected: TCP Disconnected
>                   UART0 Target IP: 255.255.255.255
>                 UART0 Target Port: 1000
>                  UART0 Local Port: 2000
>            UART0 Serial Baud Rate: 9600
>             UART0 Serial Settings: 1 stop bit, parity: None, 8 data bits
>              UART0 Serial Timeout: 0*5 ms

**UDP Server Mode** automatically overwrites the Target_IP for that Uart channel to **255.255.255.255**. 

You can set a Python socket to write to an IP such as 192.168.0.255 or 192.168.1.255 to reach this broadcast address. You can also configure a second Pico_Eth_CH9121 in UDP Client Mode with a Target_IP such as 192.168.0.255 or 192.168.1.255 to reach the first Pico in UDP Server Mode.

Use of the **\x34 command** disables the auto assignment of 255.255.255.255 while in UDP Server Mode. This is the *DEVICE_NAME* constant in the Parameter...py file, or the *devicename* variable in the CH9121.py Class. 

    uart0.write(b'\x57\xab\x34'+DEVICE_NAME) #CH9121 set network device name (maximum length 28 bytes) (Optional)

Setting this value to *DEVICE_NAME = b''* restores the auto assignment of 255.255.255.255 while in UDP Server Mode. 

    DEVICE_NAME = b''


## Summary 

I recommend the use of this breakout board to confirm GPIO pin usage by LED. It has been very helpful towards this project.

https://www.amazon.com/FREENOVE-Breakout-Raspberry-Terminal-Shield/dp/B0BFB53Y2N/ref=sr_1_3?crid=277Y10PM3UV1E&keywords=freenove+pico+breakout+board&qid=1674280060&sprefix=freenova+pico+breakout+boar%2Caps%2C125&sr=8-3

As I understand it the CH9121 is supposed to wrap the UART write data in TCP/IP addressing information, before forwarding it onto the target IP address & port. It then strips the TCP/IP off incoming data before sending it via UART to the Pico. 

I am developing this software for use having a Pico communicate to a Rpi4B over a LAN. Ultimately I need two Picos as clients to a Rpi4B server over PoE switcher, as a stand alone LAN. This requires data transfer from Micropython UART commands to Python sockets and back. I'll update this repository as the communications software is developed and tested. 
