import pyautogui
from pynput.mouse import Listener
import time

click_positions = []

def click_and_drag(x1, y1, x2, y2, duration=0.5):
    pyautogui.moveTo(x1, y1)
    pyautogui.mouseDown()
    pyautogui.moveTo(x2, y2, duration=duration)
    pyautogui.mouseUp()

# Stop listening after 4 clicks
def on_click (x, y, button, pressed): 
    if pressed: 
        click_positions.append((x, y))
        print(f"Clicked ({x}, {y})")
    
    if len(click_positions) == 4:
        print("Captured 4 clicks. Stopping listener.")
        return False

with Listener(on_click=on_click) as listener: 
    listener.join()

x1, y1 = 100, 100
x2, y2 = 200, 200
click_and_drag(x1, y1, x2, y2)
print("Click positions:", click_positions)
