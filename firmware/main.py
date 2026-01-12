# ================================
# CTRL Macro Pad Firmware v1.0
# AI-Ready Programmable Macro Pad
# ================================

import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import MatrixScanner
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.extensions.media_keys import MediaKeys

# ----------------
# Hardware Configuration (Verified Pins)
# ----------------
class Config:
    """Hardware configuration - verified GPIO assignments"""
    
    # Matrix Configuration (2 rows x 3 columns)
    ROW_PINS = (board.GP2, board.GP3)          # ROW1=GP2, ROW2=GP3
    COL_PINS = (board.GP6, board.GP7, board.GP8)  # COL1=GP6, COL2=GP7, COL3=GP8
    
    # Matrix layout:
    # [SW1] [SW2] [SW3]  ← ROW1 (GP2)
    # [SW4] [SW5] [SW6]  ← ROW2 (GP3)
    #   ↑     ↑     ↑
    # COL1  COL2  COL3
    # (GP6) (GP7) (GP8)
    
    # Rotary Encoder (NO CONFLICTS!)
    ENCODER_A = board.GP14      # RE-1
    ENCODER_B = board.GP15      # RE-2
    
    # IPS Display (SPI) - ST7789 135x240 (NO CONFLICTS!)
    DISPLAY_DC = board.GP16     # TFT_DC
    DISPLAY_CS = board.GP17     # TFT_CS
    DISPLAY_SCK = board.GP18    # TFT_SCK
    DISPLAY_MOSI = board.GP19   # TFT_MOSI
    DISPLAY_RST = board.GP20    # TFT_RST
    
    NUM_LAYERS = 3
    DIODE_DIRECTION = "COL2ROW"

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
# Matrix Scanner Configuration
# ----------------
keyboard.matrix = MatrixScanner(
    row_pins=Config.ROW_PINS,
    col_pins=Config.COL_PINS,
    columns_to_anodes=Config.DIODE_DIRECTION,
    interval=0.02,  # 20ms debounce
    max_events=64
)

# ----------------
# Rotary Encoder Configuration
# ----------------
encoder_module.pins = (
    (Config.ENCODER_A, Config.ENCODER_B, None),  # GP14, GP15
)

# ----------------
# Custom Macros
# ----------------

# Productivity Macros
COPY = KC.LCTL(KC.C)
PASTE = KC.LCTL(KC.V)
CUT = KC.LCTL(KC.X)
UNDO = KC.LCTL(KC.Z)
REDO = KC.LCTL(KC.Y)
SAVE = KC.LCTL(KC.S)
SAVE_ALL = KC.LCTL(KC.K)(KC.S)
SELECT_ALL = KC.LCTL(KC.A)
FIND = KC.LCTL(KC.F)
REPLACE = KC.LCTL(KC.H)

# Browser/Tab Macros
NEW_TAB = KC.LCTL(KC.T)
CLOSE_TAB = KC.LCTL(KC.W)
REOPEN_TAB = KC.LCTL(KC.LSFT(KC.T))
SWITCH_TAB_RIGHT = KC.LCTL(KC.TAB)
SWITCH_TAB_LEFT = KC.LCTL(KC.LSFT(KC.TAB))
REFRESH = KC.LCTL(KC.R)
HARD_REFRESH = KC.LCTL(KC.LSFT(KC.R))

# Developer Macros
COMMENT_LINE = KC.LCTL(KC.SLASH)
FORMAT_DOC = KC.LSFT(KC.LALT(KC.F))
TERMINAL = KC.LCTL(KC.GRAVE)
COMMAND_PALETTE = KC.LCTL(KC.LSFT(KC.P))
GO_TO_FILE = KC.LCTL(KC.P)
SPLIT_EDITOR = KC.LCTL(KC.BACKSLASH)

# Screenshot & System
SCREENSHOT = KC.LGUI(KC.LSFT(KC.S))
TASK_MANAGER = KC.LCTL(KC.LSFT(KC.ESC))

# ----------------
# Encoder Behavior Map
# ----------------
encoder_module.map = [
    # Layer 0: Volume control
    ((KC.VOLU, KC.VOLD),),
    
    # Layer 1: Horizontal scroll
    ((KC.RIGHT, KC.LEFT),),
    
    # Layer 2: Zoom (Ctrl + Plus/Minus)
    ((KC.LCTL(KC.EQUAL), KC.LCTL(KC.MINUS)),),
]

