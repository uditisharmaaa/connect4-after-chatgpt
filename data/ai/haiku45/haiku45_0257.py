import os
import random

# Global constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board(rows, cols):
    """Create an empty board with given dimensions."""
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board


def print_board(board, cols):
    """Print the board with column labels and formatting."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(cols):
        letter = chr(ord('A') + i)
        print(f" {letter}  ", end="")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    print("+---" * cols + "+")


def is_valid_input(column_input, cols):
    """Check if the input is valid."""
    if len(column_input) != 1:
        return False
    
    if not column_input.isalpha():
        return False
    
    column_input = column_input.upper()
    col_index = ord(column_input) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return False
    
    return True


def get_column_index(column_input):
    """Convert column letter to index."""
    return ord(column_input.upper()) - ord('A')


def can_place_checker(board, col_index, cols):
    """Check if a checker can be placed in the given column."""
    if col_index < 0 or col_index >= cols:
        return False
    
    # Check if the top cell of the column is empty
    if board[0][col_index] != " ":
        return False
    
    return True


def place_checker(board, col_index, checker, rows):
    """Place a checker in the given column and return the row where it was placed."""
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    
    return -1


def check_win(board, row, col, checker, rows, cols):
    """Check if the current move results in a win."""
    # Check horizontal
    count = 1
    
    # Check left
    j = col - 1
    while j >= 0 and board[row][j] == checker:
        count += 1
        j -= 1
    
    # Check right
    j = col + 1
    while j < cols and board[row][j] == checker:
        count += 1
        j += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    
    # Check up
    i = row - 1
    while i >= 0 and board[i][col] == checker:
        count += 1
        i -= 1
    
    # Check down
    i = row + 1
    while i < rows and board[i][col] == checker:
        count += 1
        i += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    
    # Check up-left
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0 and board[i][j] == checker:
        count += 1
        i -= 1
        j -= 1
    
    # Check down-right
    i, j = row + 1, col + 1
    while i < rows and j < cols and board[i][j] == checker:
        count += 1
        i += 1
        j += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    
    # Check up-right
    i, j = row - 1, col + 1
    while i >= 0 and j < cols and board[i][j] == checker:
        count += 1
        i -= 1
        j += 1
    
    # Check down-left
    i, j = row + 1, col - 1
    while i < rows and j >= 0 and board[i][j] == checker:
        count += 1
        i += 1
        j -= 1
    
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board, rows, cols):
    """Check if the board is full (draw condition)."""
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == " ":
                return False
    
    return True


def play_game():
    """Main game loop."""
    # Create board
    board = create_board(ROWS, COLS)
    
    # Get player checkers
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLS)
    
    # Game loop
    game_over = False
    
    while not game_over:
        current_checker = players[current_player_index]
        
        # Get valid input from player
        valid_input = False
        while not valid_input:
            user_input = input(f"Player {current_checker}, please enter a column: ")
            
            if not is_valid_input(user_input, COLS):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            col_index = get_column_index(user_input)
            
            if not can_place_checker(board, col_index, COLS):
                print("Column is full or invalid. Please try another column.")
                continue
            
            valid_input = True
        
        # Place checker
        row = place_checker(board, col_index, current_checker, ROWS)
        
        # Print board
        print_board(board, COLS)
        
        # Check for win
        if check_win(board, row, col_index, current_checker, ROWS, COLS):
            print(f"Player {current_checker} won!")
            game_over = True
        
        # Check for draw
        elif is_board_full(board, ROWS, COLS):
            print("It's a draw!")
            game_over = True
        
        # Switch to next player
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
