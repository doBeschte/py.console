# py.console
A gaming console based on a Raspberry Pi 5 and python games with 5 bluetooth-controllers

# CONSOLE
The console is based on a Raspberry Pi 5. The 3D-printed housing includes two parts. The main part holds all the components and electronics.
The top view looks like this:
<img width="1143" height="959" alt="Bildschirmfoto 2026-01-08 um 20 00 13" src="https://github.com/user-attachments/assets/aec2fac6-4dd1-4b35-af99-34352dc48da1" />

On the top right the Raspberry Pi will be mounted using four pieces that fit into its mounting holes. The HDMI-Ports and the USB-C-Ports are accessible from the back side of the console.
On the sides I designed some holes for the air outlet of the device. 
<img width="1293" height="765" alt="Bildschirmfoto 2026-01-09 um 20 36 10" src="https://github.com/user-attachments/assets/69851521-1fd6-4705-a60f-349a17f50270" />

On the front are two holes for a USB port and a boot push button. 
The USB port is connected to the USB port of the Raspberry Pi. It will be used to connect a USB stick with the .py game files.
The wires of the push button are connected to the two pins next to the battery connector on the Raspberry Pi to act like the integrated button.
The button has an integrated LED that is connected to GPIO13 with a resistor in series to be enabled when the device is operating.
An active buzzer is connected

Raspberry Pi 5
USB
push button
USB-stick
Resistors
