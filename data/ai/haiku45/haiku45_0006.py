import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, cols):
    """Initialize the board with empty spaces."""
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the board to the console."""
    os.system("clear")
    rows = len(board)
    cols = len(board[0])
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        letter = chr(ord('A') + col)
        print(f" {letter}  ", end="")
    print()
    
    # Print board rows
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

def get_player_input(cols):
    """Get and validate player input for column selection."""
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Check if input is empty
        if len(user_input) == 0:
            print("Invalid input. Please enter a column letter.")
            continue
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Check if letter is within valid range
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a column between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        return col_index

def can_place_checker(board, col):
    """Check if a checker can be placed in the given column."""
    return board[0][col] == " "

def place_checker(board, col, checker):
    """Place a checker in the given column and return the row where it was placed."""
    rows = len(board)
    
    # Find the lowest available space in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    # Column is full
    return -1

def check_horizontal_win(board, row, col, checker):
    """Check if there is a horizontal win at the given position."""
    cols = len(board[0])
    count = 0
    
    # Check to the left
    for c in range(col, -1, -1):
        if board[row][c] == checker:
            count += 1
        else:
            break
    
    # Check to the right (excluding the current position)
    for c in range(col + 1, cols):
        if board[row][c] == checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH

def check_vertical_win(board, row, col, checker):
    """Check if there is a vertical win at the given position."""
    rows = len(board)
    count = 0
    
    # Check downwards
    for r in range(row, rows):
        if board[r][col] == checker:
            count += 1
        else:
            break
    
    # Check upwards (excluding the current position)
    for r in range(row - 1, -1, -1):
        if board[r][col] == checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH

def check_diagonal_win_right(board, row, col, checker):
    """Check if there is a diagonal win (top-left to bottom-right) at the given position."""
    rows = len(board)
    cols = len(board[0])
    count = 0
    
    # Check up-left
    r, c = row, col
    while r >= 0 and c >= 0:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r -= 1
        c -= 1
    
    # Check down-right (excluding the current position)
    r, c = row + 1, col + 1
    while r < rows and c < cols:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r += 1
        c += 1
    
    return count >= WIN_LENGTH

def check_diagonal_win_left(board, row, col, checker):
    """Check if there is a diagonal win (top-right to bottom-left) at the given position."""
    rows = len(board)
    cols = len(board[0])
    count = 0
    
    # Check up-right
    r, c = row, col
    while r >= 0 and c < cols:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r -= 1
        c += 1
    
    # Check down-left (excluding the current position)
    r, c = row + 1, col - 1
    while r < rows and c >= 0:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r += 1
        c -= 1
    
    return count >= WIN_LENGTH

def check_win(board, row, col, checker):
    """Check if there is a win at the given position."""
    if check_horizontal_win(board, row, col, checker):
        return True
    if check_vertical_win(board, row, col, checker):
        return True
    if check_diagonal_win_right(board, row, col, checker):
        return True
    if check_diagonal_win_left(board, row, col, checker):
        return True
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board(ROWS, COLS)
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    current_checker = CHECKERS[current_player]
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        print(f"Player {current_checker}, ", end="")
        
        # Get valid input from player
        col = get_player_input(COLS)
        
        # Check if column is full
        if not can_place_checker(board, col):
            print("Column is full. You lose this turn.")
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            current_checker = CHECKERS[current_player]
            continue
        
        # Place checker
        row = place_checker(board, col, current_checker)
        
        # Print board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            current_checker = CHECKERS[current_player]

# Run the game
if __name__ == "__main__":
    play_game()
