# if oa.sys.os == 'win':
#     global wshell
#     import win32com.client
#     from win32com.client import Dispatch as CreateObject
#     wshell = CreateObject("WScript.Shell")

#     # Windows processing.
#     import win32gui
#     import re

#     class WindowMgr:
#         """ Encapsulates calls to the WinAPI for window management. """

#         def __init__ (self):
#             """ Constructor. """
#             self._handle = None

#         def find_window(self, class_name, window_name = None):
#             """ Find a window by its class_name. """
#             self._handle = win32gui.FindWindow(class_name, window_name)

#         def _window_enum_callback(self, hwnd, wildcard):
#             """ Pass to win32gui.EnumWindows() to check all opened windows. """
#             if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
#                 self._handle = hwnd

#         def find_window_wildcard(self, wildcard):
#             """ Find a window whose title matches a wildcard regex. """
#             self._handle = None
#             win32gui.EnumWindows(self._window_enum_callback, wildcard)

#         def set_foreground(self):
#             """ Put a window in the foreground. """
#             win32gui.SetForegroundWindow(self._handle)
