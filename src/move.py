import pyautogui
import cv2
from pynput.mouse import Listener
import mss
import time
from inference_sdk import InferenceHTTPClient

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

    # Calculate the top-left and bottom-right corners
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