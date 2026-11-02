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
    """Print the game board"""
    print("\n  A   B   C   D   E   F   G")
    for i in range(ROWS):
        print(i, end=' ')
        for j in range(COLS):
            print(board[i][j], end=' | ')
        print()
        if i < ROWS - 1:
            print("  " + "---+" * 6 + "---")
    print()

def drop_piece(col, player):
    """Drop a piece in the given column"""
    # Start from bottom row and go up
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == ' ':
            board[i][col] = player
            return i
    return -1

def check_win(player):
    """Check if player has won"""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row][col + 1] == player and 
                board[row][col + 2] == player and 
                board[row][col + 3] == player):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player and 
                board[row + 1][col] == player and 
                board[row + 2][col] == player and 
                board[row + 3][col] == player):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row + 1][col + 1] == player and 
                board[row + 2][col + 2] == player and 
                board[row + 3][col + 3] == player):
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == player and 
                board[row + 1][col - 1] == player and 
                board[row + 2][col - 2] == player and 
                board[row + 3][col - 3] == player):
                return True
    
    return False

def check_draw():
    """Check if the board is full (draw)"""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                return False
    return True

def get_column():
    """Get valid column input from player"""
    while True:
        col_input = input("Enter column (A-G): ").upper()
        
        if len(col_input) != 1:
            print("Invalid input! Enter a single letter.")
            continue
        
        if col_input < 'A' or col_input > 'G':
            print("Invalid column! Choose A-G.")
            continue
        
        col = ord(col_input) - ord('A')
        
        if board[0][col] != ' ':
            print("Column is full! Choose another.")
            continue
        
        return col

# Main game
players = []
for i in range(NUM_PLAYERS):
    players.append(PLAYERS[i])

current_player_index = random.randint(0, NUM_PLAYERS - 1)

print("Welcome to Connect 4!")
print(f"Players: {', '.join(players)}")
print(f"Player {players[current_player_index]} goes first!")
input("Press Enter to start...")

game_over = False

while not game_over:
    os.system('clear')
    print_board()
    
    current_player = players[current_player_index]
    print(f"Player {current_player}'s turn")
    
    col = get_column()
    drop_piece(col, current_player)
    
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
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

print("Game over!")
