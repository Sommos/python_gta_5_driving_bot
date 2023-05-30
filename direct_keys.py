import ctypes
import time

# allows the program to send input using Windows API
send_input = ctypes.windll.user32.SendInput

# scan codes for W, A, S, D
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

# C structure definitions 
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [
                # wVk represents a virtual-key code
                ("wVk", ctypes.c_ushort),
                # wScan represents a hardware scan code
                ("wScan", ctypes.c_ushort),
                # dwFlags specifies various aspects of function operation
                ("dwFlags", ctypes.c_ulong),
                # time specifies the time stamp for the event, in milliseconds
                ("time", ctypes.c_ulong),
                # dwExtraInfo specifies extra information associated with the message
                ("dwExtraInfo", PUL)
                ]

class HardwareInput(ctypes.Structure):
    _fields_ = [
                # uMsg specifies the message type
                ("uMsg", ctypes.c_ulong),
                # wParamL specifies the low-order word of the wParam argument
                ("wParamL", ctypes.c_short),
                # wParamH specifies the high-order word of the wParam argument
                ("wParamH", ctypes.c_ushort)
                ]

class MouseInput(ctypes.Structure):
    _fields_ = [
                # dx specifies the mouse's absolute position along the x-axis or its amount of motion since the last mouse event was generated
                ("dx", ctypes.c_long),
                # dy specifies the mouse's absolute position along the y-axis or its amount of motion since the last mouse event was generated
                ("dy", ctypes.c_long),
                # mouseData specifies the mouse wheel's distance rotated, expressed in multiples or divisions of WHEEL_DELTA
                ("mouseData", ctypes.c_ulong),
                # dwFlags specifies various aspects of mouse motion and button clicks
                ("dwFlags", ctypes.c_ulong),
                # time specifies the time stamp for the event, in milliseconds
                ("time",ctypes.c_ulong),
                # dwExtraInfo specifies extra information associated with the message
                ("dwExtraInfo", PUL)
                ]

class Input_I(ctypes.Union):
    # the union of the three structures  
    _fields_ = [
                ("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)
                ]

class Input(ctypes.Structure):
    _fields_ = [
                # type specifies the type of the input event
                ("type", ctypes.c_ulong),
                # the union of the three structures
                ("ii", Input_I)
                ]

# function to press key, hexKeyCode is the scan code of the key
def press_key(hexKeyCode):
    # extra is a variable of type unsigned long equal to 0
    extra = ctypes.c_ulong(0)
    # ii_ is an instance of Input_I
    ii_ = Input_I()
    # ki is an instance of KeyBdInput, '0x0008' is the value of KEYEVENTF_EXTENDEDKEY to show an extended key event (it's been pressed down)
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    # x is an instance of Input, '1' is the value of INPUT_KEYBOARD to show a keyboard event
    x = Input( ctypes.c_ulong(1), ii_)
    # send the input
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# function to release key
def release_key(hexKeyCode):
    # extra is a variable of type unsigned long equal to 0
    extra = ctypes.c_ulong(0)
    # ii_ is an instance of Input_I
    ii_ = Input_I()
    # ki is an instance of KeyBdInput, '0x0008 | 0x0002' is the value of KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP to show an extended key event (it's been released)
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    # x is an instance of Input, '1' is the value of INPUT_KEYBOARD to show a keyboard event
    x = Input( ctypes.c_ulong(1), ii_)
    # send the input
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

if __name__ == '__main__':
    while(True):
        press_key(0x11)
        time.sleep(1)
        release_key(0x11)
        time.sleep(1)