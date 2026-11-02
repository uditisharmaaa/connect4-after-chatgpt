import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Create empty board
board = []
for i in range(ROWS):
    row = []
    for j in range(COLS):
        row.append(' ')
    board.append(row)

# Get players for this game
players = []
for i in range(NUM_PLAYERS):
    players.append(PLAYER_SYMBOLS[i])

# Pick random first player
current_player_index = random.randint(0, NUM_PLAYERS - 1)

# Function to print the board
def print_board():
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
        print("-----------------------------")

# Function to drop a piece in a column
def drop_piece(col, symbol):
    # Start from bottom row and go up
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return True
    return False

# Function to check if column is valid and not full
def is_valid_move(col_letter):
    # Check if input is a single letter
    if len(col_letter) != 1:
        return False
    
    # Convert to uppercase
    col_letter = col_letter.upper()
    
    # Check if it's A-G
    if col_letter < 'A' or col_letter > 'G':
        return False
    
    # Convert letter to column number
    col = ord(col_letter) - ord('A')
    
    # Check if column is full
    if board[0][col] != ' ':
        return False
    
    return True

# Function to check for a win
def check_win(symbol):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == symbol and board[row][col+1] == symbol and board[row][col+2] == symbol and board[row][col+3] == symbol:
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == symbol and board[row+1][col] == symbol and board[row+2][col] == symbol and board[row+3][col] == symbol:
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == symbol and board[row+1][col+1] == symbol and board[row+2][col+2] == symbol and board[row+3][col+3] == symbol:
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if board[row][col] == symbol and board[row+1][col-1] == symbol and board[row+2][col-2] == symbol and board[row+3][col-3] == symbol:
                return True
    
    return False

# Function to check if board is full (draw)
def is_board_full():
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

# Main game loop
game_over = False
while not game_over:
    print_board()
    
    current_player = players[current_player_index]
    print("Player " + current_player + "'s turn")
    
    # Get valid input
    valid_input = False
    while not valid_input:
        col_letter = input("Choose a column (A-G): ")
        if is_valid_move(col_letter):
            valid_input = True
        else:
            print("Invalid move! Try again.")
    
    # Convert letter to column number
    col_letter = col_letter.upper()
    col = ord(col_letter) - ord('A')
    
    # Drop the piece
    drop_piece(col, current_player)
    
    # Check for win
    if check_win(current_player):
        print_board()
        print("Player " + current_player + " wins!")
        game_over = True
    # Check for draw
    elif is_board_full():
        print_board()
        print("It's a draw!")
        game_over = True
    else:
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

print("Game over!")
