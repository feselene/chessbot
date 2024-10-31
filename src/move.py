import cv2
import mss
from inference_sdk import InferenceHTTPClient
import subprocess
import time

CLIENT = InferenceHTTPClient(
    api_url="https://outline.roboflow.com",
    api_key="23rLdZSuKttIzDN4MKCd"
)

def generate_fen_from_predictions(predictions, board_length = 740):
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
    square_size = board_length // board_size  # Adjust based on actual board size in pixels if necessary

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
    fen = "/".join(fen_rows) + " b - - 2 33"  # Default FEN extras

    return fen

def capture_screenshot():
    with mss.mss() as sct: 
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)

        output_file = "screenshot.png"
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=output_file)
        print(f"Screenshot saved to {output_file}")

capture_screenshot()
result = CLIENT.infer("screenshot.png", model_id="chessboard-segmentation/1")
image = cv2.imread("screenshot.png")

width = 740

if (result['predictions']):
    x = int(result['predictions'][0]['x'])
    y = int(result['predictions'][0]['y'])

    width = int(result['predictions'][0]['width'])
    height = int(result['predictions'][0]['height'])
    
    print("width: ", width)
    print("height: ", height)
    
    # Calculate the top-left and bottom-right corners
    top_left = (x - width // 2, y - height // 2)
    bottom_right = (x + width // 2, y + height // 2)

    # Crop the image using the calculated coordinates
    cropped_image = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    cv2.imwrite("cropped_screenshot.png", cropped_image)

    CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="23rLdZSuKttIzDN4MKCd"
)

    result = CLIENT.infer("cropped_screenshot.png", model_id="2dcpd/2")
else:
    print("No prediction available.")

import subprocess
import time

def get_best_move_from_fen(fen, laser_path="Laser-1_7.exe"):
    depth = 20  # Depth to search for the best move, you can adjust this as needed
    timeout = 5  # Timeout for each Laser response

    try:
        # Start the Laser chess engine
        process = subprocess.Popen(
            laser_path,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Initialize UCI and check readiness
        process.stdin.write("uci\n")
        process.stdin.flush()
        
        # Wait for the 'uciok' response with a timeout
        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError("Laser initialization timed out.")
            output = process.stdout.readline().strip()
            if output == "uciok":
                break

        # Send the FEN position to Laser
        process.stdin.write(f"position fen {fen}\n")
        process.stdin.flush()

        # Ask Laser to calculate the best move
        process.stdin.write(f"go depth {depth}\n")
        process.stdin.flush()

        # Wait for the best move with a timeout
        best_move = None
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError("Laser move calculation timed out.")
            
            output = process.stdout.readline().strip()
            if output.startswith("bestmove"):
                best_move = output.split(" ")[1]
                break

        # Close the Laser process
        process.stdin.write("quit\n")
        process.stdin.flush()
        process.terminate()

        return best_move

    except TimeoutError as e:
        if process:
            process.terminate()
        print(e)
        return None
    except Exception as e:
        if process:
            process.terminate()
        print(f"An error occurred: {e}")
        return None



fen = generate_fen_from_predictions(result['predictions'], width)
print(fen)
# Example usage
fen = "5bk1/3R4/7p/6p1/p2B4/P5P1/1Pr2PKP/8 b - - 0 1"
best_move = get_best_move_from_fen(fen)
print("Best move:", best_move)