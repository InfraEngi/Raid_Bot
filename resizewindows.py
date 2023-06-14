# Import the necessary modules
import win32gui
from win32con import SWP_NOSIZE, SW_SHOW, SWP_SHOWWINDOW

class WindowResizer:
    def __init__(self, width, height, title_prefix):
        # Store the width, height, and title prefix as instance attributes
        self.width = width
        self.height = height
        self.title_prefix = title_prefix

    def resize_windows(self):
        # Create a function that will be called for each window
        def callback(hwnd, extra):
            # Get the window title and dimensions
            title = win32gui.GetWindowText(hwnd)
            x, y, right, bottom = win32gui.GetWindowRect(hwnd)

            # Check if the window is valid and has a title that starts with the prefix, and has valid dimensions
            if win32gui.IsWindow(hwnd) and title.startswith(self.title_prefix) and (x, y, right, bottom) != (0, 0, 0, 0):
                # Check if the window has valid dimensions
                if x >= 0 and y >= 0 and right > 0 and bottom > 0:
                    # Check if the window is visible and not already the correct size
                    if win32gui.IsWindowVisible(hwnd) and (right-x, bottom-y) != (self.width, self.height):
                        # Check if the window is still valid before calling SetWindowPos
                        if win32gui.IsWindow(hwnd):
                            # Resize the window
                            win32gui.MoveWindow(hwnd, x, y, self.width, self.height, True)

                            # Show the window, if it's not already visible
                            if not win32gui.IsWindowVisible(hwnd):
                                win32gui.ShowWindow(hwnd, SW_SHOW)
                            win32gui.SetWindowPos(hwnd, SWP_SHOWWINDOW, 0, 0, 0, 0, SWP_NOSIZE)
        # Enumerate all windows on the desktop
        win32gui.EnumWindows(callback, None)

# Create an instance of the WindowResizer class
resizer = WindowResizer(1900, 1060,"EVE - ")

# Resize the windows
resizer.resize_windows()