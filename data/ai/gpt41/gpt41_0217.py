import os
import random
import sys

# ========== CONSTANT VARIABLES ==========
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2  # for submission, set to 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LETTERS = [chr(ord('A') + i) for i in range(COLUMNS)]

# ========== FUNCTIONS ==========

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board(rows, cols):
    """Creates a 2D list for the game board, initialized to ' '."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board to the console in the required format."""
    # Print column letters
    print('  ' + '   '.join(COLUMN_LETTERS))
    # Print top border
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def is_valid_column(input_col):
    """Checks if the chosen column is valid (exists and letter)."""
    return input_col in COLUMN_LETTERS

def is_column_not_full(board, col_idx):
    """Returns True if there is space in the column."""
    return board[0][col_idx] == ' '

def drop_checker(board, col_idx, checker):
    """Places a checker in the chosen column if possible. Returns True if successful."""
    for row in reversed(board):
        if row[col_idx] == ' ':
            row[col_idx] = checker
            return True
    return False  # Column is full

def board_full(board):
    """Checks if the entire board is full."""
    return all(cell != ' ' for cell in board[0])

def check_winner(board, checker):
    """Checks if the player with 'checker' has won."""
    # Horizontal Check
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    # Vertical Check
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    # Diagonal /
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    # Diagonal \
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    return False

def get_valid_player_input(board):
    """Asks user for input, checks for validity, returns column index or None if full."""
    while True:
        user_input = input().strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter for the column (e.g. A, B, C).")
            continue
        if not user_input.isalpha():
            print("Invalid input. Please enter a valid column letter (A-G).")
            continue
        if not is_valid_column(user_input):
            print("Invalid column. Please select a letter from A to {}.".format(COLUMN_LETTERS[-1]))
            continue
        col_idx = COLUMN_LETTERS.index(user_input)
        if not is_column_not_full(board, col_idx):
            print("This column is full. You lose your turn.")
            return None  # Player loses turn per instructions
        return col_idx

def main():
    board = create_board(ROWS, COLUMNS)
    player_checkers = CHECKERS[:NUM_PLAYERS]
    player_names = ["Player {}".format(c) for c in player_checkers]
    # Randomly choose who starts
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    clear_screen()
    print_board(board)
    print()

    while True:
        player_checker = player_checkers[current_player]
        print("{} ({}), please enter a column: ".format(player_names[current_player], player_checker))

        col_idx = get_valid_player_input(board)
        if col_idx is None:
            # Column is full, player loses turn
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        # Place checker
        drop_checker(board, col_idx, player_checker)
        
        clear_screen()
        print_board(board)
        print()

        # Check for winner
        if check_winner(board, player_checker):
            print("{} won!".format(player_names[current_player]))
            break
        
        if board_full(board):
            print("It's a draw!")
            break
        
        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
