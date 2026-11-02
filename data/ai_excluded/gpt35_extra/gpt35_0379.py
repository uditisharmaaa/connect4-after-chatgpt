import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
MAX_COLS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5

# Configuration for this assignment submission
NUM_PLAYERS = 2  # Between 2 and 5
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers
    header = '  '
    for i in range(cols):
        header += '  ' + chr(ord('A') + i) + ' '
    print(header)
    # Print separator and board rows
    sep_line = '+' + ('---+' * cols)
    for row in range(len(board)):
        print(sep_line)
        row_cells = '|'
        for col in range(cols):
            row_cells += ' ' + board[row][col] + ' |'
        print(row_cells)
    print(sep_line)

def valid_column_input(input_str, cols):
    if len(input_str) != 1:
        return False
    char = input_str[0]
    if char < 'A' or char >= chr(ord('A') + cols):
        return False
    return True

def get_column_index(ch):
    return ord(ch) - ord('A')

def column_full(board, col):
    return board[0][col] != ' '

def place_checker(board, col, checker):
    """
    Places the checker in the lowest available cell in column col.
    Returns True if successful, False if the column is full.
    """
    rows = len(board)
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Horizontal check
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + offset] == checker for offset in range(WIN_LENGTH)):
                return True
    # Vertical check
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + offset][col] == checker for offset in range(WIN_LENGTH)):
                return True
    # Diagonal (down-right) check
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + offset][col + offset] == checker for offset in range(WIN_LENGTH)):
                return True
    # Diagonal (down-left) check
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + offset][col - offset] == checker for offset in range(WIN_LENGTH)):
                return True
    return False

def board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def next_player_index(current_idx, num_players):
    return (current_idx + 1) % num_players

def main():
    # Validate configuration
    if not (2 <= NUM_PLAYERS <= MAX_PLAYERS):
        print(f"Number of players must be between 2 and {MAX_PLAYERS}")
        return
    if not (1 <= ROWS <= 100 and 1 <= COLS <= MAX_COLS):
        print(f"Board dimensions must be positive and columns <= {MAX_COLS}")
        return

    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column:"
        valid_input = False
        col_idx = -1

        while not valid_input:
            user_input = input(prompt + " ").strip().upper()
            if not valid_column_input(user_input, COLS):
                continue
            col_idx = get_column_index(user_input)
            # If column full, player loses turn
            if column_full(board, col_idx):
                # Losing turn as per assignment spec
                # Move on to next player after print_board
                break
            else:
                valid_input = True

        if valid_input:
            # Place checker
            placed = place_checker(board, col_idx, current_checker)
            # placed should be True here, but just safety
            if not placed:
                # This case theoretically shouldn't happen, since we check full column earlier
                # But if it happens, treat as turn lost
                pass

        print_board(board)

        # Check for winner only if player placed a checker this turn
        if valid_input:
            if check_winner(board, current_checker):
                print(f"Player {current_checker} won!")
                break

        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Advance to next player
        current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)

if __name__ == "__main__":
    main()
