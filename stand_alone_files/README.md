# Stand Alone *Congfig* & *Read* micropython files

![The Board](/images/Pico-ETH-CH9121.jpg#center)


## Installation & Configuration

Copy *CH9121config.py* to the */lib* directory of your Pico. Create that directory in Thonny if not already present. 

https://thonny.org/

Within Thonny adjust the constants with your prefered network settings for the CH9121. IP addresses are a Micropython List.

> UART0_MODE        = 1               # Mode 0:TCP Server, Mode 1:TCP Client, Mode 2:UDP Server, Mode 3:UDP Client
>    
> UART0_TARGET_IP   = (192,168,1,100) # TARGET_IP of destination
>    
> UART0_TARGET_PORT = 1000            # TARGET_PORT of destination
>    
> UART0_LOCAL_PORT  = 2000            # LOCAL_PORT of UART0, each uart shares local IP but has a unique port, maximum 65535
>    
> UART0_BAUD_RATE   = 115200          # BAUD_RATE of UART0 serial Port  

To save your network preferences into the CH9121 chip once powered add this to *main.py*:

    import CH9121config

*CH9121read.py* should be run from Thonny with the Pico attached when you are curious about the current network settings of your CH9121 device. 
The read file does not need to be part of *main.py*, nor stored in */lib*. Just run it when you need to check. It outputs to the Thonny terminal, and to a text file saved to the Pico: *CH9121config.txt*.

To incorporate a read into your *main.py* startup copy *CH9121read.py* into the Pico's */lib* directory. Then add this to *main.py*:

    from time import sleep    
    import CH9121config
    sleep(10) #Can take the CH9121 up to 10 seconds to fully connect
    import CH9121read

The Pico_ETH_CH9121 can be pinged from another computer on the LAN when the network settings are correct. And the *CH9121read.py* file confirms that your Pico UART0 is set up properly for RX & TX with the CH9121 when it outputs data.

