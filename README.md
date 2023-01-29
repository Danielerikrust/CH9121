# CH9121
Micropython files for the Waveshare Pico_ETH_CH9121 ethernet hat for Raspberry Pi Pico.

These files incorporate the full range of commands provided in:

https://www.waveshare.com/w/upload/e/ef/CH9121_SPCC.pdf

https://www.waveshare.com/wiki/Pico-ETH-CH9121

Place Serial_Port_Parameter_Configuration_Full.py to the /lib directory of your Pico. Create that directory in Thonny if not already present. Add "import Serial_Port_Parameter_Configuration_Full" to main.py. This saves the network preferences into the CH9121 chip while powered. 

https://thonny.org/

Adjust your network settings with the variables. IP addresses are separated by comma and not periods as a micropython list. To find your gateway & subnet mask your router will usually have a sticker with a router loggin such as http://routerlogin.net. It will also show the default login & password. While in routerlogin.net search for gateway & submask, and assign your CH9121 the same static IP you assinged in the configuration variables. Otherwise your routers DHCP will try to assign it a random IP address. DHCP support can be enabled on the CH9121 with the parameter configuration file if desired, line 57. 

Interestingly, setting UART0 or UART1 to "Mode 3-UDP Server" will automatically set the Local_IP for that UART to 255.255.255.255. A workaround is to set the Target_IP of the client to *.255, such as 192.168.0.255.

CH9121_read_chip_settings.py should also be run from Thonny with the Pico attached. The read file also does not need to be part of main.py, nor stored in /lib. Just run it when you need to check. It incorporates the full range of read options laid out in:

https://www.waveshare.com/w/upload/e/ef/CH9121_SPCC.pdf

You can verify the read CH9181 Mac address against your routerlogin.net listing associated with the expected CH9121 IP address.

The Pico_ETH_CH9121 can be pinged from another computer on the LAN when the network settings are correct. And the read_chip_settings.py file confirms that UART0 is set up properly for RX & TX with the CH9121 when it outputs data.

I recommend the use of this breakout board to confirm GPIO pin usage by LED. It has been very helpful towards this project.

https://www.amazon.com/FREENOVE-Breakout-Raspberry-Terminal-Shield/dp/B0BFB53Y2N/ref=sr_1_3?crid=277Y10PM3UV1E&keywords=freenove+pico+breakout+board&qid=1674280060&sprefix=freenova+pico+breakout+boar%2Caps%2C125&sr=8-3

As I understand it the CH9121 is supposed to wrap the UART write data in TCP/IP addressing information, before forwarding it onto the target IP address & port. It then strips the TCP/IP off incoming data before sending it via UART to the Pico. This requires data transfer from Micropython to Python and back. 

I am developing this software for use having a Pico communicate to a Rpi4B over a LAN. Ultimately I need two Pic's as clients to a Rpi4B server over PoE switcher, as a stand alone LAN. I'll update this repository as the communications software is developed and tested. 
