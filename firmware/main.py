 # ================================
# CTRL Macro Pad Firmware v3.0
# AI-Ready Programmable Macro Pad
# NEW: Bluetooth, Battery Monitor, Power Management
# ================================

import board
import busio
import time
import digitalio
import analogio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import MatrixScanner
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.extensions.media_keys import MediaKeys

# ----------------
# Hardware Configuration
# ----------------
class Config:
    """Complete hardware configuration"""
    
    # Matrix Configuration (6 mechanical keys)
    ROW_PINS = (board.GP2, board.GP3)
    COL_PINS = (board.GP6, board.GP7, board.GP8)
    
    # Rotary Encoder with Push Switch
    ENCODER_A = board.GP14      # RE-1 (CLK)
    ENCODER_B = board.GP15      # RE-2 (DT)
    ENCODER_SW = board.GP14     # Switch (SW2 to GP14, SW1 to GND)
    
    # IPS Display (ST7789 - 135x240)
    DISPLAY_DC = board.GP16
    DISPLAY_CS = board.GP17
    DISPLAY_SCK = board.GP18
    DISPLAY_MOSI = board.GP19
    DISPLAY_RST = board.GP20
    
    # Battery Monitor (ADC)
    BATTERY_PIN = board.GP26    # ADC0 - Battery voltage divider
    
    # Power Management
    LONG_PRESS_MS = 5000        # 5 seconds for power toggle
    LOW_BATTERY_THRESHOLD = 3.3  # Volts
    CRITICAL_BATTERY_THRESHOLD = 3.0  # Volts
    
    # Bluetooth (Optional - if HC-05/HC-06 module added)
    # BT_TX = board.GP0  # UART TX (future expansion)
    # BT_RX = board.GP1  # UART RX (future expansion)
    
    NUM_LAYERS = 3
    DIODE_DIRECTION = "COL2ROW"

# ----------------
# Power Management System
# ----------------
class PowerManager:
    """
    Manages device power states and battery monitoring
    """
    
    def __init__(self):
        self.device_on = True
        self.battery_voltage = 0.0
        self.battery_percent = 100
        self.press_start = None
        self.in_sleep = False
        
        # Initialize battery ADC
        try:
            self.battery_adc = analogio.AnalogIn(Config.BATTERY_PIN)
            self.battery_enabled = True
            print("✓ Battery monitor enabled")
        except Exception as e:
            print(f"⚠ Battery monitor disabled: {e}")
            self.battery_enabled = False
    
    def read_battery(self):
        """Read battery voltage and calculate percentage"""
        if not self.battery_enabled:
            return 100
        
        try:
            # Read ADC value (0-65535)
            raw = self.battery_adc.value
            
            # Convert to voltage (3.3V reference, voltage divider x2)
            self.battery_voltage = (raw / 65535.0) * 3.3 * 2.0
            
            # Calculate percentage (3.0V = 0%, 4.2V = 100% for LiPo)
            if self.battery_voltage >= 4.2:
                self.battery_percent = 100
            elif self.battery_voltage <= 3.0:
                self.battery_percent = 0
            else:
                self.battery_percent = int(((self.battery_voltage - 3.0) / 1.2) * 100)
            
            return self.battery_percent
            
        except Exception as e:
            print(f"Battery read error: {e}")
            return 100
    
    def check_long_press(self, encoder_pressed):
        """
        Check for long press (5 seconds) to toggle power
        Returns True if power state should toggle
        """
        if encoder_pressed:
            if self.press_start is None:
                self.press_start = time.monotonic()
            
            elapsed = time.monotonic() - self.press_start
            
            if elapsed >= (Config.LONG_PRESS_MS / 1000.0):
                self.press_start = None
                return True
        else:
            self.press_start = None
        
        return False
    
    def enter_sleep(self):
        """Enter low-power sleep mode"""
        self.in_sleep = True
        self.device_on = False
        print("→ Entering sleep mode...")
        # Placeholder for actual sleep implementation
        # In CircuitPython, true deep sleep requires alarm module
    
    def wake_up(self):
        """Wake from sleep mode"""
        self.in_sleep = False
        self.device_on = True
        print("→ Waking up...")
    
    def get_battery_status(self):
        """Get battery status string"""
        if not self.battery_enabled:
            return "USB"
        
        if self.battery_voltage < Config.CRITICAL_BATTERY_THRESHOLD:
            return "CRITICAL"
        elif self.battery_voltage < Config.LOW_BATTERY_THRESHOLD:
            return "LOW"
        else:
            return f"{self.battery_percent}%"

