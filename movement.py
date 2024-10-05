import pyautogui
import time

# Pause between actions to avoid bot detection (if on a website) and make it human-like
pyautogui.PAUSE = 0.5  

def move_piece(start_x, start_y, end_x, end_y):
    # Move the mouse to the starting position (where the piece is located)
    pyautogui.moveTo(start_x, start_y, duration=0.2)

    # Simulate a mouse click and hold to "grab" the piece
    pyautogui.mouseDown()

    # Move the piece to the target position
    pyautogui.moveTo(end_x, end_y, duration=0.2)

    # Release the mouse button to "drop" the piece
    pyautogui.mouseUp()

# Example coordinates for starting and ending squares (replace these with actual values)
start_square = (500, 500)  # Example: Piece starting at (500, 500) on the board
end_square = (600, 600)    # Example: Move to (600, 600)

# Perform the drag and drop
move_piece(start_square[0], start_square[1], end_square[0], end_square[1])
