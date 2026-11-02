import os
import random

# Global constants
BOARD_ROWS = 6
BOARD_COLS = 7
WIN_LENGTH = 4
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create a board with all cells initialized to empty spaces."""
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the board in a formatted way."""
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        letter = chr(ord('A') + col)
        print(f" {letter}  ", end="")
    print()
    
    # Print each row with borders
    for row in range(rows):
        # Print top border
        print("+---" * cols + "+")
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+---" * cols + "+")

def get_column_input(board):
    """Get valid column input from the player."""
    cols = len(board[0])
    
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("That column is full. Please choose another column.")
            continue
        
        return col_index

def place_checker(board, col, checker):
    """Place a checker in the lowest available position in a column."""
    rows = len(board)
    
    # Find the lowest empty cell in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1

def check_win(board, row, col, checker):
    """Check if the last placed checker at (row, col) resulted in a win."""
    rows = len(board)
    cols = len(board[0])
    
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

def check_draw(board):
    """Check if the board is full (draw condition)."""
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board(BOARD_ROWS, BOARD_COLS)
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = PLAYER_CHECKERS[current_player_index]
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        print(f"Player {current_player_checker}, please enter a column: ", end="")
        col = get_column_input(board)
        
        # Place checker
        row = place_checker(board, col, current_player_checker)
        
        # Print board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_player_checker = PLAYER_CHECKERS[current_player_index]

if __name__ == "__main__":
    play_game()
