import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Creates an empty board with the specified dimensions."""
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print each row with borders
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("| ", end="")
        for j in range(COLS):
            print(board[i][j] + " | ", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(column, board):
    """Checks if the given column is valid and has space."""
    # Check if column is within bounds
    if column < 0 or column >= COLS:
        return False
    
    # Check if column has space (top row is empty)
    if board[0][column] != " ":
        return False
    
    return True

def place_checker(board, column, checker):
    """Places a checker in the specified column at the lowest available row."""
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Checks if the last move resulted in a win."""
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r = start_row
    c = start_col
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r = start_row
    c = start_col
    while r >= 0 and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def check_draw(board):
    """Checks if the board is full (draw)."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_input(player_checker):
    """Gets and validates player input for column selection."""
    while True:
        user_input = input("Player " + player_checker + ", please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is an uppercase letter
        if not user_input.isupper():
            print("Invalid input. Please enter an uppercase letter.")
            continue
        
        # Convert letter to column index
        column = ord(user_input) - 65
        
        # Check if column is within bounds
        if column < 0 or column >= COLS:
            print("Invalid column. Please choose a column between A and " + chr(64 + COLS) + ".")
            continue
        
        return column

def main():
    """Main game loop."""
    # Create and initialize the board
    board = create_board()
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        checker = CHECKERS[current_player]
        
        # Get valid column from player
        column = get_player_input(checker)
        
        # Check if column is valid (not full)
        if not is_valid_column(column, board):
            print("Column is full. You lose your turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        # Place the checker
        row = place_checker(board, column, checker)
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, row, column, checker):
            print("Player " + checker + " won!")
            game_over = True
        # Check for a draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
main()
