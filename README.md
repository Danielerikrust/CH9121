# CH9121
Micropython files for the Waveshare Pico_ETH_CH9121 ethernet hat for Raspberry Pi Pico, and Waveshare 2-Ch_Uart_to_Eth board.

These files incorporate the full range of commands provided in:

https://www.waveshare.com/w/upload/e/ef/CH9121_SPCC.pdf

https://www.waveshare.com/wiki/Pico-ETH-CH9121

## Installation

Copy *Serial_Port_Parameter_Configuration_Full.py* to the /lib directory of your Pico. Create that directory in Thonny if not already present. To save the network preferences into the CH9121 chip while powered add this to *main.py*.

    import Serial_Port_Parameter_Configuration_Full

https://thonny.org/

*CH9121_read_chip_settings.py* should also be run from Thonny with the Pico attached. The read file also does not need to be part of main.py, nor stored in /lib. Just run it when you need to check. It incorporates the full range of read options laid out in:

https://www.waveshare.com/w/upload/e/ef/CH9121_SPCC.pdf

## Configuration

Adjust your network settings with the variables in *Serial_Port_Parameter_Configuration_Full.py*. IP addresses are separated by comma and not periods as a micropython list. To find your gateway & subnet mask your router will usually have a sticker with a router loggin such as http://routerlogin.net or its IP Address. It will also show the default login & password. While in the router admin search for its gateway & submask, and assign your CH9121 the same static IP you assinged in the configuration variables. Otherwise your routers DHCP will try to assign it a random IP address. DHCP support can be enabled on the CH9121 with the parameter configuration file if desired. 

You can verify the CH9121 Mac address generated from *CH9121_read_chip_settings.py* against your router admin listing associated with the expected CH9121 IP address.

The Pico_ETH_CH9121 can be pinged from another computer on the LAN when the network settings are correct. And the *CH9121_read_chip_settings.py* file confirms that your Pico UART0 is set up properly for RX & TX with the CH9121 when it outputs data.

## Summary 

I recommend the use of this breakout board to confirm GPIO pin usage by LED. It has been very helpful towards this project.

https://www.amazon.com/FREENOVE-Breakout-Raspberry-Terminal-Shield/dp/B0BFB53Y2N/ref=sr_1_3?crid=277Y10PM3UV1E&keywords=freenove+pico+breakout+board&qid=1674280060&sprefix=freenova+pico+breakout+boar%2Caps%2C125&sr=8-3

As I understand it the CH9121 is supposed to wrap the UART write data in TCP/IP addressing information, before forwarding it onto the target IP address & port. It then strips the TCP/IP off incoming data before sending it via UART to the Pico. 

I am developing this software for use having a Pico communicate to a Rpi4B over a LAN. Ultimately I need two Picos as clients to a Rpi4B server over PoE switcher, as a stand alone LAN. This requires data transfer from Micropython UART commands to Python sockets and back. I'll update this repository as the communications software is developed and tested. 
