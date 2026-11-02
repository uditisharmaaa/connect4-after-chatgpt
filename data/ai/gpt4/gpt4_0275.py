import os
import random

# Constants for the game configuration
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = 2  # Set this to 2 for submission
CHECKERS = ['X', 'O', 'V', 'H', 'M']
EMPTY_CELL = " "

# Clear the terminal screen
def clear_screen():
    os.system('clear')

# Initialize the game board
def create_board(rows, columns):
    return [[EMPTY_CELL for _ in range(columns)] for _ in range(rows)]

# Print the board to the terminal
def print_board(board):
    clear_screen()
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(column_labels)
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Check if a column input is valid
def is_valid_column(column, board):
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(ord('A') + COLUMNS - 1)

# Get the row index in the column where the checker should be placed
def get_next_open_row(board, column_index):
    for row in reversed(range(ROWS)):
        if board[row][column_index] == EMPTY_CELL:
            return row
    return None

# Place the checker in the chosen column
def place_checker(board, row, column_index, checker):
    board[row][column_index] = checker

# Check for a win (horizontal, vertical, diagonal)
def check_win(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Diagonal (positive slope) check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Diagonal (negative slope) check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

# Check if the board is full (draw)
def check_draw(board):
    return all(board[0][col] != EMPTY_CELL for col in range(COLUMNS))

# Main game loop
def connect4():
    # Initialize the board
    board = create_board(ROWS, COLUMNS)
    
    # Select players and their checkers
    players = [CHECKERS[i] for i in range(PLAYERS)]
    
    # Randomly select the starting player
    current_player_index = random.randint(0, PLAYERS - 1)
    
    game_over = False
    print_board(board)

    while not game_over:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")
        column = input().strip().upper()

        # Validate the input
        if not is_valid_column(column, board):
            print("Invalid input. Please enter a valid column (e.g., A, B, C).")
            continue
        
        column_index = ord(column) - ord('A')
        
        # Check if the column is full
        row = get_next_open_row(board, column_index)
        if row is None:
            print("Column is full. Choose a different column.")
            continue
        
        # Place the checker
        place_checker(board, row, column_index, current_player)
        print_board(board)
        
        # Check for win/draw
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    connect4()
