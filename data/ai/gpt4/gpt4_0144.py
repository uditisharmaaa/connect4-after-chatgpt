import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "
COLUMN_LETTERS = [chr(i) for i in range(ord('A'), ord('A') + COLUMNS)]

# Helper functions
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def initialize_board():
    return [[EMPTY_CELL for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(COLUMN_LETTERS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    if column not in COLUMN_LETTERS:
        return False
    col_index = COLUMN_LETTERS.index(column)
    return board[0][col_index] == EMPTY_CELL  # Check if column is not full

def get_available_row(column, board):
    col_index = COLUMN_LETTERS.index(column)
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == EMPTY_CELL:
            return row
    return None

def place_checker(column, player_checker, board):
    row = get_available_row(column, board)
    if row is not None:
        col_index = COLUMN_LETTERS.index(column)
        board[row][col_index] = player_checker
        return True
    return False

def check_winner(board, player_checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player_checker for i in range(4)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_checker for i in range(4)):
                return True

    # Diagonal (bottom left to top right) check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_checker for i in range(4)):
                return True

    # Diagonal (top left to bottom right) check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != EMPTY_CELL for col in range(COLUMNS))

# Main game logic
def play_connect_4():
    # Settings
    num_players = 2
    player_checkers = PLAYER_CHECKERS[:num_players]
    board = initialize_board()
    
    # Select starting player
    current_player = random.randint(0, num_players - 1)
    clear_screen()
    print("Welcome to Connect 4!")
    print(f"Starting player: Player {player_checkers[current_player]}")
    print_board(board)

    while True:
        # Current player's turn
        player_checker = player_checkers[current_player]
        print(f"Player {player_checker}, it's your turn.")
        column = input(f"Enter a column (A-{COLUMN_LETTERS[COLUMNS-1]}): ").strip().upper()

        # Validate input
        while not is_valid_column(column, board):
            print("Invalid column. Please try again.")
            column = input(f"Enter a column (A-{COLUMN_LETTERS[COLUMNS-1]}): ").strip().upper()

        # Place the checker
        place_checker(column, player_checker, board)
        print_board(board)

        # Check for a win
        if check_winner(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % num_players

# Run the game
if __name__ == "__main__":
    play_connect_4()
