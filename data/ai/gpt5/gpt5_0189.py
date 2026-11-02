import os
import random
import string

# Configuration (submission requires 6 rows x 7 cols and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
TOKENS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def col_labels(cols):
    return list(string.ascii_uppercase[:cols])

def print_board(board):
    clear_screen()
    labels = col_labels(len(board[0]))
    # Header
    print("  " + "   ".join(labels))
    # Rows
    sep = "+" + "+".join(["---"] * len(labels)) + "+"
    for r in range(len(board)):
        print(sep)
        row = "|" + "|".join(f" {board[r][c]} " for c in range(len(labels))) + "|"
        print(row)
    print(sep)

def get_move(player_token):
    labels = col_labels(COLS)
    while True:
        move = input(f"Player {player_token}, please enter a column: ").strip().upper()
        if len(move) == 1 and move in labels:
            return labels.index(move)
        # Invalid input, reprompt (turn not lost)
        print("Invalid input. Enter a valid column letter (e.g., A, B, ...).")

def drop_checker(board, col, token):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r, col
    return None  # column full

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, token):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + k] == token for k in range(4)):
                return True
    # Vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + k][c] == token for k in range(4)):
                return True
    # Diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + k][c + k] == token for k in range(4)):
                return True
    # Diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - k][c + k] == token for k in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    assert 2 <= NUM_PLAYERS <= 5, "Players must be between 2 and 5."
    assert 1 <= COLS <= 26, "Columns must be between 1 and 26."
    board = create_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    print_board(board)  # show empty board before first move
    while True:
        token = TOKENS[current]
        col = get_move(token)
        placed = drop_checker(board, col, token)
        if placed is None:
            # Column full: turn is invalid and player loses the turn
            print_board(board)
            print(f"Column {col_labels(COLS)[col]} is full. Turn lost.")
            current = (current + 1) % NUM_PLAYERS
            continue
        print_board(board)
        if check_win(board, token):
            print(f"Player {token} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