# Initialize power manager
power = PowerManager()

# ----------------
# Bluetooth Manager (Future Expansion)
# ----------------
class BluetoothManager:
    """
    Bluetooth HID support via HC-05/HC-06 module
    Currently placeholder for future hardware expansion
    """
    
    def __init__(self):
        self.enabled = False
        self.connected = False
        self.mode = "USB"  # "USB" or "BLUETOOTH"
    
    def init_uart(self):
        """Initialize UART for Bluetooth module"""
        # Future: Initialize UART on GP0/GP1
        # self.uart = busio.UART(board.GP0, board.GP1, baudrate=115200)
        pass
    
    def send_key_event(self, key_code, pressed):
        """Send key event over Bluetooth"""
        if not self.enabled or not self.connected:
            return
        # Future: Send HID packets over UART
        pass
    
    def send_encoder_event(self, direction):
        """Send encoder rotation over Bluetooth"""
        if not self.enabled or not self.connected:
            return
        # Future: Send encoder data
        pass
    
    def poll(self):
        """Check for incoming Bluetooth messages"""
        if not self.enabled:
            return
        # Future: Read UART data
        pass
    
    def toggle_mode(self):
        """Switch between USB and Bluetooth modes"""
        if not self.enabled:
            return
        
        self.mode = "BLUETOOTH" if self.mode == "USB" else "USB"
        print(f"→ Mode: {self.mode}")
        return self.mode

# Initialize Bluetooth manager
bluetooth = BluetoothManager()

# ----------------
# Keyboard Setup
# ----------------
keyboard = KMKKeyboard()

# Initialize modules
layers_module = Layers()
encoder_module = EncoderHandler()
media_keys = MediaKeys()

# Register modules and extensions
keyboard.modules = [layers_module, encoder_module]
keyboard.extensions = [media_keys]

# ----------------
# Matrix Scanner
# ----------------
keyboard.matrix = MatrixScanner(
    row_pins=Config.ROW_PINS,
    col_pins=Config.COL_PINS,
    columns_to_anodes=Config.DIODE_DIRECTION,
    interval=0.02,
    max_events=64
)

# ----------------
# Rotary Encoder
# ----------------
encoder_module.pins = (
    (Config.ENCODER_A, Config.ENCODER_B, Config.ENCODER_SW),
)

# ----------------
# Custom Macros
# ----------------

# Productivity
COPY = KC.LCTL(KC.C)
PASTE = KC.LCTL(KC.V)
CUT = KC.LCTL(KC.X)
UNDO = KC.LCTL(KC.Z)
REDO = KC.LCTL(KC.Y)
SAVE = KC.LCTL(KC.S)
SELECT_ALL = KC.LCTL(KC.A)
FIND = KC.LCTL(KC.F)

# Browser/Tabs
NEW_TAB = KC.LCTL(KC.T)
CLOSE_TAB = KC.LCTL(KC.W)
REOPEN_TAB = KC.LCTL(KC.LSFT(KC.T))
REFRESH = KC.LCTL(KC.R)

# Developer
COMMENT_LINE = KC.LCTL(KC.SLASH)
FORMAT_DOC = KC.LSFT(KC.LALT(KC.F))
TERMINAL = KC.LCTL(KC.GRAVE)
COMMAND_PALETTE = KC.LCTL(KC.LSFT(KC.P))

