import cv2
import pytesseract
import numpy as np
import pyautogui
import sys
import win32gui, win32ui, win32con
from PIL import ImageGrab
from resizewindows import WindowResizer

try:
    # Create an instance of the WindowResizer class
    resizer = WindowResizer(1600, 1200, "Raid:")
    # Resize the windows
    resizer.resize_windows()
except:
    print("Couldn't resize window")

# set the path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

windowtocapture = 'Raid: Shadow Legends'
window_handle = win32gui.FindWindow(None, windowtocapture)
if not window_handle:
    raise Exception('Window not found: {}'.format(windowtocapture))
window_region = win32gui.GetWindowRect(window_handle)

#while(True):

# these are to help calulations below of the specific points in the windows
top_right_corner = window_region[2], window_region[1]
top_left_corner = window_region[0], window_region[1]
bottom_left_corner = window_region[0], window_region[3]
bottom_right_corner = window_region[2], window_region[3]

# This is the region calulations for the Mission and Quests button
mission_quest_top_left = ((top_left_corner[0] + 240), (top_left_corner[1] + 1070)) 
mission_quest_bottom_right = ((bottom_right_corner[0] - 1075), (bottom_right_corner[1] - 8)) 
mission_quest_region = (mission_quest_top_left[0], mission_quest_top_left[1],  mission_quest_bottom_right[0],  mission_quest_bottom_right[1])

# This is the region calculations for the BATTLE icon on the start 
battle_top_left = ((top_left_corner[0] + 1275), (top_left_corner[1] + 1065))
battle_bottom_right = ((bottom_right_corner[0] - 10), (bottom_right_corner[1] - 8))
battle_button_region = (battle_top_left[0], battle_top_left[1],   battle_bottom_right[0],  battle_bottom_right[1])

# This is the region calculations for the energy counter
energy_top_left = ((top_left_corner[0] + 480), (top_left_corner[1] + 35))
energy_bottom_right = ((bottom_right_corner[0] - 1055), (bottom_right_corner[1] - 1080))
energy_counter_region = (energy_top_left[0], energy_top_left[1], energy_bottom_right[0], energy_bottom_right[1] )

# This is the region calculation for the arena coin counter
#arena_top_left = 
#arena_bottom_right

win32gui.SetForegroundWindow(window_handle)
screenshot = ImageGrab.grab(bbox=(energy_counter_region))
screenshot = np.array(screenshot)
screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    #cv2.imshow('Raid Vision', screenshot)
    #if cv2.waitKey(1) == ord('q'):
        #cv2.destroyAllWindows()
        #break 

def extract_number_from_screenshot(region):
    # Open the image using PIL
    screenshot = ImageGrab.grab(bbox=(region))

    # Convert the PIL image to a numpy array
    screenshot = np.array(screenshot)

    # Convert the image to grayscale
    gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

    # Apply thresholding to the image
    thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Use the Tesseract OCR engine to recognize the text in the image
    text = pytesseract.image_to_string(thresh)

    # Extract the number from the recognized text
    number = int(''.join(filter(str.isdigit, text)))

    # Print the number
    return number

def clickbattlebutton():
    battlebutton = pyautogui.locateOnScreen(r'Images\Battle_button.png', battle_button_region, confidence= 0.9)
    pyautogui.moveTo(battlebutton)
    pyautogui.leftClick()
    print("Clicking the BATTLE Button.")

def clickquestbutton():
    questbutton_noalert = pyautogui.locateOnScreen(r'Images\Quest_noalert.png', mission_quest_region, confidence= 0.9)
    if questbutton_noalert:
        pyautogui.moveTo(questbutton_noalert)
        pyautogui.leftClick()
        print("Clicking the Quest Button.")
    else:
        questbutton_alert = pyautogui.locateOnScreen(r'Images\Quest_alert.png', mission_quest_region, confidence= 0.9)
        if questbutton_alert:
            pyautogui.moveTo(questbutton_alert)
            pyautogui.leftClick()
            print("Clicking the Quest Button.")
        else:
            print("could not find the Quest button")
        
def energycheck():
    # Start the script by checking if the account has enough energy to do tasks
    energynumber = 0

    try:
        extract_number_from_screenshot(energy_counter_region)
        energynumber = extract_number_from_screenshot(energy_counter_region)
        if energynumber > 20:
            print(f"I have {energynumber} energy")
            return True
        else:
            print("Account donesn't have enough energy to continue playing")
            print("Shutting down script due to low energy")
            sys.exit()
    except:
        print("Can't find energy number")
        print(f"Closing the script ")
        sys.exit()

if energycheck() == True:
    clickquestbutton()

