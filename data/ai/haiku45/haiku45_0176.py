import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, columns):
    """Initialize an empty board with given dimensions."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current board state."""
    os.system('clear')
    rows = len(board)
    columns = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(columns):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        print("+---" * columns + "+")
        print("|", end="")
        for col in range(columns):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * columns + "+")

def is_valid_column(column_letter, columns):
    """Check if the column letter is valid."""
    if len(column_letter) != 1:
        return False
    if not column_letter.isalpha():
        return False
    column_index = ord(column_letter.upper()) - 65
    return 0 <= column_index < columns

def get_column_index(column_letter):
    """Convert column letter to index."""
    return ord(column_letter.upper()) - 65

def is_column_full(board, column_index):
    """Check if a column is completely full."""
    return board[0][column_index] != " "

def place_checker(board, column_index, checker):
    """Place a checker in the lowest available position in a column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = checker
            return row
    return -1

def check_horizontal_win(board, row, column, checker):
    """Check if there's a horizontal win."""
    columns = len(board[0])
    count = 0
    
    # Check left to right
    for col in range(columns):
        if board[row][col] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    return False

def check_vertical_win(board, row, column, checker):
    """Check if there's a vertical win."""
    rows = len(board)
    count = 0
    
    # Check top to bottom
    for r in range(rows):
        if board[r][column] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    return False

def check_diagonal_win(board, row, column, checker):
    """Check if there's a diagonal win (both directions)."""
    rows = len(board)
    columns = len(board[0])
    
    # Check diagonal from top-left to bottom-right
    count = 0
    start_row = row - min(row, column)
    start_col = column - min(row, column)
    
    r, c = start_row, start_col
    while r < rows and c < columns:
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal from top-right to bottom-left
    count = 0
    start_row = row - min(row, columns - 1 - column)
    start_col = column + min(row, columns - 1 - column)
    
    r, c = start_row, start_col
    while r < rows and c >= 0:
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c -= 1
    
    return False

def check_win(board, row, column, checker):
    """Check if the last move resulted in a win."""
    return (check_horizontal_win(board, row, column, checker) or
            check_vertical_win(board, row, column, checker) or
            check_diagonal_win(board, row, column, checker))

def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board(ROWS, COLUMNS)
    
    # Choose random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    game_over = False
    winner = None
    
    while not game_over:
        checker = PLAYER_CHECKERS[current_player]
        
        # Get valid input from player
        while True:
            try:
                column_input = input(f"Player {checker}, please enter a column: ").strip().upper()
                
                if not is_valid_column(column_input, COLUMNS):
                    print(f"Invalid column. Please enter a letter from A to {chr(65 + COLUMNS - 1)}.")
                    continue
                
                column_index = get_column_index(column_input)
                
                if is_column_full(board, column_index):
                    print("Column is full. Please choose another column.")
                    continue
                
                break
            except Exception as e:
                print("Invalid input. Please try again.")
        
        # Place checker and get the row where it was placed
        row = place_checker(board, column_index, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, column_index, checker):
            print(f"Player {checker} won!")
            game_over = True
            winner = checker
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
