import os
import random
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6
COLS = 7
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]  # ['A','B',...,'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
NUM_PLAYERS = 2  # Change to 2..5 as desired

# =========================
# Utility functions
# =========================
def clear_screen():
    # Requirement: use os.system('clear')
    # Attempt to clear for Unix-like; ignore errors on non-Unix.
    try:
        os.system('clear')
    except Exception:
        pass

def create_board(rows=ROWS, cols=COLS):
    return [['.' for _ in range(cols)] for _ in range(rows)]

def print_board(board, players, current_player_index):
    # Header
    print("Connect 4")
    print("Players: " + " ".join(players))
    print(f"Current: {players[current_player_index]}")
    print("  " + " ".join(COLUMN_LABELS))
    # Rows
    for r in range(ROWS):
        print(f"{r+1} " + " ".join(board[r]))
    print()

def col_label_to_index(label):
    label = label.strip().upper()
    if len(label) != 1:
        return None
    if label in COLUMN_LABELS:
        return COLUMN_LABELS.index(label)
    return None

def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    # If top cell is empty, column has space
    return board[0][col] == '.'

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == '.':
            return r
    return None

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == piece and
                board[r][c+1] == piece and
                board[r][c+2] == piece and
                board[r][c+3] == piece):
                return True
    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == piece and
                board[r+1][c] == piece and
                board[r+2][c] == piece and
                board[r+3][c] == piece):
                return True
    # Diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == piece and
                board[r+1][c+1] == piece and
                board[r+2][c+2] == piece and
                board[r+3][c+3] == piece):
                return True
    # Diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == piece and
                board[r-1][c+1] == piece and
                board[r-2][c+2] == piece and
                board[r-3][c+3] == piece):
                return True
    return False

def is_draw(board):
    # Draw if no '.' in top row (board full) and no winner
    return all(cell != '.' for cell in board[0])

def get_player_move(players, current_player_index):
    prompt = f"Player {players[current_player_index]} - choose a column (A-G) or Q to quit: "
    while True:
        choice = input(prompt).strip()
        if not choice:
            print("Please enter a column letter A-G, or Q to quit.")
            continue
        if choice.lower() == 'q':
            return 'quit'
        col = col_label_to_index(choice)
        if col is None:
            print("Invalid input. Please enter a single letter A-G.")
            continue
        return col

def validated_num_players(num):
    if num < 2:
        print("NUM_PLAYERS too low; using 2.")
        return 2
    if num > len(PLAYER_SYMBOLS):
        print(f"NUM_PLAYERS too high; using {len(PLAYER_SYMBOLS)}.")
        return len(PLAYER_SYMBOLS)
    return num

# =========================
# Main game loop
# =========================
def play_game():
    num_players = validated_num_players(NUM_PLAYERS)
    players = PLAYER_SYMBOLS[:num_players]

    board = create_board()

    # Pick random starting player index
    current_player_index = random.randrange(num_players)

    while True:
        clear_screen()
        print_board(board, players, current_player_index)

        move = get_player_move(players, current_player_index)
        if move == 'quit':
            print("Thanks for playing!")
            return

        col = move
        if not is_valid_move(board, col):
            print(f"Column {COLUMN_LABELS[col]} is full or invalid. Press Enter to try again.")
            input()
            continue

        row = get_next_open_row(board, col)
        if row is None:
            print(f"Column {COLUMN_LABELS[col]} is full. Press Enter to try again.")
            input()
            continue

        piece = players[current_player_index]
        drop_piece(board, row, col, piece)

        # Check for win
        if winning_move(board, piece):
            clear_screen()
            print_board(board, players, current_player_index)
            print(f"Player {piece} wins! Congrats!")
            return

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board, players, current_player_index)
            print("It's a draw!")
            return

        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
        sys.exit(0)
