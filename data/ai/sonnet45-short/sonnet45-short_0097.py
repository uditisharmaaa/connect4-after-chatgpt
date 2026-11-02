import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 3, 4, or 5 for more players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Create empty board
board = []
for i in range(ROWS):
    row = []
    for j in range(COLS):
        row.append(' ')
    board.append(row)

# Get the players for this game
players = []
for i in range(NUM_PLAYERS):
    players.append(PLAYER_SYMBOLS[i])

# Pick random first player
current_player_index = random.randint(0, NUM_PLAYERS - 1)

def print_board():
    print("\n  A B C D E F G")
    for i in range(ROWS):
        print(i + 1, end=' ')
        for j in range(COLS):
            print(board[i][j], end='|')
        print()
    print()

def drop_piece(col, symbol):
    # Start from bottom row and go up
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == ' ':
            board[i][col] = symbol
            return True
    return False

def check_win(symbol):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and 
                board[row][col + 1] == symbol and 
                board[row][col + 2] == symbol and 
                board[row][col + 3] == symbol):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == symbol and 
                board[row + 1][col] == symbol and 
                board[row + 2][col] == symbol and 
                board[row + 3][col] == symbol):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and 
                board[row + 1][col + 1] == symbol and 
                board[row + 2][col + 2] == symbol and 
                board[row + 3][col + 3] == symbol):
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == symbol and 
                board[row + 1][col - 1] == symbol and 
                board[row + 2][col - 2] == symbol and 
                board[row + 3][col - 3] == symbol):
                return True
    
    return False

def check_draw():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                return False
    return True

# Main game loop
game_over = False

while not game_over:
    os.system('clear')
    print_board()
    
    current_player = players[current_player_index]
    print("Player " + current_player + "'s turn")
    
    valid_move = False
    while not valid_move:
        move = input("Enter column (A-G): ").upper()
        
        # Validate input
        if len(move) != 1:
            print("Invalid input! Enter a single letter A-G")
            continue
        
        if move < 'A' or move > 'G':
            print("Invalid column! Enter A-G")
            continue
        
        col_index = ord(move) - ord('A')
        
        # Check if column is full
        if board[0][col_index] != ' ':
            print("Column is full! Pick another column")
            continue
        
        valid_move = True
    
    # Drop the piece
    drop_piece(col_index, current_player)
    
    # Check for win
    if check_win(current_player):
        os.system('clear')
        print_board()
        print("Player " + current_player + " wins!")
        game_over = True
    # Check for draw
    elif check_draw():
        os.system('clear')
        print_board()
        print("It's a draw!")
        game_over = True
    else:
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
