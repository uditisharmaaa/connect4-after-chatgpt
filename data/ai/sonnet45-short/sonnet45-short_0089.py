import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Create empty board
board = []
for i in range(ROWS):
    row = []
    for j in range(COLS):
        row.append(' ')
    board.append(row)

def print_board():
    print("\n  A   B   C   D   E   F   G")
    for i in range(ROWS):
        print("|", end="")
        for j in range(COLS):
            print(" " + board[i][j] + " |", end="")
        print()
    print("-----------------------------")

def drop_piece(col, player):
    # Start from bottom row and go up
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == ' ':
            board[i][col] = player
            return True
    return False

def check_win(player):
    # Check horizontal
    for i in range(ROWS):
        for j in range(COLS - 3):
            if board[i][j] == player and board[i][j+1] == player and board[i][j+2] == player and board[i][j+3] == player:
                return True
    
    # Check vertical
    for i in range(ROWS - 3):
        for j in range(COLS):
            if board[i][j] == player and board[i+1][j] == player and board[i+2][j] == player and board[i+3][j] == player:
                return True
    
    # Check diagonal (down-right)
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if board[i][j] == player and board[i+1][j+1] == player and board[i+2][j+2] == player and board[i+3][j+3] == player:
                return True
    
    # Check diagonal (up-right)
    for i in range(3, ROWS):
        for j in range(COLS - 3):
            if board[i][j] == player and board[i-1][j+1] == player and board[i-2][j+2] == player and board[i-3][j+3] == player:
                return True
    
    return False

def check_draw():
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] == ' ':
                return False
    return True

# Main game
players = []
for i in range(NUM_PLAYERS):
    players.append(PLAYERS[i])

current_player_index = random.randint(0, NUM_PLAYERS - 1)

print("Welcome to Connect 4!")
print("Players:", players)

game_over = False

while not game_over:
    os.system('clear')
    print_board()
    
    current_player = players[current_player_index]
    print("\nPlayer " + current_player + "'s turn")
    
    valid_move = False
    while not valid_move:
        column = input("Enter column (A-G): ").upper()
        
        # Validate input
        if len(column) != 1:
            print("Invalid input! Enter a single letter A-G")
            continue
        
        if column not in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            print("Invalid column! Enter A-G")
            continue
        
        # Convert letter to number
        col_num = ord(column) - ord('A')
        
        # Try to drop piece
        if drop_piece(col_num, current_player):
            valid_move = True
        else:
            print("Column is full! Pick another column")
    
    # Check for win
    if check_win(current_player):
        os.system('clear')
        print_board()
        print("\nPlayer " + current_player + " wins!")
        game_over = True
    # Check for draw
    elif check_draw():
        os.system('clear')
        print_board()
        print("\nIt's a draw!")
        game_over = True
    else:
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

print("\nThanks for playing!")