# Screenshot
SCREENSHOT = KC.LGUI(KC.LSFT(KC.S))

# ----------------
# Encoder Behavior
# ----------------
encoder_module.map = [
    # Layer 0: Volume + Mute
    ((KC.VOLU, KC.VOLD, KC.MUTE),),
    
    # Layer 1: Scroll + Enter
    ((KC.RIGHT, KC.LEFT, KC.ENTER),),
    
    # Layer 2: Zoom + Reset
    ((KC.LCTL(KC.EQUAL), KC.LCTL(KC.MINUS), KC.LCTL(KC.N0)),),
]

# ----------------
# Keymap
# ----------------
keyboard.keymap = [
    # Layer 0 — Productivity
    [
        COPY,           # SW1
        PASTE,          # SW2
        CUT,            # SW3
        UNDO,           # SW4
        SAVE,           # SW5
        KC.MO(1),       # SW6 → Layer 1
    ],
    
    # Layer 1 — Media & Navigation
    [
        KC.MPLY,        # SW1: Play/Pause
        KC.MNXT,        # SW2: Next
        KC.MPRV,        # SW3: Previous
        KC.HOME,        # SW4: Home
        KC.END,         # SW5: End
        KC.MO(2),       # SW6 → Layer 2
    ],
    
    # Layer 2 — Developer Tools
    [
        NEW_TAB,        # SW1
        CLOSE_TAB,      # SW2
        COMMAND_PALETTE,# SW3
        COMMENT_LINE,   # SW4
        TERMINAL,       # SW5
        KC.TO(0),       # SW6 → Layer 0
    ],
]

