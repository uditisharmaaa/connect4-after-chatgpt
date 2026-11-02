import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Create and initialize an empty board with whitespaces."""
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the board with column labels and formatting."""
    rows = len(board)
    cols = len(board[0])
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        letter = chr(ord('A') + col)
        print(f" {letter}  ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * cols + "+")

def get_column_input(cols, board):
    """Get and validate column input from the player."""
    while True:
        user_input = input("Player " + current_player + ", please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is uppercase letter
        if not user_input.isupper():
            print("Invalid input. Please enter an uppercase letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within board
        if col_index < 0 or col_index >= cols:
            print("Invalid input. Column out of board.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("Invalid input. Column is full.")
            continue
        
        return col_index

def place_checker(board, col, checker):
    """Place a checker in the specified column at the lowest available row."""
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False

def check_horizontal_win(board, checker):
    """Check if there is a horizontal win for the given checker."""
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_vertical_win(board, checker):
    """Check if there is a vertical win for the given checker."""
    rows = len(board)
    cols = len(board[0])
    
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_diagonal_win(board, checker):
    """Check if there is a diagonal win for the given checker."""
    rows = len(board)
    cols = len(board[0])
    
    # Check diagonals going down-right
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonals going down-left
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_win(board, checker):
    """Check if the given checker has won."""
    return (check_horizontal_win(board, checker) or 
            check_vertical_win(board, checker) or 
            check_diagonal_win(board, checker))

def is_board_full(board):
    """Check if the board is completely full."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    global current_player
    
    # Create and initialize board
    board = create_board(ROWS, COLS)
    
    # Get player checkers
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player = players[current_player_index]
    
    # Clear screen and print initial board
    clear_screen()
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        # Get column input from current player
        col = get_column_input(COLS, board)
        
        # Place checker
        place_checker(board, col, current_player)
        
        # Clear screen and print board
        clear_screen()
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("Draw!")
            game_over = True
        # Switch to next player
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_player = players[current_player_index]

# Global variable to track current player
current_player = ""

# Run the game
if __name__ == "__main__":
    play_game()
