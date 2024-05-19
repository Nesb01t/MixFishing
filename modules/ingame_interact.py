import win32con
import win32gui

global VK_ZERO
VK_ZERO = 0x30
VK_SLASH = 0xDC


def pressKey(hwnd, key):
    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, key, 32772)
    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, key, 32772)
