import os
import random
import string

# ---- CONSTANTS ----
NUM_ROWS = 6
NUM_COLS = 7
MAX_COLS = 26
CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Set to 2 for assignment requirements

# ---- FUNCTIONS ----

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    letters = [chr(ord('A') + i) for i in range(cols)]
    # Print header
    print("  " + "   ".join(letters))
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def is_valid_column(input_letter, cols):
    if len(input_letter) != 1 or input_letter not in string.ascii_uppercase[:cols]:
        return False
    return True

def get_available_row(board, col):
    # Return the lowest empty row in the given col, or None if full
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return None

def drop_checker(board, row, col, checker):
    board[row][col] = checker

def check_win(board, checker, needed=4):
    rows = len(board)
    cols = len(board[0])
    # Horizontal
    for r in range(rows):
        for c in range(cols - needed + 1):
            if all(board[r][c+i] == checker for i in range(needed)):
                return True
    # Vertical
    for c in range(cols):
        for r in range(rows - needed + 1):
            if all(board[r+i][c] == checker for i in range(needed)):
                return True
    # Diagonal /
    for r in range(needed-1, rows):
        for c in range(cols - needed + 1):
            if all(board[r-i][c+i] == checker for i in range(needed)):
                return True
    # Diagonal \
    for r in range(rows - needed + 1):
        for c in range(cols - needed + 1):
            if all(board[r+i][c+i] == checker for i in range(needed)):
                return True
    return False

def is_full(board):
    return all(cell != ' ' for row in board for cell in row)

def next_player_idx(current, total):
    return (current + 1) % total

def get_valid_column_input(cols):
    valid_letters = string.ascii_uppercase[:cols]
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if not is_valid_column(user_input, cols):
            print(f"Invalid input. Choose a letter between A and {valid_letters[-1]}.")
            continue
        return ord(user_input) - ord('A')

def game():
    # Initialize variables
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    player_names = [f"Player {p}" for p in players]
    col_labels = [chr(ord('A') + i) for i in range(NUM_COLS)]
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Show initial board
    clear_screen()
    print_board(board, NUM_COLS)
    print(f"{player_names[current_player]}, you start!")

    # Game loop
    while True:
        player = players[current_player]
        print()
        print_board(board, NUM_COLS)
        print(f"{player_names[current_player]} ({player}), please enter a column:")

        col = get_valid_column_input(NUM_COLS)
        row = get_available_row(board, col)
        if row is None:
            print(f"Column {col_labels[col]} is full! You lose your turn.")
            current_player = next_player_idx(current_player, NUM_PLAYERS)
            continue

        drop_checker(board, row, col, player)

        clear_screen()
        print_board(board, NUM_COLS)

        # Win check
        if check_win(board, player, 4):
            print(f"{player_names[current_player]} ({player}) won!")
            break

        # Draw check
        if is_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player = next_player_idx(current_player, NUM_PLAYERS)

if __name__ == "__main__":
    game()
