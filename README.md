# CH9121
Software for the Waveshare Pico_ETH_CH9121

Micropython files for the Waveshare Pico_ETH_CH9121 ethernet hat for Raspberry Pi Pico.

These files incorporate the full range of commands provided in:

https://www.waveshare.com/w/upload/e/ef/CH9121_SPCC.pdf

https://www.waveshare.com/wiki/Pico-ETH-CH9121

Serial_Port_Parameter_Configuration_Full.py need only be run once in Thonny with the Pico attached. This saves the network preferences into the CH9121 chip firmware. No need to place this file into Pico/lib nor run it each time as part of main.py.

https://thonny.org/

Adjust your network settings with the variables. IP addresses are separated by comma and not periods as a micropython list. To find your gateway & subnet mask your router will usually have a sticker with a router loggin such as http://routerlogin.net. It will also show the default login & password. at routerlogin.net assign your CH9121 the same static IP you assinged in the configuration variables. Otherwise your routers DHCP will try to assign it a random IP address. DHCP support can be enabled on the CH9121 with the parameter configuration file if desired, line 57.

CH9121_read_chip_settings.py should also be run from Thonny with the Pico attached. It incorporates the full range of read options laid out in:

https://www.waveshare.com/w/upload/e/ef/CH9121_SPCC.pdf

