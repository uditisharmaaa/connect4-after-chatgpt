import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board"""
    board = []
    for i in range(NUM_ROWS):
        row = []
        for j in range(NUM_COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(NUM_COLS):
        print(chr(65 + i), end="   ")
    print()
    
    # Print rows with borders
    for row in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("|", end="")
        for col in range(NUM_COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * NUM_COLS + "+")

def is_valid_move(board, col):
    """Check if a move is valid (column not full and within bounds)"""
    if col < 0 or col >= NUM_COLS:
        return False
    # Check if top row of column is empty
    if board[0][col] != " ":
        return False
    return True

def place_checker(board, col, checker):
    """Place a checker in the specified column"""
    # Find the lowest empty row in the column
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win"""
    
    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(NUM_ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    # Find starting position
    start_row = row
    start_col = col
    while start_row < NUM_ROWS - 1 and start_col > 0:
        start_row += 1
        start_col -= 1
    # Count along diagonal
    r = start_row
    c = start_col
    while r >= 0 and c < NUM_COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    # Find starting position
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    # Count along diagonal
    r = start_row
    c = start_col
    while r < NUM_ROWS and c < NUM_COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    return False

def check_draw(board):
    """Check if the board is full (draw)"""
    for col in range(NUM_COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_move(board, player_checker):
    """Get and validate player input"""
    while True:
        move = input("Player " + player_checker + ", please enter a column: ")
        
        # Check if input is a single character
        if len(move) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Convert to uppercase
        move = move.upper()
        
        # Check if it's a letter
        if not move.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(move) - 65
        
        # Check if column is valid
        if col < 0 or col >= NUM_COLS:
            print("Invalid column. Please choose a column between A and " + chr(65 + NUM_COLS - 1) + ".")
            continue
        
        # Check if column is full
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col

def main():
    """Main game function"""
    # Create the board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        player_checker = CHECKERS[current_player]
        
        # Get player move
        col = get_player_move(board, player_checker)
        
        # Place checker
        row = place_checker(board, col, player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, player_checker):
            print("Player " + player_checker + " won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("Game is a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
main()