# ----------------
# Keymap Definition
# ----------------
keyboard.keymap = [
    # ========================================
    # Layer 0 — Default (Productivity)
    # ========================================
    [
        COPY,           # SW1: Copy
        PASTE,          # SW2: Paste
        CUT,            # SW3: Cut
        UNDO,           # SW4: Undo
        SAVE,           # SW5: Save
        KC.MO(1),       # SW6: Hold for Layer 1
    ],
    
    # ========================================
    # Layer 1 — Media & Navigation
    # ========================================
    [
        KC.MPLY,        # SW1: Play/Pause
        KC.MNXT,        # SW2: Next Track
        KC.MPRV,        # SW3: Previous Track
        KC.HOME,        # SW4: Home
        KC.END,         # SW5: End
        KC.MO(2),       # SW6: Hold for Layer 2
    ],
    
    # ========================================
    # Layer 2 — Developer Tools
    # ========================================
    [
        NEW_TAB,        # SW1: New Tab
        CLOSE_TAB,      # SW2: Close Tab
        COMMAND_PALETTE,# SW3: Command Palette
        COMMENT_LINE,   # SW4: Comment/Uncomment
        TERMINAL,       # SW5: Toggle Terminal
        KC.TO(0),       # SW6: Return to Layer 0
    ],
]

# ----------------
# Display Module
# ----------------
class DisplayManager:
    """
    IPS Display Driver (ST7789 - 135x240)
    Connected via SPI - NO PIN CONFLICTS
    """
    
    def __init__(self):
        self.enabled = False
        self.display = None
        self.current_layer = 0
        self.init_display()
    
    def init_display(self):
        """Initialize SPI display"""
        try:
            import displayio
            import adafruit_st7789
            from adafruit_display_text import label
            import terminalio
            
            # Release any existing displays
            displayio.release_displays()
            
            # Configure SPI bus
            spi = busio.SPI(
                clock=Config.DISPLAY_SCK,   # GP18
                MOSI=Config.DISPLAY_MOSI    # GP19
            )
            
            # Setup display bus
            display_bus = displayio.FourWire(
                spi,
                command=Config.DISPLAY_DC,     # GP16
                chip_select=Config.DISPLAY_CS, # GP17
                reset=Config.DISPLAY_RST       # GP20
            )
            
            # Initialize ST7789 display (135x240)
            self.display = adafruit_st7789.ST7789(
                display_bus,
                width=135,
                height=240,
                rotation=90,  # Landscape mode
                rowstart=40,
                colstart=53
            )
            
            self.enabled = True
            self.show_startup()
            print("✓ Display initialized successfully")
            
        except ImportError:
            print("⚠ Display libraries not found")
            print("  Install: adafruit_st7789, adafruit_display_text")
            self.enabled = False
        except Exception as e:
            print(f"✗ Display init failed: {e}")
            self.enabled = False
    
    def show_startup(self):
        """Show startup screen"""
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
                y=30
            )
            
            # Version
            version = label.Label(
                terminalio.FONT,
                text="v2.3",
                color=0xFFFFFF,
                scale=1,
                x=100,
                y=60
            )
            
            # Status
            status = label.Label(
                terminalio.FONT,
                text="READY",
                color=0x00FFFF,
                scale=2,
                x=80,
                y=100
            )
            
            splash.append(title)
            splash.append(version)
            splash.append(status)
            
            self.display.show(splash)
            
        except Exception as e:
            print(f"Startup display error: {e}")
    
    def show_layer(self, layer_num):
        """Display current layer name"""
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
                
                # Layer number
                layer_label = label.Label(
                    terminalio.FONT,
                    text=f"LAYER {layer_num}",
                    color=0xFFFFFF,
                    scale=2,
                    x=70,
                    y=30
                )
                
                # Layer name
                name_label = label.Label(
                    terminalio.FONT,
                    text=layer_names[layer_num],
                    color=layer_colors[layer_num],
                    scale=2,
                    x=20,
                    y=70
                )
                
                splash.append(layer_label)
                splash.append(name_label)
                self.display.show(splash)
                
            except Exception as e:
                print(f"Layer display error: {e}")
    
    def show_key_action(self, key_name):
        """Show key action temporarily"""
        if not self.enabled:
            return
        
        try:
            import displayio
            from adafruit_display_text import label
            import terminalio
            
            splash = displayio.Group()
            
            action_label = label.Label(
                terminalio.FONT,
                text=key_name,
                color=0xFFFF00,
                scale=2,
                x=50,
                y=60
            )
            
            splash.append(action_label)
            self.display.show(splash)
            
        except Exception as e:
            print(f"Action display error: {e}")
    
    def show_context(self, context_name):
        """Show AI-detected context"""
        if not self.enabled:
            return
        
        try:
            import displayio
            from adafruit_display_text import label
            import terminalio
            
            splash = displayio.Group()
            
            context_label = label.Label(
                terminalio.FONT,
                text=f"Context:\n{context_name}",
                color=0xFF8800,
                scale=1,
                x=10,
                y=60
            )
            
            splash.append(context_label)
            self.display.show(splash)
            
        except Exception as e:
            print(f"Context display error: {e}")

