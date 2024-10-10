from pynput import mouse

# Function to print the current coordinates of the mouse pointer
def on_move(x, y):
    print(f"Mouse pointer is at ({x}, {y})")

# Set up the listener to track mouse movement
with mouse.Listener(on_move=on_move) as listener:
    listener.join()
