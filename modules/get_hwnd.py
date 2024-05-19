import win32gui


def get_hwnd_by_window_name(window_name):
    return win32gui.FindWindow(None, window_name)
