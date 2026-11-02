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

# Setup players
players = []
for i in range(NUM_PLAYERS):
    players.append(PLAYER_SYMBOLS[i])

def print_board():
    print("\n  A B C D E F G")
    for i in range(ROWS):
        print(i + 1, end=' ')
        for j in range(COLS):
            print(board[i][j], end=' ')
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

def check_draw():
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] == ' ':
                return False
    return True

# Main game loop
current_player_index = random.randint(0, NUM_PLAYERS - 1)
game_over = False

print("Welcome to Connect 4!")
print(f"Players: {', '.join(players)}")
print(f"First player: {players[current_player_index]}")
input("Press Enter to start...")

while not game_over:
    os.system('clear')
    print_board()
    
    current_symbol = players[current_player_index]
    print(f"Player {current_symbol}'s turn")
    
    # Get input
    valid_move = False
    while not valid_move:
        col_input = input("Enter column (A-G): ").upper()
        
        # Validate input
        if len(col_input) != 1:
            print("Please enter a single letter!")
            continue
        
        if col_input not in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            print("Please enter a letter between A and G!")
            continue
        
        # Convert letter to column number
        col = ord(col_input) - ord('A')
        
        # Check if column is full
        if board[0][col] != ' ':
            print("That column is full! Choose another.")
            continue
        
        # Drop piece
        drop_piece(col, current_symbol)
        valid_move = True
    
    # Check for win
    if check_win(current_symbol):
        os.system('clear')
        print_board()
        print(f"Player {current_symbol} wins!")
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

print("Game over! Thanks for playing!")
