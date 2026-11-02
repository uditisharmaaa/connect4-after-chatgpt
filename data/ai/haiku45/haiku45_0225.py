import os
import random

# Game constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, cols):
    """Create and return an empty board with the specified dimensions."""
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print board with borders
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * cols + "+")

def is_valid_column(column_letter, cols):
    """Check if the column letter is valid."""
    if len(column_letter) != 1:
        return False
    if not column_letter.isalpha():
        return False
    col_index = ord(column_letter.upper()) - ord('A')
    if col_index < 0 or col_index >= cols:
        return False
    return True

def get_player_input(player_checker, cols):
    """Get and validate player input for column choice."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ")
        if is_valid_column(user_input, cols):
            return ord(user_input.upper()) - ord('A')
        else:
            print("Invalid input. Please enter a valid column letter.")

def can_place_checker(board, col):
    """Check if a checker can be placed in the given column."""
    if board[0][col] == " ":
        return True
    return False

def place_checker(board, col, checker):
    """Place a checker in the specified column and return the row where it was placed."""
    rows = len(board)
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_horizontal_win(board, row, col, checker):
    """Check if there are 4 checkers in a row horizontally."""
    count = 0
    cols = len(board[0])
    
    for c in range(cols):
        if board[row][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    return False

def check_vertical_win(board, row, col, checker):
    """Check if there are 4 checkers in a row vertically."""
    count = 0
    rows = len(board)
    
    for r in range(rows):
        if board[r][col] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    return False

def check_diagonal_win(board, row, col, checker):
    """Check if there are 4 checkers in a row diagonally (both directions)."""
    rows = len(board)
    cols = len(board[0])
    
    # Check diagonal from top-left to bottom-right
    count = 0
    r, c = row, col
    # Go to the start of the diagonal
    while r > 0 and c > 0:
        r -= 1
        c -= 1
    # Count along the diagonal
    while r < rows and c < cols:
        if board[r][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal from top-right to bottom-left
    count = 0
    r, c = row, col
    # Go to the start of the diagonal
    while r > 0 and c < cols - 1:
        r -= 1
        c += 1
    # Count along the diagonal
    while r < rows and c >= 0:
        if board[r][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c -= 1
    
    return False

def check_win(board, row, col, checker):
    """Check if the current move results in a win."""
    if check_horizontal_win(board, row, col, checker):
        return True
    if check_vertical_win(board, row, col, checker):
        return True
    if check_diagonal_win(board, row, col, checker):
        return True
    return False

def is_board_full(board):
    """Check if the board is full (draw condition)."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    print(f"Player {CHECKERS[current_player]} starts the game!")
    
    # Game loop
    game_over = False
    winner = None
    
    while not game_over:
        # Get player input
        col = get_player_input(CHECKERS[current_player], COLS)
        
        # Check if move is valid
        if not can_place_checker(board, col):
            print("This column is full. Please choose another column.")
            continue
        
        # Place the checker
        row = place_checker(board, col, CHECKERS[current_player])
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            game_over = True
            winner = current_player
        
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        # Switch to next player
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
