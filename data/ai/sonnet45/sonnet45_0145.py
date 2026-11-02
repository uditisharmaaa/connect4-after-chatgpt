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
    """Create an empty board with ROWS x COLS dimensions"""
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        label = chr(ord('A') + col)
        print(label + "   ", end="")
    print()
    
    # Print rows with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(board, col):
    """Check if a column is valid and not full"""
    if col < 0 or col >= COLS:
        return False
    # Check if top row of column is empty
    if board[0][col] != " ":
        return False
    return True

def get_next_row(board, col):
    """Find the next available row in a column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

def place_checker(board, col, checker):
    """Place a checker in the specified column"""
    row = get_next_row(board, col)
    if row != -1:
        board[row][col] = checker
        return True
    return False

def check_win(board, checker):
    """Check if the current player has won"""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for k in range(WIN_LENGTH):
                if board[row][col + k] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            count = 0
            for k in range(WIN_LENGTH):
                if board[row + k][col] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for k in range(WIN_LENGTH):
                if board[row + k][col + k] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            count = 0
            for k in range(WIN_LENGTH):
                if board[row + k][col - k] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw)"""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_input(board, player_checker):
    """Get valid input from player"""
    while True:
        user_input = input("Player " + player_checker + ", please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert to uppercase and get column number
        user_input = user_input.upper()
        col = ord(user_input) - ord('A')
        
        # Check if column is valid
        if col < 0 or col >= COLS:
            print("Invalid column. Please choose a column between A and " + chr(ord('A') + COLS - 1) + ".")
            continue
        
        # Check if column is full
        if not is_valid_column(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col

def main():
    """Main game function"""
    # Create board
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
        
        # Get player input
        col = get_player_input(board, player_checker)
        
        # Place checker
        place_checker(board, col, player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, player_checker):
            print("Player " + player_checker + " won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Next player's turn
            current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
main()
