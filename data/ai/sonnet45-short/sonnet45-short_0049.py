import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Create empty board
board = []
for r in range(ROWS):
    row = []
    for c in range(COLS):
        row.append(' ')
    board.append(row)

# Get players for this game
players = []
for i in range(NUM_PLAYERS):
    players.append(PLAYER_SYMBOLS[i])

# Pick random first player
current_player_index = random.randint(0, NUM_PLAYERS - 1)

def print_board():
    print("\n  A B C D E F G")
    for r in range(ROWS):
        print(r + 1, end=' ')
        for c in range(COLS):
            print(board[r][c], end=' ')
        print()
    print()

def drop_piece(col, symbol):
    # Start from bottom row and go up
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return r
    return -1

def check_win(symbol):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == symbol and board[r][c+1] == symbol and board[r][c+2] == symbol and board[r][c+3] == symbol:
                return True
    
    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if board[r][c] == symbol and board[r+1][c] == symbol and board[r+2][c] == symbol and board[r+3][c] == symbol:
                return True
    
    # Check diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == symbol and board[r+1][c+1] == symbol and board[r+2][c+2] == symbol and board[r+3][c+3] == symbol:
                return True
    
    # Check diagonal (down-left)
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if board[r][c] == symbol and board[r+1][c-1] == symbol and board[r+2][c-2] == symbol and board[r+3][c-3] == symbol:
                return True
    
    return False

def check_draw():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == ' ':
                return False
    return True

# Main game loop
game_over = False
while not game_over:
    os.system('clear')
    print_board()
    
    current_player = players[current_player_index]
    print(f"Player {current_player}'s turn")
    
    # Get input
    valid_move = False
    while not valid_move:
        col_input = input("Enter column (A-G): ").upper()
        
        # Validate input
        if len(col_input) != 1:
            print("Invalid input! Enter a single letter A-G")
            continue
        
        if col_input < 'A' or col_input > 'G':
            print("Invalid column! Enter A-G")
            continue
        
        col = ord(col_input) - ord('A')
        
        # Check if column is full
        if board[0][col] != ' ':
            print("Column is full! Pick another column")
            continue
        
        valid_move = True
    
    # Drop the piece
    drop_piece(col, current_player)
    
    # Check for win
    if check_win(current_player):
        os.system('clear')
        print_board()
        print(f"Player {current_player} wins!")
        game_over = True
    elif check_draw():
        os.system('clear')
        print_board()
        print("It's a draw!")
        game_over = True
    else:
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
