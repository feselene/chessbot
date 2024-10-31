import pyautogui
import cv2
from pynput.mouse import Listener
import mss
import time
from inference_sdk import InferenceHTTPClient
from collections import defaultdict

CLIENT = InferenceHTTPClient(
    api_url="https://outline.roboflow.com",
    api_key="23rLdZSuKttIzDN4MKCd"
)

def capture_screenshot():
    with mss.mss() as sct: 
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)

        output_file = "screenshot.png"
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=output_file)
        print(f"Screenshot saved to {output_file}")

capture_screenshot()
result = CLIENT.infer("screenshot.png", model_id="chessboard-segmentation/1")

print(result)

image = cv2.imread("screenshot.png")
if (result['predictions']):
    x = int(result['predictions'][0]['x'])
    y = int(result['predictions'][0]['y'])

    width = int(result['predictions'][0]['width'])
    height = int(result['predictions'][0]['height'])
    
    print("width: ", width)
    print("height: ", height)
    
    # Calculate the top-left and bottom-right corners
    # top_left = (x - width // 2, y - height // 2)
    # bottom_right = (x + width // 2, y + height // 2)

    top_left = (x - width // 2, y - height // 2)
    bottom_right = (x + width // 2, y + height // 2)

    # Crop the image using the calculated coordinates
    cropped_image = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    # Save the cropped image
    cv2.imwrite("cropped_screenshot.png", cropped_image)

    print(result)
    CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="23rLdZSuKttIzDN4MKCd"
)

    result = CLIENT.infer("cropped_screenshot.png", model_id="2dcpd/2")
    print(result)
else:
    print("No prediction available. ")


def generate_fen_from_predictions(predictions):
    # Map classes to chess pieces in FEN notation
    piece_map = {
        'black-king': 'k',
        'black-queen': 'q',
        'black-rook': 'r',
        'black-bishop': 'b',
        'black-knight': 'n',
        'black-pawn': 'p',
        'white-king': 'K',
        'white-queen': 'Q',
        'white-rook': 'R',
        'white-bishop': 'B',
        'white-knight': 'N',
        'white-pawn': 'P'
    }
    
    # Define the board size and square size (assuming a 740x740 grid)
    board_size = 8
    square_size = 740 // board_size  # Adjust based on actual board size in pixels if necessary

    # Initialize an empty 8x8 board
    board = [['' for _ in range(board_size)] for _ in range(board_size)]

    # Populate the board array based on predictions
    for prediction in predictions:
        x = prediction['x']
        y = prediction['y']
        piece_class = prediction['class']
        
        # Calculate row and column on the chessboard based on x and y
        col = board_size - 1 - int(x // square_size)  # Reverse column for correct FEN orientation
        row = board_size - 1 - int(y // square_size)  # Flip vertically to align with FEN
        
        if 0 <= row < board_size and 0 <= col < board_size:
            board[row][col] = piece_map.get(piece_class, '')

    # Generate FEN notation
    fen_rows = []
    for row in board:
        fen_row = ""
        empty_count = 0
        for cell in row:
            if cell == '':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += cell
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)

    # Join rows with '/' to complete the FEN string
    fen = "/".join(fen_rows) + " w KQkq - 0 1"  # Default FEN extras

    return fen

# Example usage with simulated predictions
predictions = [
    {'x': 220.5, 'y': 517.5, 'width': 65.0, 'height': 75.0, 'confidence': 0.993, 'class': 'black-knight'},
    {'x': 504.5, 'y': 234.5, 'width': 75.0, 'height': 75.0, 'confidence': 0.988, 'class': 'white-queen'},
    # Add more predictions as needed
]

fen = generate_fen_from_predictions(result['predictions'])
print("FEN:", fen)