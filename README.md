# CTRL-AI-Macropad
<img width="1419" height="571" alt="Screenshot 2025-12-28 222231" src="https://github.com/user-attachments/assets/f7881569-19a2-49f7-9838-46889130ec1f" />

## What is CTRL?
CTRL is a custom-built programmable macropad designed for productivity,
automation, and future AI-assisted workflows. It features mechanical
switches, a rotary encoder, and an IPS display, powered by a Raspberry Pi Pico.
<p align="center">
  <img src=https://github.com/user-attachments/assets/c879a765-367e-4b05-86a0-af208b819c26>

-------------------------------------------------------------------------------------------------
## Purpose 
I wanted to design a fully custom keyboard input device from scratch — including
PCB design, firmware, and enclosure — to better understand hardware design
and embedded systems. This project is also built with future software
customization & productivity in mind , ensuring optimization of the project

 <p align="center">
  <img src="https://github.com/user-attachments/assets/4551a615-e77e-4ec2-b289-c4d70b81c0fa">
</p>

-------------------------------------------------------------------------------------------------
## Features
- 6 mechanical keys (Cherry MX compatible)
- Rotary encoder with push button
- IPS SPI display
- Raspberry Pi Pico (RP2040)
- Fully custom PCB
- Open-source hardware & firmware
-------------------------------------------------------------------------------------------------
## Hardware
- PCB designed using **KiCad** (open-source) and **Fusion 360**
- 2-layer PCB
- Diode-protected key matrix
- SPI-connected IPS display

All PCB source files are available in `/hardware/kicad`.

<p align="center">
  <img src="https://github.com/user-attachments/assets/b63ff671-658b-4ba5-a15d-6402b3deaaeb">
</p>

-------------------------------------------------------------------------------------------------

## Firmware
The firmware is written using **KMK** and **CircuitPython**.

Currently supported:
- Basic key mapping
- Rotary encoder input

Planned features:
- Dynamic key remapping
- Software-based configuration tool
- Display-driven UI

Firmware files are located in `/firmware`.

-------------------------------------------------------------------------------------------------
## Case
The enclosure is designed in Fusion 360 (personal use).
[STEP and source files are included in `/case`.] The length of the macropad/hackpad is 11.8 cm, 
and the height is 6.3 cm and it has a thickness of 1.5 cm. 
The enclosure is designed to be 3D printed.

~ **Recommended filament:** PLA  
PLA provides good dimensional accuracy, clean surface finish, and is easy to print, making it ideal for prototyping and desktop devices.

~ **Alternative:** PETG  
PETG can be used for improved durability and heat resistance, though it may require tuning for small cutouts.

[The enclosure is intended for indoor use and does not require high-temperature or impact-resistant materials.]

<p align="center">
  <img src="https://github.com/user-attachments/assets/2931899d-0f27-4e3b-9777-3a29c8599f60">
</p>

-------------------------------------------------------------------------------------------------
## Images
<img width="1139" height="808" alt="Pcb" src="https://github.com/user-attachments/assets/395aed8f-0ed4-41ae-b612-e8b5305dca23" />

<img width="803" height="557" alt="assembled-case" src="https://github.com/user-attachments/assets/95c67418-6ab1-4e1c-b6ce-ca660ebd0613" />

-------------------------------------------------------------------------------------------------

## Future AI Integration (Planned)
CTRL is designed to support future AI-assisted workflows via a desktop companion
application. AI processing will run on the host computer, while CTRL acts as a
low-latency physical interface for context-aware shortcuts and feedback.

-------------------------------------------------------------------------------------------------
## BOM
The complete bill of materials (BOM), including purchase links, is available in  
`/hardware/bom.csv`.

Manufacturing & sourcing:
- PCB fabrication: **JLCPCB**
- Components (India): **Robu.in**
- Enclosure: Online 3D printing services
  
-------------------------------------------------------------------------------------------------
## License
This project is open-source hardware and software and is released under the **MIT License**.

