import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the board with column labels."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board rows with separators
    for row in range(ROWS):
        print("+" + "---+" * COLS)
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+" + "---+" * COLS)


def is_valid_column(column_input):
    """Check if the column input is valid."""
    if len(column_input) != 1:
        return False
    if not column_input.isalpha():
        return False
    if not column_input.isupper():
        return False
    col_index = ord(column_input) - ord('A')
    if col_index < 0 or col_index >= COLS:
        return False
    return True


def is_column_full(board, col_index):
    """Check if a column is full."""
    return board[0][col_index] != " "


def place_checker(board, col_index, checker):
    """Place a checker in the specified column. Returns True if successful."""
    if is_column_full(board, col_index):
        return False
    
    # Find the lowest available row
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False


def check_win(board, checker):
    """Check if the specified checker has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is full (draw condition)."""
    return all(board[0][col] != " " for col in range(COLS))


def get_player_input(player_checker):
    """Get and validate player input."""
    while True:
        column_input = input(f"Player {player_checker}, please enter a column: ")
        
        if not is_valid_column(column_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        return ord(column_input) - ord('A')


def play_game():
    """Main game loop."""
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_index]
        
        col_index = get_player_input(current_checker)
        
        if is_column_full(board, col_index):
            print("Column is full. You lose your turn.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        place_checker(board, col_index, current_checker)
        print_board(board)
        
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
