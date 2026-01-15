# py.console
A gaming console based on a Raspberry Pi 5 and python games with 5 bluetooth-controllers
I designed the 3D-printed parts in Fusion360, the schematics and the PCB in KiCAD.

# HARDWARE


## CONSOLE

<img width="3680" height="1946" alt="Console rendering" src="https://github.com/user-attachments/assets/81589308-efee-4d1a-85b0-49d5695bfe2d" />

The console is based on a Raspberry Pi 5. The 3D-printed housing (12cm x 12cm) includes two parts. The main part holds all the components and electronics.
The top view looks like this:
<img width="941" height="920" alt="Bildschirmfoto 2026-01-09 um 21 03 50" src="https://github.com/user-attachments/assets/cb72cb26-5ad3-4fab-8eb3-12751fa76929" />

On the left side of this picture the Raspberry Pi will be mounted using four pieces that fit into its mounting holes. The HDMI-Ports and the USB-C-Ports are accessible from the back side of the console.
On the sides I designed some holes for the air outlet of the device. 
<img width="1293" height="765" alt="Bildschirmfoto 2026-01-09 um 20 36 10" src="https://github.com/user-attachments/assets/69851521-1fd6-4705-a60f-349a17f50270" />

On the front are two holes for a USB port and a boot push button. 
The USB port is connected to the USB port of the Raspberry Pi. It will be used to connect a USB stick with the .py game files.
The wires of the push button are connected to the two pins next to the battery connector on the Raspberry Pi to act like the integrated button.
The button has an integrated LED that is connected to GPIO13 with a resistor in series to be enabled when the device is operating.
An active buzzer is connected to GPIO18 to make a sound when booting or starting a game. It is placed in the hole of the case.


The other housing part is the top cover.
<img width="877" height="862" alt="Bildschirmfoto 2026-01-09 um 21 09 07" src="https://github.com/user-attachments/assets/56064fc5-19a0-4ec2-9a03-c87bc5746013" />

It is mounted with two screws on the front and round pieces that fit into holes in the main part at the back.
<img width="1267" height="532" alt="Bildschirmfoto 2026-01-09 um 21 11 52" src="https://github.com/user-attachments/assets/3cc04dc4-5abc-4ab5-af41-973c46149567" />

I will use the Raspberry Pi active cooler that takes air through the holes in the top cover.

https://github.com/user-attachments/assets/2c3ed64f-fc42-457b-9e3d-2fc4b27291a0

*This video shows how the mounting will work*

## CONTROLLERS

The controllers are more complicated as they are smaller and include more components.
I build five of them because a lot of things are shipped in five or ten, including PCBs, Joysticks, buttons, batteries etc. .

<img width="1294" height="791" alt="Bildschirmfoto 2026-01-14 um 21 28 14" src="https://github.com/user-attachments/assets/63d5447f-b005-4498-b59d-922dd42a5e05" />

The rendering doesn't include the joystick because I don't print it by myself.

<img width="1589" height="856" alt="Bildschirmfoto 2026-01-06 um 15 12 12" src="https://github.com/user-attachments/assets/bf905f9f-2cb0-4e01-8a10-0b906bda28fb" />

The microcontroller is a XIAO-ESP32-C3 that has BLE and a battery charger and it is small. Its USB-C port is the charging port of my controller.

At the left side is a tipical thumb joystick and at the right side two buttons. They are connected to inputs on the ESP32 and GND.
Around the PCB are 20 "PL9823" LEDs. They need 5 volts which the ESP32 doesn't deliver. So, I use a little boost converter from the battery cell to five volts and a 74125 level shifter (with a 330Ω resistor) for the data. A MOSFET turnes the boost converter off when the ESP32 is in DeepSleep.
Two capacitors deliver high current for the LEDs for a short time.
The battery voltage is measured by splitting it in half using two resistors 1MΩ

The device is 12cm x 5cm, rounded at the sides and around 26mm thick. The case is made like the one of the console, but the cover is at the opposite side. The PCB is held between these two parts.
The main part holds the battery in the middle and the "keycaps" at the right side OF THE DEVICE.
<img width="1233" height="647" alt="Bildschirmfoto 2026-01-06 um 18 56 03" src="https://github.com/user-attachments/assets/eeafa166-22e9-4303-8421-8d10189178a7" />

The "keycaps" just fit into their holes and have a margin to prevent falling out.
<img width="916" height="787" alt="Bildschirmfoto 2026-01-06 um 18 56 38" src="https://github.com/user-attachments/assets/2a1fcb81-f940-498f-9ac3-37c56f118753" />

The cover is screwed into the main case at the sides. It holds the PCB at the edges, under the joystick and under the keys for pressure, leaving a bit of space for the solder joints.


## BOM

CONSOLE:

• Raspberry Pi 5, 4GB RAM  -  103,82€

• Power supply for Pi 5  -  1,87€

• Raspberry Pi 5 active cooler  -  3,09€

• USB-A port  -  3,04€

• push button, 16mm mounting hole  -  0,87€

• blue PLA (also for the controllers)  -  15,19€

• active buzzer, 24mm Ø  -  /

• 330Ω resistor  -  /

• microSD-card  -  16,95€

TOTAL PRICE CONSOLE: 144,83€


CONTROLLERS:

• 5pcs PCB, 112mm*46mm  -  ≈15€ (including spedition)

• 5pcs Seeed Studio XIAO-ESP32-C3  -  27,55€

• 5pcs thumb joystick  -  0,87€

• 10pcs silent push button, 8*8mm  -  0,86€

• 10pcs LiPo battery, 30mm* 40mm* 5mm  -  16,88€

• 5pcs voltage regulator  -  2,53€

• 5pcs 74125 level shifter  -  1,02€

• 5pcs 330Ω resistor  -  /

• 10pcs 1MΩ resistor  -  /

• 10pcs 100nF capacitor  -  0,87€

• 5pcs polarized capacitor  -  0,87€

• 100pcs PL9823 LED  -  5,50€

• 5pcs MOSFET (IRLZ44N)  -  0,70€

TOTAL PRICE 5 CONTROLLERS: 72,65€

# SOFTWARE


## CONSOLE

The console uses the Raspberry Pi Desktop. After booting, a menu appears. It shows python files saved on the external USB stick and uses pygame for the graphics.
The idea behind this project: All of the other software are some python games on a USB stick. I can code them by myself or download them from the internet - as many as I want!

## CONTROLLERS

The controllers are coded in C++ and use ESP32 bleGamepad library. They use DeepSleep to be shut down by pressing the joystick for 5 seconds or by inactivity. Pressing the Joystick will wake the ESP32 up.
The code includes a lot of animations for the LEDs, using fastLED library. The battery level is calculated using the measured battery voltage and a table from the web. It is sent every 20 seconds to the connected device and displayed on the LEDs when starting and if it is under 20%.