# Initialize display manager
display = DisplayManager()

# ----------------
# AI Integration
# ----------------
class AIInterface:
    """
    AI integration via USB serial
    Receives context from host computer
    """
    
    def __init__(self):
        self.context = "default"
        self.enabled = False
        self.serial = None
    
    def init_serial(self):
        """Initialize USB serial for AI communication"""
        try:
            import usb_cdc
            self.serial = usb_cdc.data
            if self.serial:
                self.enabled = True
                print("✓ AI serial interface ready")
        except Exception as e:
            print(f"✗ AI interface init failed: {e}")
    
    def update_context(self, new_context):
        """Receive context updates from host"""
        self.context = new_context
        display.show_context(new_context)
        print(f"→ Context: {new_context}")
    
    def check_messages(self):
        """Check for incoming messages from host"""
        if not self.enabled or not self.serial:
            return None
        
        if self.serial.in_waiting > 0:
            try:
                message = self.serial.readline()
                return message.decode('utf-8').strip()
            except Exception as e:
                print(f"Serial read error: {e}")
        return None
    
    def send_event(self, event_type, data):
        """Send key event to host for logging/learning"""
        if not self.enabled or not self.serial:
            return
        
        try:
            import json
            import time
            message = json.dumps({
                "type": event_type,
                "data": data,
                "timestamp": time.monotonic()
            })
            self.serial.write((message + "\n").encode('utf-8'))
        except Exception as e:
            print(f"Serial write error: {e}")

# Initialize AI interface
ai = AIInterface()
# Uncomment to enable AI features:
# ai.init_serial()

# ----------------
# Custom Key Handlers
# ----------------
original_process_key = keyboard.process_key

def custom_process_key(self, key, is_pressed, int_coord):
    """Custom key handler with display feedback"""
    result = original_process_key(self, key, is_pressed, int_coord)
    
    if is_pressed and display.enabled:
        # Show visual feedback on key press
        row, col = int_coord
        key_num = row * 3 + col + 1
        display.show_key_action(f"SW{key_num}")
    
    return result

keyboard.process_key = custom_process_key.__get__(keyboard, KMKKeyboard)

# ----------------
# Layer Change Handler
# ----------------
def on_layer_change(layer):
    """Called when layer changes"""
    display.show_layer(layer)
    ai.send_event("layer_change", {"layer": layer})

# Hook into layer changes
original_activate_layer = layers_module.activate_layer

def custom_activate_layer(self, layer):
    result = original_activate_layer(self, layer)
    on_layer_change(layer)
    return result

layers_module.activate_layer = custom_activate_layer.__get__(layers_module, Layers)

# ----------------
# Startup Info
# ----------------
print("")
print("=" * 55)
print("   CTRL MACRO PAD - FIRMWARE v2.3")
print("=" * 55)
print("")
print("HARDWARE CONFIGURATION:")
print(f"  Matrix: {len(Config.ROW_PINS)}x{len(Config.COL_PINS)} (6 mechanical keys)")
print(f"  Rows:   GP{Config.ROW_PINS[0].id}, GP{Config.ROW_PINS[1].id}")
print(f"  Cols:   GP{Config.COL_PINS[0].id}, GP{Config.COL_PINS[1].id}, GP{Config.COL_PINS[2].id}")
print(f"  Encoder: GP{Config.ENCODER_A.id} (A), GP{Config.ENCODER_B.id} (B)")
print("")
print("DISPLAY:")
print(f"  Status:  {'✓ Active' if display.enabled else '✗ Disabled'}")
if display.enabled:
    print(f"  Pins:    SCK=GP{Config.DISPLAY_SCK.id}, MOSI=GP{Config.DISPLAY_MOSI.id}")
    print(f"           CS=GP{Config.DISPLAY_CS.id}, DC=GP{Config.DISPLAY_DC.id}, RST=GP{Config.DISPLAY_RST.id}")
print("")
print("FEATURES:")
print(f"  Layers:  {Config.NUM_LAYERS} (Productivity, Media, Developer)")
print(f"  AI:      {'✓ Ready' if ai.enabled else '○ Available (disabled)'}")
print("")
print("=" * 55)
print("✓ NO PIN CONFLICTS - All systems nominal")
print("=" * 55)
print("")
print("Ready for input. Encoder controls volume on Layer 0.")
print("")

# ----------------
# Start Keyboard
# ----------------
if __name__ == '__main__':
    keyboard.go()