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
    os.system('clear')
    # Print column letters
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
    print("+---" * COLS + "+")

# Check if column is valid
def is_valid_column(board, col):
    if col < 0 or col >= COLS:
        return False
    if board[0][col] != " ":
        return False
    return True

# Place checker in column
def place_checker(board, col, symbol):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row
    return -1

# Check for win horizontally
def check_horizontal(board, symbol):
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == symbol and board[row][col+1] == symbol and board[row][col+2] == symbol and board[row][col+3] == symbol:
                return True
    return False

# Check for win vertically
def check_vertical(board, symbol):
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == symbol and board[row+1][col] == symbol and board[row+2][col] == symbol and board[row+3][col] == symbol:
                return True
    return False

# Check for win diagonally (bottom-left to top-right)
def check_diagonal1(board, symbol):
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == symbol and board[row-1][col+1] == symbol and board[row-2][col+2] == symbol and board[row-3][col+3] == symbol:
                return True
    return False

# Check for win diagonally (top-left to bottom-right)
def check_diagonal2(board, symbol):
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == symbol and board[row+1][col+1] == symbol and board[row+2][col+2] == symbol and board[row+3][col+3] == symbol:
                return True
    return False

# Check if player won
def check_win(board, symbol):
    if check_horizontal(board, symbol):
        return True
    if check_vertical(board, symbol):
        return True
    if check_diagonal1(board, symbol):
        return True
    if check_diagonal2(board, symbol):
        return True
    return False

# Check if board is full
def is_board_full(board):
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

# Main game
def play_game():
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(SYMBOLS[i])
    
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    while not game_over:
        player_symbol = players[current_player]
        print("Player " + player_symbol + ", please enter a column: ", end="")
        user_input = input()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Try again.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Try again.")
            continue
        
        col_letter = user_input.upper()
        col_index = ord(col_letter) - 65
        
        if col_index < 0 or col_index >= COLS:
            print("Invalid column. Try again.")
            continue
        
        if not is_valid_column(board, col_index):
            print("Column is full. Try again.")
            continue
        
        # Place checker
        place_checker(board, col_index, player_symbol)
        print_board(board)
        
        # Check for win
        if check_win(board, player_symbol):
            print("Player " + player_symbol + " won!")
            game_over = True
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Next player
            current_player = (current_player + 1) % NUM_PLAYERS

play_game()
