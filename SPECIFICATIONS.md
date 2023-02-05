# CH9121 Specifications
Specifications for the Waveshare Pico_ETH_CH9121 ethernet hat for Raspberry Pi Pico, and Waveshare 2-Ch_Uart_to_Eth board.

## Default Parameters

Uart 1 is disabled, and Uart 0 works in *TCP CLIENT* mode by default.
Configuration of the CH9121 must be conducted through Uart 0, at 9600 baud.

The default network parameters of the CH9121
- Device/Local IP: 192.168.1.200
- Subnet mask: 255.255.255.0

The default parameters of CH9121 Uart 0:
- Device/Local port: 2000
- Target IP: 192.168.1.100
- Target port: 1000

The default serial parameters of CH9121 Uart 0 & Uart 1 (These match default Pico parameters, except baud):
- Baud rate: 9600
- Timeout: 0
- Data bit: 8
- Stop bit: 1
- Parity bit: None
- Clear buffer: Never

## Reset Pin

    RST = Pin(17, Pin.OUT,Pin.PULL_UP)  #CH9121 external reset input pin, low active

    RST.value(0)                        #CH9121 external reset input pin 17, (0 active, 1 inactive)

The reset pin, when given a value of 0, produces the following results for the duration of the reset:
- CH9121 running status indicator led goes off. **(Image #3)**
- CH9121 power indicator led remains on. **(Image #4)**
- The left and right lights on the CH9121 RJ45 connector go off. **(Image #8)**
- On an external Switch the attached port usually shows a yellow blinking light indicating 100M/10M speed with activity. During a Reset this light is off.

![The Board](/images/Pico-ETH-CH9121-Board.jpg#center)

- Pico TX GPIO0 and GPIO4 remain high (value 1).
- Pico RX GPIO1 and GPIO5 go low (value 0).
- Pico Config GPIO14 remains high (value 1).
- Pico Reset GPIO17 remains low (value 0).

![The Board](/images/Pico-ETH-CH9121-Pinout.jpg#center)

After a Reset running the CH9121_read_chip_settings.py file shows that the user configuration settings are still in CH9121 memory. Wireshark confirms the CH9121 is still using its last configurations even after a reset.


## UDP Server Mode

This mode automatically overwrites the Local_IP for that Uart channel to 255.255.255.255. You can set a Python socket to write to an IP such as 192.168.0.255 or 192.168.1.255 to reach this broadcast address. You can also configure a second Pico_Eth_CH9121 in UDP Client Mode with a Target_IP such as 192.168.0.255 or 192.168.1.255 to reach the first Pico in UDP Server Mode.