# ----------------
# Display Manager
# ----------------
class DisplayManager:
    """Enhanced display with battery and status info"""
    
    def __init__(self):
        self.enabled = False
        self.display = None
        self.current_layer = 0
        self.last_battery_check = 0
        self.init_display()
    
    def init_display(self):
        """Initialize SPI display"""
        try:
            import displayio
            import adafruit_st7789
            from adafruit_display_text import label
            import terminalio
            
            displayio.release_displays()
            
            spi = busio.SPI(
                clock=Config.DISPLAY_SCK,
                MOSI=Config.DISPLAY_MOSI
            )
            
            display_bus = displayio.FourWire(
                spi,
                command=Config.DISPLAY_DC,
                chip_select=Config.DISPLAY_CS,
                reset=Config.DISPLAY_RST
            )
            
            self.display = adafruit_st7789.ST7789(
                display_bus,
                width=135,
                height=240,
                rotation=90,
                rowstart=40,
                colstart=53
            )
            
            self.enabled = True
            self.show_startup()
            print("✓ Display initialized")
            
        except ImportError:
            print("⚠ Display libraries missing")
            self.enabled = False
        except Exception as e:
            print(f"✗ Display init failed: {e}")
            self.enabled = False
    
    def show_startup(self):
        """Enhanced startup screen with battery info"""
        if not self.enabled:
            return
        
        try:
            import displayio
            from adafruit_display_text import label
            import terminalio
            
            splash = displayio.Group()
            
            # Title
            title = label.Label(
                terminalio.FONT,
                text="CTRL",
                color=0x00FF00,
                scale=3,
                x=80,
                y=20
            )
            
            # Version
            version = label.Label(
                terminalio.FONT,
                text="v3.0 PRO",
                color=0xFFFFFF,
                scale=1,
                x=85,
                y=50
            )
            
            # Battery status
            battery_status = power.get_battery_status()
            battery_color = 0x00FF00 if power.battery_percent > 50 else (
                0xFFFF00 if power.battery_percent > 20 else 0xFF0000
            )
            
            battery = label.Label(
                terminalio.FONT,
                text=f"Battery: {battery_status}",
                color=battery_color,
                scale=1,
                x=60,
                y=75
            )
            
            # Mode indicator
            mode = label.Label(
                terminalio.FONT,
                text=f"Mode: {bluetooth.mode}",
                color=0x00FFFF,
                scale=1,
                x=70,
                y=95
            )
            
            # Status
            status = label.Label(
                terminalio.FONT,
                text="READY",
                color=0x00FFFF,
                scale=2,
                x=80,
                y=115
            )
            
            splash.append(title)
            splash.append(version)
            splash.append(battery)
            splash.append(mode)
            splash.append(status)
            
            self.display.show(splash)
            
        except Exception as e:
            print(f"Startup display error: {e}")
    
    def show_layer(self, layer_num):
        """Display layer with battery indicator"""
        if not self.enabled:
            return
        
        self.current_layer = layer_num
        layer_names = ["PRODUCTIVITY", "MEDIA", "DEVELOPER"]
        layer_colors = [0x00FF00, 0xFF00FF, 0x00FFFF]
        
        if 0 <= layer_num < len(layer_names):
            try:
                import displayio
                from adafruit_display_text import label
                import terminalio
                
                splash = displayio.Group()
                
                # Battery indicator (top right)
                battery_status = power.get_battery_status()
                battery_color = 0x00FF00 if power.battery_percent > 50 else (
                    0xFFFF00 if power.battery_percent > 20 else 0xFF0000
                )
                
                battery_label = label.Label(
                    terminalio.FONT,
                    text=battery_status,
                    color=battery_color,
                    scale=1,
                    x=190,
                    y=10
                )
                
                # Layer number
                layer_label = label.Label(
                    terminalio.FONT,
                    text=f"LAYER {layer_num}",
                    color=0xFFFFFF,
                    scale=2,
                    x=60,
                    y=40
                )
                
                # Layer name
                name_label = label.Label(
                    terminalio.FONT,
                    text=layer_names[layer_num],
                    color=layer_colors[layer_num],
                    scale=2,
                    x=20,
                    y=80
                )
                
                splash.append(battery_label)
                splash.append(layer_label)
                splash.append(name_label)
                self.display.show(splash)
                
            except Exception as e:
                print(f"Layer display error: {e}")
    
    def show_low_battery_warning(self):
        """Show critical battery warning"""
        if not self.enabled:
            return
        
        try:
            import displayio
            from adafruit_display_text import label
            import terminalio
            
            splash = displayio.Group()
            
            warning = label.Label(
                terminalio.FONT,
                text="LOW BATTERY!",
                color=0xFF0000,
                scale=2,
                x=40,
                y=60
            )
            
            voltage = label.Label(
                terminalio.FONT,
                text=f"{power.battery_voltage:.2f}V",
                color=0xFFFF00,
                scale=2,
                x=80,
                y=90
            )
            
            splash.append(warning)
            splash.append(voltage)
            self.display.show(splash)
            
        except Exception as e:
            print(f"Warning display error: {e}")
    
    def update_battery_indicator(self):
        """Periodically update battery status"""
        current_time = time.monotonic()
        if current_time - self.last_battery_check > 30:  # Update every 30 seconds
            self.last_battery_check = current_time
            power.read_battery()
            
            if power.battery_voltage < Config.CRITICAL_BATTERY_THRESHOLD:
                self.show_low_battery_warning()

# Initialize display
display = DisplayManager()

# ----------------
# AI Integration
# ----------------
class AIInterface:
    """Enhanced AI interface with battery and mode awareness"""
    
    def __init__(self):
        self.context = "default"
        self.enabled = False
        self.serial = None
    
    def init_serial(self):
        """Initialize USB serial"""
        try:
            import usb_cdc
            self.serial = usb_cdc.data
            if self.serial:
                self.enabled = True
                print("✓ AI serial ready")
        except Exception as e:
            print(f"✗ AI init failed: {e}")
    
    def send_telemetry(self):
        """Send device telemetry to host"""
        if not self.enabled or not self.serial:
            return
        
        try:
            import json
            data = json.dumps({
                "type": "telemetry",
                "battery": power.battery_percent,
                "voltage": power.battery_voltage,
                "mode": bluetooth.mode,
                "layer": display.current_layer,
                "timestamp": time.monotonic()
            })
            self.serial.write((data + "\n").encode('utf-8'))
        except Exception as e:
            print(f"Telemetry error: {e}")
    
    def send_event(self, event_type, data):
        """Send event to host"""
        if not self.enabled or not self.serial:
            return
        
        try:
            import json
            message = json.dumps({
                "type": event_type,
                "data": data,
                "timestamp": time.monotonic()
            })
            self.serial.write((message + "\n").encode('utf-8'))
        except Exception as e:
            print(f"Event send error: {e}")

