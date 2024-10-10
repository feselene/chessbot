import cv2
import numpy as np
import mss

# Chessboard size: 8x8 chessboard has 7x7 internal corners
CHESSBOARD_SIZE = (7, 7)

def find_chessboard_in_monitor(monitor, monitor_number):
    # Capture the screenshot from the monitor
    with mss.mss() as sct:
        screenshot = np.array(sct.grab(monitor))

    # Convert the screenshot to grayscale
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    found, corners = cv2.findChessboardCorners(gray, CHESSBOARD_SIZE, None)

    if found:
        # If found, retrieve the four corner coordinates
        top_left = tuple(corners[0][0])
        top_right = tuple(corners[6][0])
        bottom_left = tuple(corners[-7][0])
        bottom_right = tuple(corners[-1][0])

        # Output the coordinates of the four corners
        print(f"Monitor {monitor_number}: Chessboard found")
        print("Top Left Corner:", top_left)
        print("Top Right Corner:", top_right)
        print("Bottom Left Corner:", bottom_left)
        print("Bottom Right Corner:", bottom_right)

    else:
        # Output -1 for each corner if chessboard not found
        print(f"Monitor {monitor_number}: Chessboard not found")
        print("-1 -1 -1 -1")

# Check both monitors for the chessboard
with mss.mss() as sct:
    # Monitor indexing starts from 1 in mss, so we skip the first entry which is a dict of all monitors
    for monitor_number, monitor in enumerate(sct.monitors[1:], start=1):
        print(f"Checking Monitor {monitor_number}...")
        find_chessboard_in_monitor(monitor, monitor_number)
