import pyautogui

def get_square_coordinates(square, top_left, bottom_right):
    # Calculate the dimensions of each square based on the bounding box
    board_width = bottom_right[0] - top_left[0]
    board_height = bottom_right[1] - top_left[1]
    square_width = board_width / 8
    square_height = board_height / 8
    
    # Convert file (letter) to 0-7 index
    file = ord(square[0]) - ord('a')
    # Convert rank (number) to 0-7 index, with rank 1 at the bottom
    rank = 8 - int(square[1])
    
    # Calculate pixel coordinates of the center of the square
    x = int(top_left[0] + file * square_width + square_width / 2)
    y = int(top_left[1] + rank * square_height + square_height / 2)
    return (x, y)

def click_and_drag_move(best_move, top_left, bottom_right):
    # Parse the best move into start and end squares
    start_square, end_square = best_move[:2], best_move[2:]
    
    # Get the pixel coordinates of the start and end squares
    start_coords = get_square_coordinates(start_square, top_left, bottom_right)
    end_coords = get_square_coordinates(end_square, top_left, bottom_right)
    
    # Perform the click-and-drag action
    pyautogui.moveTo(start_coords)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_coords)
    pyautogui.mouseUp()
