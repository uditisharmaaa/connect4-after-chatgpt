import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player symbols
SYMBOLS = ["X", "O", "V", "H", "M"]

# Create empty board
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
    # Print column letters
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows with borders
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("| ", end="")
        for j in range(COLS):
            print(board[i][j] + " | ", end="")
        print()
    print("+---" * COLS + "+")

# Check if column is valid
def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    # Check if top row of column is empty
    if board[0][col] == " ":
        return True
    return False

# Place checker in column
def place_checker(board, col, symbol):
    # Find lowest empty row in column
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = symbol
            return i
    return -1

# Check for win
def check_win(board, symbol):
    # Check horizontal
    for i in range(ROWS):
        for j in range(COLS - 3):
            if board[i][j] == symbol and board[i][j+1] == symbol and board[i][j+2] == symbol and board[i][j+3] == symbol:
                return True
    
    # Check vertical
    for i in range(ROWS - 3):
        for j in range(COLS):
            if board[i][j] == symbol and board[i+1][j] == symbol and board[i+2][j] == symbol and board[i+3][j] == symbol:
                return True
    
    # Check diagonal (down-right)
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if board[i][j] == symbol and board[i+1][j+1] == symbol and board[i+2][j+2] == symbol and board[i+3][j+3] == symbol:
                return True
    
    # Check diagonal (down-left)
    for i in range(ROWS - 3):
        for j in range(3, COLS):
            if board[i][j] == symbol and board[i+1][j-1] == symbol and board[i+2][j-2] == symbol and board[i+3][j-3] == symbol:
                return True
    
    return False

# Check if board is full
def is_board_full(board):
    for j in range(COLS):
        if board[0][j] == " ":
            return False
    return True

# Main game
def play_game():
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(SYMBOLS[i])
    
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    os.system('clear')
    print_board(board)
    
    game_over = False
    
    while not game_over:
        symbol = players[current_player]
        print("Player " + symbol + ", please enter a column: ", end="")
        user_input = input()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please try again.")
            continue
        
        if not user_input.isupper():
            print("Invalid input. Please try again.")
            continue
        
        col_letter = user_input
        col_num = ord(col_letter) - 65
        
        if col_num < 0 or col_num >= COLS:
            print("Invalid column. Please try again.")
            continue
        
        if not is_valid_move(board, col_num):
            print("Column is full. You lose your turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        # Place checker
        place_checker(board, col_num, symbol)
        
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, symbol):
            print("Player " + symbol + " won!")
            game_over = True
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Next player's turn
            current_player = (current_player + 1) % NUM_PLAYERS

play_game()
