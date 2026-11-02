import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Create the board
def create_board():
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

# Print the board
def print_board(board):
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for j in range(COLS):
            print(" " + board[i][j] + " |", end="")
        print()
    print("+---" * COLS + "+")

# Check if column is valid
def is_valid_column(col, board):
    if col < 0 or col >= COLS:
        return False
    # Check if column is full
    if board[0][col] != " ":
        return False
    return True

# Place checker in column
def place_checker(col, checker, board):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = checker
            return i
    return -1

# Check for win horizontally
def check_horizontal(board, checker):
    for i in range(ROWS):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i][j+1] == checker and board[i][j+2] == checker and board[i][j+3] == checker:
                return True
    return False

# Check for win vertically
def check_vertical(board, checker):
    for i in range(ROWS - 3):
        for j in range(COLS):
            if board[i][j] == checker and board[i+1][j] == checker and board[i+2][j] == checker and board[i+3][j] == checker:
                return True
    return False

# Check for win diagonally (positive slope)
def check_diagonal_positive(board, checker):
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i+1][j+1] == checker and board[i+2][j+2] == checker and board[i+3][j+3] == checker:
                return True
    return False

# Check for win diagonally (negative slope)
def check_diagonal_negative(board, checker):
    for i in range(3, ROWS):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i-1][j+1] == checker and board[i-2][j+2] == checker and board[i-3][j+3] == checker:
                return True
    return False

# Check if player won
def check_win(board, checker):
    if check_horizontal(board, checker):
        return True
    if check_vertical(board, checker):
        return True
    if check_diagonal_positive(board, checker):
        return True
    if check_diagonal_negative(board, checker):
        return True
    return False

# Check if board is full (draw)
def check_draw(board):
    for j in range(COLS):
        if board[0][j] == " ":
            return False
    return True

# Main game
def play_game():
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    while not game_over:
        current_checker = players[current_player_index]
        
        # Get player input
        valid_input = False
        while not valid_input:
            user_input = input("Player " + current_checker + ", please enter a column: ")
            
            # Check if input is valid
            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter.")
                continue
            
            if not user_input.isalpha():
                print("Invalid input. Please enter a letter.")
                continue
            
            user_input = user_input.upper()
            col = ord(user_input) - 65
            
            if col < 0 or col >= COLS:
                print("Invalid column. Please enter a letter between A and " + chr(65 + COLS - 1) + ".")
                continue
            
            if not is_valid_column(col, board):
                print("Column is full. Please choose another column.")
                continue
            
            valid_input = True
        
        # Place checker
        place_checker(col, current_checker, board)
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print("Player " + current_checker + " won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Start the game
play_game()
