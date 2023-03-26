# CH9121

Micropython files for the Waveshare **Pico_ETH_CH9121** ethernet hat for Raspberry Pi Pico, and Waveshare **2-Ch_Uart_to_Eth** board. These cover configuring the CH9121 chip, reading existing settings, and Pico software to get up and running.

![The Board](/images/Pico-ETH-CH9121.jpg#center)

These files incorporate the full range of commands provided in:

https://www.waveshare.com/w/upload/e/ef/CH9121_SPCC.pdf

https://www.waveshare.com/wiki/Pico-ETH-CH9121

I'd like to give special acknowledgment to **SplashAudio** for his early work on the CH9121 chip which set the stage for this Repository. Thank you.

https://github.com/Splashaudio/Pico-ETH-CH9121_basic


## Installation

Copy *CH9121.py* to the */lib* directory of your Pico. Create that directory in Thonny if not already present. 

https://thonny.org/

Copy *mainForPico.py* to the root directory of the Pico. It may be renamed *main.py* once it is configured.

# Software

*CH9121_Demo.py* demonstrates using the **CH9121 Class** for Rpi Pico. It shows how to adjust network parameters and reconfigure the CH9121 within your code on the fly. After changing any network setting the `eth.config()`function must be run to import them into the device:

    eth.u0mode       = 2                  # Mode 0:TCP Server, Mode 1:TCP Client, Mode 2:UDP Server, Mode 3:UDP Client
    eth.u0targetip   = (192,168,0,123)
    eth.config()

*CH9121_Demo2.py* shows how to use the CH9121 after having adjusted all the constants within the *CH9121.py* file. This method is recommended if your Pico maintains consistent network settings.

*mainForPico.py* is the working software for the Pico-ETH-CH9121 hat. The write and read functions are set to Timers instead of interrupts. As a PLC the Pico has great usage performing second by second routines. You can connect two CH9121 Picos over a LAN. Set one to a server mode, and the other to a client mode and they will communicate their internal temperatures by Timed read & writes. Set the Timers to whatever period you wish. Perhaps write second by second `PERIOD=1000`, and read for new data every tenth of a second `PERIOD=100`. 

UDP and TCP modes are both accomodated with this software. Simply change the network parameters and Mode for your application and start. For a LAN it is workable to use the local IP of the device also as the Gateway IP.

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

Then, upon repowering the unit the *CH9121read.py* confirmed factory reset to the chip parameters.

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

![Board Hardware](/images/Pico-ETH-CH9121-Board.jpg#center)

- Pico TX GPIO0 and GPIO4 remain high (value 1).
- Pico RX GPIO1 and GPIO5 go low (value 0).
- Pico Config GPIO14 remains high (value 1).
- Pico Reset GPIO17 remains low (value 0).

![Pinout](/images/Pico-ETH-CH9121-Pinout.jpg#center)

After a RST running *CH9121read.py* shows that the user configuration settings are still in CH9121 memory. Wireshark confirms the CH9121 is still using its last configurations even after RST. The RST severs and resets active ethernet connections to the chip.


## TCP Modes & Connection Status LEDs

The board has two led's which indicate a TCP connection. - **(Image #1 & 2)**

These are listed as:

>    1. UART 2 connection indicator
>    2. UART 1 connection indicator

It is more applicable to label these leds as:

>    1. UART 1 TCP connection indicator (CH2 LED)
>    2. UART 0 TCP connection indicator (CH1 LED)
  
![Board Hardware](/images/CH9121_WhatsOnBoard.png#center)

These leds are unresponsive in either UDP mode. In TCP modes these leds only light up once a connection has been established.

For my own project I will be networking a pair of Picos to a Raspberry Pi 4B, along with several ethernet connected analyzers providing real time data. As such I have a pair of Picos for use to experiment with the Pico-ETH-CH9121. These have 20x4 LCD screens attached for addition communication while I'm off Thonny. I call them 81 & 91.

![Pair of Picos](/images/dualPicos2.jpg#center)

In the picture both uarts of 81 are set to TCP Server Mode. And both channels of 91 are set to TCP Client Mode.

Using *CH9121read.py* reveals the following for Pico 81:

>           CH9121 Local IP: 192.168.0.81
>                *CH9121 UART0 Settings*
>                UART0 Mode: TCP Server
>          UART0 TCP Status: TCP Disconnected (TCP LED CH1 is OFF)
>           UART0 Target IP: 192.168.0.91
>         UART0 Target Port: 9100
>          UART0 Local Port: 8100
>          
>                *CH9121 UART1 Settings*
>                     UART1: Enabled
>                UART1 Mode: TCP Server
>          UART1 TCP Status: TCP Connected  (TCP LED CH2 is ON)
>           UART1 Target IP: 192.168.0.91
>         UART1 Target Port: 9101
>          UART1 Local Port: 8101

Using *CH9121read.py* reveals the following for Pico 91:

>           CH9121 Local IP: 192.168.0.91
>                *CH9121 UART0 Settings*
>                UART0 Mode: TCP Client
>          UART0 TCP Status: TCP Connected (TCP LED CH1 is ON)
>           UART0 Target IP: 192.168.0.81
>         UART0 Target Port: 8100
>          UART0 Local Port: 9100
>          
>                *CH9121 UART1 Settings*
>                     UART1: Enabled
>                UART1 Mode: TCP Client
>          UART1 TCP Status: TCP Connected (TCP LED CH2 is ON)
>           UART1 Target IP: 192.168.0.81
>         UART1 Target Port: 8101
>          UART1 Local Port: 9101

However, both UART0 and UART1 on Pico 81 are actually reading the correct data sent from Pico 91. It appears that the CH9121 chip merges connections from TCP clients down to a single active TCP server connection on UART 1, And so only the CH2 LED is active. The CH9121 chip then redistributes incoming data from different ports to the corresponding UART.

I reason it does this intentionally, to leave UART0 open for querry commands without interrupting an active connection. These include commands such as:

    command .write(b'\x57\xab\x03') = uart0 TCP connection status
    command .write(b'\x57\xab\x04') = uart1 TCP connection status
    command .write(b'\x67\xab\x03') = number of TCP reconnections

Experimentation shows that we can set both Uarts on Pico 91 to have identical target ports. These will both connect to the same Uart1 local port on Pico 81. This strategy also leaves Uart 0 open for real time querries. I will experiment with these real time querries to validate the hypothesis.

    eth.u0targetport = 4000
    eth.u1targetport = 4000

We can establish the following hardware & software associations:

>     command .write(b'\x57\xab\x03') = uart0 TCP connection status = TCPCS1 (CH9121 chip pin 30) = CH1 LED
>     
>     command .write(b'\x57\xab\x04') = uart1 TCP connection status = TCPCS2 (CH9121 chip pin 33) = CH2 LED

Use of the **\x34 command** disrupts TCP connectivity. This is the *DOMAIN_NAME* constant in the *CH9121config.py* file, or the *domainname* variable in the *CH9121.py* Class. 

    uart0.write(b'\x57\xab\x34'+DOMAIN_NAME) #CH9121 set network device name (maximum length 28 bytes) (Optional)

Setting this value to *DOMAIN_NAME = b''* restores TCP connectivety to the chip.

    DOMAIN_NAME = b''


## UDP Server Mode
Starting from a freshly Reset Pico-ETH-CH9121 chip I changed the following parameters only, before running the *CH9121config.py* file:

>                        UART0_MODE = 2 

*CH9121read.py* shows this new change:

>                        UART0 Mode: UDP Server
>                   UART0 Target IP: 255.255.255.255
>                 UART0 Target Port: 1000
>                  UART0 Local Port: 2000
>            UART0 Serial Baud Rate: 9600
>             UART0 Serial Settings: 1 stop bit, parity: None, 8 data bits
>              UART0 Serial Timeout: 0*5 ms

**UDP Server Mode** automatically overwrites the Target_IP for that Uart channel to **255.255.255.255**. 

Use of the **\x34 command** disables the auto assignment of 255.255.255.255 while in UDP Server Mode. This is the *DOMAIN_NAME* constant in the *CH9121config.py* file, or the *domainname* variable in the *CH9121.py* Class. 

    uart0.write(b'\x57\xab\x34'+DOMAIN_NAME) #CH9121 set network device name (maximum length 28 bytes) (Optional)

Setting this value to *DOMAIN_NAME = b''* restores the auto assignment of 255.255.255.255 while in UDP Server Mode. 

    DOMAIN_NAME = b''
    
# Troubleshooting

## Wireshark for Troubleshooting

The Pico-Eth-CH9121 wraps UART write data in TCP/IP addressing information, before forwarding it onto the target IP address & port. It then strips the TCP/IP headers off incoming data before sending it via UART to the Pico.

As such, much of the chips functionality is hidden. The chip is intended to be an invisible component. However, it happens that the chip can be undertaking its own functions and become stuck or trapped, quite unknown to the Pico. The Pico merrily continues on its way performing reads & writes, never knowing that none of these communications have ever been executed past the CH9121. Even the active querries generated through Uart 0 can only provide a limited understanding of how or why the chip may get stuck.

I have found it essential to use [Wireshark](https://www.wireshark.org/download.html) software when debugging this chip. This software is free and can show you what the CH9121 is doing in the TCP/IP layers of your network. After a short learning curve you'll be able to identify your Pico device and see the sorts of things it is doing on your network. You'll also be able to see the loops it gets stuck in. This is how the 192.168.1.100 void was discovered.

> Wireshark® is a network protocol analyzer. It lets you capture and interactively browse the traffic running on a computer network. It has a rich and powerful feature set and is world’s most popular tool of its kind. It runs on most computing platforms including Windows, macOS, Linux, and UNIX. Network professionals, security experts, developers, and educators around the world use it regularly. It is freely available open source, and is released under the GNU General Public License version 2.

The Pico-Eth-CH9121 initially shows up in Wireshark SOURCE as "JiangsuQ_", followed by the last 3 numbers of its MAC address. `JiangsuQ_44:ec:2b` Once a connection has been established the device will have the SOURCE of its Local IP. Here is a screen shot of two CH9121 devices forming a TCP connection. These have local IPs of 192.168.0.91 (`JiangsuQ_44:ec:2b`) & 192.168.0.81 (`JiangsuQ_44:ec:0e`). Once you know what to look for it is easy to determine what each device is doing in the background, one packet at a time.

![Wireshark Software](/images/Wireshark.png#center)

[Wireshark](https://www.wireshark.org/download.html)

## Gateway while on LAN

It has been found that the pico-ETH-CH9121 will continue to search for a true gateway when it is installed in a stand alone LAN. In some cases it will not allow other connections to go forward until the gateway has been found. If no gateway to the external internet exists, or if your device will never be contacting the external internet then set the gateway the same as the local IP. In this mode the CH9121 chip will automatically locate itself and then no longer seek any further gateway functions.

    eth.localip      = 192.168.0.91
    eth.gateway      = eth.localip

## Connection Times

I have found it takes 5-10 seconds for the Pico-Eth-CH9121 to establish a connection with its terget IP after power on, or at the end of a `eth.config()`. It may be wise to establish a micropython sleep period before entering the main part of your code, to allow for this connection to be established.

   sleep(10)

## The 192.168.1.100 Void

Rarely the CH9121 has been found to lock up into its default values. In particular it can get stuck trying to locate a target IP of `192.168.1.100`, despite having something on the order of `eth.u0targetip = 192.168.0.50`. Being stuck trying to locate this phantom address the CH9121 will not allow other connections to be established. Once this IP address has been located the chip will continue with its desired connections.

You may assign some neutral network device the IP of `192.168.1.100`, such as a Managed Switch. Or a reset of the chip using the Reset Jumper, followed by a renewed `eth.config()`. Either route may unstick it. 

## The Domain Name Paradox

Use of the **\x34 command** disables a number of features on the chip. This is the *DOMAIN_NAME* constant in the *CH9121config.py* file, or the *domainname* variable in the *CH9121.py* Class. 

    uart0.write(b'\x57\xab\x34'+DOMAIN_NAME) #CH9121 set network device name (maximum length 28 bytes) (Optional)

I have found no usage of this command which does anything other than disable the chip from proper function. Perhaps it has a use, but it is recommended to leave this setting at the null value of *DOMAIN_NAME = b''*. Experimentation may reveal proper use of this command for advanced applications. Otherwise leave it null.

    DOMAIN_NAME = b''

# Summary 

I am developing this software for use having several Picos communicate to a Rpi4B over a LAN. Ultimately I need two Picos as clients to a Rpi4B server over PoE switcher, as a stand alone LAN. This requires data transfer from Micropython UART commands to Python sockets and back. I'll update this repository as the communications software is developed and tested. 

I recommend the use of this [Freenove Breakout Board for Pico](https://www.amazon.com/FREENOVE-Breakout-Raspberry-Terminal-Shield/dp/B0BFB53Y2N/ref=sr_1_3?crid=277Y10PM3UV1E&keywords=freenove+pico+breakout+board&qid=1674280060&sprefix=freenova+pico+breakout+boar%2Caps%2C125&sr=8-3
) to confirm GPIO pin usage by LED. It has been very helpful towards this project.

![The Board](/images/Freenove_Breakout_Board.jpg#center)
