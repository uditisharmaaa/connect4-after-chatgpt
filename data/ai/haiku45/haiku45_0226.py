import os
import random

# Constants for board configuration
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checker symbols
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Get the checkers for the current game
ACTIVE_CHECKERS = CHECKERS[:NUM_PLAYERS]

def initialize_board():
    """
    Initialize the board with empty cells (whitespaces).
    Returns a 2D list representing the board.
    """
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return board

def print_board(board):
    """
    Print the current state of the board with column labels and formatting.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(NUM_COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board with separators
    for row in range(NUM_ROWS):
        # Print top separator
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for col in range(NUM_COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom separator
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

def is_valid_column(column_input):
    """
    Validate if the input is a valid column letter.
    Returns the column index if valid, -1 otherwise.
    """
    if len(column_input) != 1:
        return -1
    
    if not column_input.isalpha():
        return -1
    
    column_index = ord(column_input.upper()) - 65
    
    if column_index < 0 or column_index >= NUM_COLS:
        return -1
    
    return column_index

def is_column_full(board, column):
    """
    Check if a column is completely filled with checkers.
    """
    return board[0][column] != ' '

def place_checker(board, column, checker):
    """
    Place a checker in the specified column at the lowest available row.
    Returns True if placement is successful, False if column is full.
    """
    # Find the lowest empty row in the column
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            return True
    
    return False

def check_direction(board, row, col, checker, row_delta, col_delta):
    """
    Check if there are 4 checkers in a row in a specific direction.
    row_delta and col_delta define the direction to check.
    """
    count = 0
    current_row = row
    current_col = col
    
    while (0 <= current_row < NUM_ROWS and 
           0 <= current_col < NUM_COLS and 
           board[current_row][current_col] == checker):
        count += 1
        current_row += row_delta
        current_col += col_delta
    
    return count

def check_win(board, row, col, checker):
    """
    Check if the last placed checker results in a win.
    A win is 4 checkers in a row horizontally, vertically, or diagonally.
    """
    # Directions: horizontal, vertical, diagonal /, diagonal \
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal \
        (1, -1)   # Diagonal /
    ]
    
    for row_delta, col_delta in directions:
        # Check in both directions
        count_forward = check_direction(board, row, col, checker, row_delta, col_delta)
        count_backward = check_direction(board, row, col, checker, -row_delta, -col_delta)
        
        # Total count includes the current checker and all consecutive checkers
        total_count = count_forward + count_backward - 1
        
        if total_count >= WIN_LENGTH:
            return True
    
    return False

def is_board_full(board):
    """
    Check if the board is completely filled (draw condition).
    """
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == ' ':
                return False
    return True

def get_player_move(board, current_player):
    """
    Get valid column input from the current player.
    Keep asking until valid input is received.
    """
    while True:
        user_input = input(f"Player {ACTIVE_CHECKERS[current_player]}, please enter a column: ")
        
        column = is_valid_column(user_input)
        
        if column == -1:
            print("Invalid input. Please enter a column letter (A-" + 
                  chr(65 + NUM_COLS - 1) + ").")
            continue
        
        if is_column_full(board, column):
            print("Column is full. Please choose another column.")
            continue
        
        return column

def play_game():
    """
    Main game loop. Handles initialization, turns, win/draw checking.
    """
    # Initialize board
    board = initialize_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    game_over = False
    
    while not game_over:
        # Get player's move
        column = get_player_move(board, current_player)
        
        # Place checker
        checker = ACTIVE_CHECKERS[current_player]
        
        # Find the row where the checker is placed
        placed_row = -1
        for row in range(NUM_ROWS - 1, -1, -1):
            if board[row][column] == ' ':
                placed_row = row
                break
        
        place_checker(board, column, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, placed_row, column, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS

def main():
    """
    Entry point of the program.
    """
    play_game()

if __name__ == "__main__":
    main()
