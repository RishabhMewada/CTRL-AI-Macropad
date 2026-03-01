# CTRL-AI-Macropad
<img width="1419" height="571" alt="Screenshot 2025-12-28 222231" src="https://github.com/user-attachments/assets/f7881569-19a2-49f7-9838-46889130ec1f" />

## What is CTRL?
CTRL is a custom-built Human-Computer Interaction (HCI) Development Board designed for productivity tooling, embedded experimentation, wireless HID systems, and future AI-assisted workflows.

Originally developed as a programmable macropad, the project has evolved into a battery-powered, dual-transport embedded platform built around the Raspberry Pi Pico (RP2040), featuring modular firmware architecture and wireless expansion capabilities.CTRL is a custom-built Human-Computer Interaction (HCI) Development Board designed for productivity tooling, embedded experimentation, wireless HID systems, and future AI-assisted workflows.

Originally developed as a programmable macropad, the project has evolved into a battery-powered, dual-transport embedded platform built around the Raspberry Pi Pico (RP2040), featuring modular firmware architecture and wireless expansion capabilities.
<p align="center">
  <img src=https://github.com/user-attachments/assets/c879a765-367e-4b05-86a0-af208b819c26>

-------------------------------------------------------------------------------------------------
## Purpose 
The goal of this project was to design a fully custom embedded input system from scratch — including:

- PCB design
- Multi-MCU system architecture
- Power management circuitry
- Firmware modularization
- Custom enclosure
- This project focuses on understanding:
- Embedded system design
- Hardware-software co-design
- Power-aware firmware
- Multi-transport communication (USB + BLE)
- Expandable interaction hardware

The system is built with future extensibility in mind rather than being limited to fixed macro execution.

 <p align="center">
  <img src="https://github.com/user-attachments/assets/4551a615-e77e-4ec2-b289-c4d70b81c0fa">
</p>

-------------------------------------------------------------------------------------------------
## Features

*Core Hardware*

- 6 Mechanical Keys (Cherry MX compatible)
- Rotary Encoder with integrated push switch
- 1.14″ IPS SPI Display (ST7789)
- Raspberry Pi Pico (RP2040)
- BLE Co-Processor (UART interface)
- Li-ion battery support
- On-board charging IC
- Software-controlled power system
- Fully custom 2-layer PCB
- Expansion GPIO header
- SWD debug header
-------------------------------------------------------------------------------------------------
## Transport & Connectivity

- USB HID (via Raspberry Pi Pico)
- Bluetooth HID (via BLE co-processor)
- UART-based inter-MCU communication
- I²C sensor bus (IMU connected with interrupt support)
-------------------------------------------------------------------------------------------------
## Hardware
The PCB is designed using KiCad (open-source) and Fusion 360.

Specifications

- 2-layer PCB
- Diode-protected key matrix
- SPI-connected IPS display
- I²C IMU (interrupt-driven)
- UART-connected BLE module
- Li-ion battery charging circuit (MCP73831)
- 3.3V LDO regulator (AP2112K)
- Single USB-C interface (handled by Pico only)

All PCB source files are available in `/hardware/kicad`.

<p align="center">
  <img src="https://github.com/user-attachments/assets/b63ff671-658b-4ba5-a15d-6402b3deaaeb">
</p>

-------------------------------------------------------------------------------------------------

## Firmware
The firmware architecture has evolved from a monolithic USB HID mapping into a modular embedded system design.

**Architecture Overview**

*Subsystems include:*

- Input Processing Layer
- Power Management Layer
- Transport Abstraction Layer
- Communication Layer (UART BLE)
- Mode Manager

*Supported Features*

- Key matrix scanning
- Rotary encoder quadrature decoding
- USB HID output
- Bluetooth HID output
- 5-second long-press soft power
- Battery voltage monitoring
- Event-driven input routing

*Planned Enhancements*

- Dynamic key remapping
- On-device UI configuration
- BLE protocol expansion
- IMU gesture-based input
- Power optimization (sleep states)
- Desktop companion software

Firmware files are located in `/firmware`.

-------------------------------------------------------------------------------------------------
## Case
The enclosure is designed in Fusion 360 (personal use).
[STEP and source files are included in `/case`.]

**Dimensions:**
- Length: 11.8 cm
- Height: 6.3 cm
- Thickness: 1.5 cm

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
CTRL is designed to support AI-assisted workflows through a host-based companion application.
AI processing will run on the host computer, while CTRL serves as:

~ A low-latency physical interface
~ A status display device
~ A context-aware shortcut controller

The hardware architecture is transport-agnostic, enabling flexible integration with higher-level software systems.

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

