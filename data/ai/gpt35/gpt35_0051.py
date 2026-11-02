import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4

# Players and their checkers, ordered
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    # Create a 2D list (rows x columns) initialized with " "
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers (A, B, C, ...)
    headers = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print("  " + "   ".join(headers))
    
    # Print board rows
    for row in board:
        print("+" + "---+"*len(row))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+"*len(board[0]))

def choose_first_player(num_players):
    return random.randint(0, num_players - 1)

def valid_input(input_str, columns):
    # Check single uppercase letter and in board range
    if len(input_str) != 1:
        return False
    if input_str not in string.ascii_uppercase[:columns]:
        return False
    return True

def column_index(letter):
    # Convert column letter to an index (0-based)
    return string.ascii_uppercase.index(letter)

def place_checker(board, col, checker):
    """
    Attempts to place checker in column col.
    Checker falls to the lowest empty row in the column.
    Returns True if placed successfully, False if column full.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def board_full(board):
    # Board is full if no spaces left in top row of every column
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    return True

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])
    
    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c+i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r+i][c] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Diagonal down-right check (\)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Diagonal up-right check (/)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def main():
    # Settings for this submission (2 players, 6x7 board)
    rows = ROWS
    columns = COLUMNS
    num_players = 2
    players = CHECKERS[:num_players]

    board = create_board(rows, columns)
    current_player = choose_first_player(num_players)

    print_board(board)

    while True:
        checker = players[current_player]
        prompt = f"Player {checker}, please enter a column: "

        # Input loop for valid input (except full column)
        while True:
            user_input = input(prompt).strip().upper()
            if not valid_input(user_input, columns):
                # Invalid input: not a single valid column letter
                continue
            col = column_index(user_input)
            # Check if column full
            if board[0][col] != " ":
                # Column full: turn lost, break input loop with invalid place
                place_success = False
                break
            else:
                place_success = place_checker(board, col, checker)
                break

        if place_success:
            print_board(board)
            if check_winner(board, checker):
                print(f"Player {checker} won!")
                break
            if board_full(board):
                print("The game is a draw.")
                break
        else:
            # Column full, turn lost, announce nothing, just continue
            print_board(board)

        # Next player's turn
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
