import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, columns):
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the game board to the console."""
    os.system('clear')
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(headers)
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(row))

def is_valid_input(user_input, columns):
    """Check if the user input is valid."""
    if len(user_input) != 1:
        return False
    col = ord(user_input.upper()) - ord('A')
    return 0 <= col < columns

def drop_checker(board, col, checker):
    """Place the checker in the appropriate row in the chosen column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_winner(board, checker):
    """Check if the current player has won the game."""
    # Check horizontal, vertical and diagonal win conditions
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (
                c <= COLUMNS - 4 and all(board[r][c + i] == checker for i in range(4)) or
                r <= ROWS - 4 and all(board[r + i][c] == checker for i in range(4)) or
                c <= COLUMNS - 4 and r <= ROWS - 4 and all(board[r + i][c + i] == checker for i in range(4)) or
                c >= 3 and r <= ROWS - 4 and all(board[r + i][c - i] == checker for i in range(4))
            ):
                return True
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def connect_four():
    num_players = 2  # Adjust this to change the number of players
    checkers = CHECKERS[:num_players]
    
    # Initialize board and first player
    board = initialize_board(ROWS, COLUMNS)
    current_player = random.choice(checkers)
    
    while True:
        print_board(board)
        user_input = input(f"Player {current_player}, please enter a column: ").strip()
        
        while not is_valid_input(user_input, COLUMNS) or not drop_checker(board, ord(user_input.upper()) - ord('A'), current_player):
            user_input = input("Invalid input. Please enter a valid column: ").strip()
        
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch players
        current_player = checkers[(checkers.index(current_player) + 1) % num_players]

# Run the game
connect_four()
