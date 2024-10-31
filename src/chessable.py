import subprocess

def get_best_move(fen, stockfish_path="stockfish\stockfish-windows-x86-64-avx2.exe"):
    # Start the Stockfish engine
    process = subprocess.Popen(
        stockfish_path, 
        universal_newlines=True, 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Initialize communication with Stockfish
    process.stdin.write("uci\n")
    process.stdin.flush()

    # Wait for Stockfish to be ready
    while True:
        output = process.stdout.readline().strip()
        if output == "uciok":
            break

    # Send the position (FEN) to Stockfish
    process.stdin.write(f"position fen {fen}\n")
    process.stdin.flush()

    # Tell Stockfish to calculate the best move
    process.stdin.write("go depth 20\n")
    process.stdin.flush()

    # Read lines until we find the best move
    best_move = None
    while True:
        output = process.stdout.readline().strip()
        if output.startswith("bestmove"):
            best_move = output.split(" ")[1]
            break

    # Close the Stockfish process
    process.stdin.write("quit\n")
    process.stdin.flush()
    process.terminate()

    return best_move

# Example usage:
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
best_move = get_best_move(fen)
print("Best move:", best_move)