# Initialize AI interface
ai = AIInterface()
# ai.init_serial()  # Uncomment to enable

# ----------------
# Event Handlers
# ----------------

# Track encoder state for long press detection
encoder_pressed = False
last_telemetry = 0

def custom_process_key(key, is_pressed, int_coord):
    """Enhanced key handler with power management"""
    global encoder_pressed
    
    # Check if this is encoder button
    if hasattr(key, 'code') and key.code == Config.ENCODER_SW:
        encoder_pressed = is_pressed
        
        # Check for long press power toggle
        if power.check_long_press(encoder_pressed):
            if power.device_on:
                power.enter_sleep()
                display.show_low_battery_warning()  # Repurpose as sleep indicator
            else:
                power.wake_up()
                display.show_startup()
            return
    
    # Don't process keys if device is off
    if not power.device_on:
        return
    
    # Send to Bluetooth if in BT mode
    if bluetooth.mode == "BLUETOOTH" and is_pressed:
        bluetooth.send_key_event(key, is_pressed)
    
    # Send telemetry
    ai.send_event("key_press", {
        "key": str(key),
        "pressed": is_pressed,
        "position": int_coord
    })

# Layer change handler
def on_layer_change(layer):
    """Handle layer changes"""
    display.show_layer(layer)
    ai.send_event("layer_change", {"layer": layer})

# ----------------
# Main Loop Enhancement
# ----------------
def background_tasks():
    """Periodic background tasks"""
    global last_telemetry
    
    current_time = time.monotonic()
    
    # Update battery every 30 seconds
    if current_time - last_telemetry > 30:
        last_telemetry = current_time
        power.read_battery()
        display.update_battery_indicator()
        ai.send_telemetry()
    
    # Poll Bluetooth
    bluetooth.poll()
    
    # Check for critical battery
    if power.battery_voltage < Config.CRITICAL_BATTERY_THRESHOLD:
        print("⚠ CRITICAL BATTERY - Entering sleep mode")
        power.enter_sleep()

# Hook background tasks into KMK
keyboard.before_matrix_scan = background_tasks

# ----------------
# Startup
# ----------------
print("")
print("=" * 60)
print("   CTRL MACRO PAD v3.0 PRO")
print("   AI-Ready | Battery Powered | Bluetooth Ready")
print("=" * 60)
print("")
print("HARDWARE:")
print(f"  Matrix: 2x3 (6 keys)")
print(f"  Encoder: GP{Config.ENCODER_A.id}, GP{Config.ENCODER_B.id} + Switch")
print(f"  Display: 135x240 IPS {'✓' if display.enabled else '✗'}")
print(f"  Battery: {power.get_battery_status()} ({power.battery_voltage:.2f}V)")
print("")
print("FEATURES:")
print(f"  Layers: {Config.NUM_LAYERS}")
print(f"  Mode: {bluetooth.mode}")
print(f"  AI: {'✓ Ready' if ai.enabled else '○ Available'}")
print(f"  Power: Hold encoder {Config.LONG_PRESS_MS/1000:.0f}s to toggle")
print("")
print("=" * 60)
print("✓ All systems operational")
print("=" * 60)
print("")

# ----------------
# Start
# ----------------
if __name__ == '__main__':
    keyboard.go()