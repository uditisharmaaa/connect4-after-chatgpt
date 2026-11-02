import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7  # max 26 (A-Z)
MAX_COLS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']

# Use for submission: set to assignment settings
NUM_PLAYERS = 2

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(cols)])
    print(header)
    print('+' + '---+'*cols)
    for row in board:
        row_str = '| ' + ' | '.join(row) + ' |'
        print(row_str)
        print('+' + '---+'*cols)

def find_lowest_spot(board, col):
    """
    Find the lowest empty row index in the given column or return -1 if column is full.
    """
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def is_valid_column(input_col, board):
    if len(input_col) != 1:
        return False
    if not input_col.isalpha():
        return False
    col = ord(input_col.upper()) - ord('A')
    if col < 0 or col >= len(board[0]):
        return False
    return True

def get_player_input(player_marker, board):
    while True:
        user_input = input(f"Player {player_marker}, please enter a column: ").strip().upper()
        if not is_valid_column(user_input, board):
            print(f"Invalid input. Please enter a letter from A to {chr(ord('A') + len(board[0]) - 1)}.")
            continue
        col = ord(user_input) - ord('A')
        if find_lowest_spot(board, col) == -1:
            print("Column is full! You lose your turn.")
            return -1  # Signal turn lost
        return col

def check_win(board, marker):
    rows = len(board)
    cols = len(board[0])
    # Horizontal
    for r in range(rows):
        for c in range(cols-3):
            if all(board[r][c+i] == marker for i in range(4)):
                return True
    # Vertical
    for r in range(rows-3):
        for c in range(cols):
            if all(board[r+i][c] == marker for i in range(4)):
                return True
    # Diagonal \
    for r in range(rows-3):
        for c in range(cols-3):
            if all(board[r+i][c+i] == marker for i in range(4)):
                return True
    # Diagonal /
    for r in range(3, rows):
        for c in range(cols-3):
            if all(board[r-i][c+i] == marker for i in range(4)):
                return True
    return False

def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    # Board and player setup
    board = create_board(BOARD_ROWS, BOARD_COLS)
    player_markers = PLAYER_MARKERS[:NUM_PLAYERS]
    # Randomize who goes first
    cur_player_index = random.randint(0, NUM_PLAYERS-1)
    print_board(board)
    print(f"Player {player_markers[cur_player_index]} goes first!")

    game_over = False
    while not game_over:
        marker = player_markers[cur_player_index]
        col = get_player_input(marker, board)
        if col == -1:
            # If col == -1, column was full, skip turn
            cur_player_index = (cur_player_index + 1) % NUM_PLAYERS
            continue
        row = find_lowest_spot(board, col)
        board[row][col] = marker
        print_board(board)
        if check_win(board, marker):
            print(f"Player {marker} won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            cur_player_index = (cur_player_index + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
