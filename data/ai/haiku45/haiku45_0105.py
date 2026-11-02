import os
import random

# Constants for board configuration
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, columns):
    """Create and return an empty board with given dimensions."""
    board = []
    for i in range(rows):
        row = []
        for j in range(columns):
            row.append(" ")
        board.append(row)
    return board

def print_board(board, columns):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(columns):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * columns + "+")
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
    print("+---" * columns + "+")

def get_player_input(columns, board):
    """Get and validate player input for column selection."""
    while True:
        user_input = input("Player " + current_player + ", please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert to uppercase
        user_input = user_input.upper()
        
        # Check if column is within board range
        column_index = ord(user_input) - ord('A')
        if column_index < 0 or column_index >= columns:
            print("Invalid column. Please enter a column between A and " + chr(ord('A') + columns - 1) + ".")
            continue
        
        # Check if column is full
        if board[0][column_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return column_index

def place_checker(board, column_index, checker, rows):
    """Place a checker in the specified column and return True if successful."""
    # Find the lowest empty row in the column
    for row_index in range(rows - 1, -1, -1):
        if board[row_index][column_index] == " ":
            board[row_index][column_index] = checker
            return True
    return False

def check_horizontal_win(board, rows, columns, checker):
    """Check if the player has won horizontally."""
    for row in range(rows):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_vertical_win(board, rows, columns, checker):
    """Check if the player has won vertically."""
    for col in range(columns):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_diagonal_down_right(board, rows, columns, checker):
    """Check if the player has won diagonally (top-left to bottom-right)."""
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_diagonal_down_left(board, rows, columns, checker):
    """Check if the player has won diagonally (top-right to bottom-left)."""
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, columns):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_win(board, rows, columns, checker):
    """Check if the current player has won."""
    if check_horizontal_win(board, rows, columns, checker):
        return True
    if check_vertical_win(board, rows, columns, checker):
        return True
    if check_diagonal_down_right(board, rows, columns, checker):
        return True
    if check_diagonal_down_left(board, rows, columns, checker):
        return True
    return False

def is_board_full(board, rows, columns):
    """Check if the board is full (draw condition)."""
    for row in range(rows):
        for col in range(columns):
            if board[row][col] == " ":
                return False
    return True

def main():
    """Main game loop."""
    global current_player
    
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Create list of players
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player = players[current_player_index]
    
    # Print initial board
    print_board(board, COLUMNS)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get player input
        column_index = get_player_input(COLUMNS, board)
        
        # Place checker
        place_checker(board, column_index, current_player, ROWS)
        
        # Print updated board
        print_board(board, COLUMNS)
        
        # Check for win
        if check_win(board, ROWS, COLUMNS, current_player):
            print("Player " + current_player + " won!")
            game_over = True
        # Check for draw
        elif is_board_full(board, ROWS, COLUMNS):
            print("It's a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_player = players[current_player_index]

if __name__ == "__main__":
    main()
