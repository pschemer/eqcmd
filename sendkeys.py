import ctypes, time
import pyautogui
import pygetwindow as gw

SendInput = ctypes.windll.user32.SendInput

# DirectInput Key Code Table
Keycode = {
    "esc":0x01,
    "1":0x02,
    "2":0x03,
    "3":0x04,
    "4":0x05,
    "5":0x06,
    "6":0x07,
    "7":0x08,
    "8":0x09,
    "9":0x0A,
    "0":0x0B,
    "-":0x0C,
    "=":0x0D,
    "backspace":0x0E,
    "tab":0x0F,
    "q":0x10,
    "w":0x11,
    "e":0x12,
    "r":0x13,
    "t":0x14,
    "y":0x15,
    "u":0x16,
    "i":0x17,
    "o":0x18,
    "p":0x19,
    "[":0x1A,
    "]":0x1B,
    "enter":0x1C,
    # Ctrl
    "^":0x1D,
    "a":0x1E,
    "s":0x1F,
    "d":0x20,
    "f":0x21,
    "g":0x22,
    "h":0x23,
    "j":0x24,
    "k":0x25,
    "l":0x26,
    ";":0x27,
    "'":0x28,
    "`":0x29,
    # Shift
    "#":0x2A,
    #"\":0x2B,
    "z":0x2C,
    "x":0x2D,
    "c":0x2E,
    "v":0x2F,
    "b":0x30,
    "n":0x31,
    "m":0x32,
    ",":0x33,
    ".":0x34,
    "/":0x35,
    # Alt
    "!":0x38,
    " ":0x39,
    "f1":0x3B,
    "f2":0x3C,
    "f3":0x3D,
    "f4":0x3E,
    "f5":0x3F,
    "f6":0x40,
    "f7":0x41,
    "f8":0x42,
    "f9":0x43,
    "f10":0x44,
    "f11":0x57,
    "f12":0x58,
    # Numpad keys
    "*":0x37,
    "num7":0x47,
    "num8":0x48,
    "num9":0x49,
    "num-":0x4A,
    "num4":0x4B,
    "num5":0x4C,
    "num6":0x4D,
    "num+":0x4E,
    "num1":0x4F,
    "num2":0x50,
    "num3":0x51,
    # end numpad
}

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def KeyPress(window_title, keystrokes):

    if keystrokes not in Keycode:
        print(f"keystroke '{keystrokes}' not found")
        return
    
    print(f"Sending keystrokes '{keystrokes}' to window '{window_title}'")

    # Implement the logic to send keystrokes to the specified window
    try:
        # Get the window handle based on the window title
        window = gw.getWindowsWithTitle(window_title)[0]

        # Activate the window
        window.activate()
        
        time.sleep(.02)
        PressKey(Keycode[keystrokes])
        time.sleep(.02)
        ReleaseKey(Keycode[keystrokes])

    except Exception as e:
        print(f"Error sending keystrokes to window '{window_title}': {e}")