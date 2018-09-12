import time, ctypes
from win32api import GetKeyState
from win32con import VK_NUMLOCK
# IMPORTANT!!! Arrow keys are default bound to numpad 4,6,2,8. Disable numlock befure use!!!!!

# http://www.flint.jp/misc/?q=dik&lang=en DirectInput Key Codes
DIK_A = 0x1E
DIK_Q = 0x10


DIK_LEFT = 0xCB
DIK_RIGHT = 0xCD
DIK_UP = 0xC8
DIK_DOWN = 0xD0
DIK_ALT = 0xB8

DIK_NUMLOCK = 0x45


SendInput = ctypes.windll.user32.SendInput
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

# Actual Functions


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))  # 0x0008: KEYEVENTF_SCANCODE
    x = Input( ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))  # 0x0002: KEYEVENTF_KEYUP


def singlepress(hexcode, delay = 0.05):
    PressKey(hexcode)
    time.sleep(delay)
    ReleaseKey(hexcode)


def get_numlock_status():
    return GetKeyState(VK_NUMLOCK)

