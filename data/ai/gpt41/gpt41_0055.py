import os
import random
import string

# ======= CONSTANT VARIABLES =======
NUM_ROWS = 6           # Default: 6 rows
NUM_COLS = 7           # Default: 7 columns (max 26)
NUM_PLAYERS = 2        # Players (between 2 and 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Symbols for up to 5 players

# Number needed in a row to win
WIN_LEN = 4

# For clearing the terminal screen
def clear_screen():
    os.system('clear')

# Create the board
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    cols = len(board[0])
    col_labels = '  '.join(string.ascii_uppercase[:cols])
    print('\n  ' + col_labels)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

# Check if a column label is valid and returns corresponding column index
def get_column_index(user_input, num_cols):
    if len(user_input) != 1 or user_input not in string.ascii_uppercase[:num_cols]:
        return -1
    return string.ascii_uppercase.index(user_input)

# Place a checker in the chosen column for the player
def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False  # Column is full

# Check if board is full (draw)
def is_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

# Check for win condition from a certain position
def check_win_from_cell(board, row, col, checker):
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LEN:
            return True
    return False

# Check if the last move was a winning move
def check_win(board, checker):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == checker:
                if check_win_from_cell(board, r, c, checker):
                    return True
    return False

def main():
    # Setup game
    board = create_board(NUM_ROWS, NUM_COLS)
    player_symbols = CHECKERS[:NUM_PLAYERS]
    player_names = [f"Player {symbol}" for symbol in player_symbols]
    cur_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Initial board display
    clear_screen()
    print_board(board)

    # Main game loop
    while True:
        symbol = player_symbols[cur_player_index]
        name = player_names[cur_player_index]

        # Prompt for move
        print(f"{name} ({symbol}), please enter a column:", end=' ')
        user_input = input().strip().upper()

        # Validate input
        col_idx = get_column_index(user_input, NUM_COLS)
        if col_idx == -1:
            clear_screen()
            print_board(board)
            print("Invalid input! Column must be a single letter from A to", string.ascii_uppercase[NUM_COLS-1])
            continue
        # Check if column is full
        if board[0][col_idx] != ' ':
            clear_screen()
            print_board(board)
            print(f"Column {user_input} is already full! You lose your turn.")
            # Skip to next player
            cur_player_index = (cur_player_index + 1) % NUM_PLAYERS
            continue

        # Place checker
        if not place_checker(board, col_idx, symbol):
            clear_screen()
            print_board(board)
            print("Unexpected error placing checker. Try a different column.")
            continue

        # Update board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, symbol):
            print(f"{name} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        cur_player_index = (cur_player_index + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
