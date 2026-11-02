import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 3, 4, or 5 for more players
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Create empty board
board = []
for i in range(ROWS):
    row = []
    for j in range(COLS):
        row.append(' ')
    board.append(row)

# Print the board
def print_board():
    os.system('clear')
    print("  A B C D E F G")
    for i in range(ROWS):
        print(i + 1, end=' ')
        for j in range(COLS):
            print(board[i][j], end=' ')
        print()
    print()

# Drop piece in column
def drop_piece(col, player):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == ' ':
            board[i][col] = player
            return True
    return False

# Check if column is valid and not full
def is_valid_move(col):
    if col < 0 or col >= COLS:
        return False
    if board[0][col] != ' ':
        return False
    return True

# Check for win
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
    
    # Check diagonal (down-left)
    for i in range(ROWS - 3):
        for j in range(3, COLS):
            if board[i][j] == player and board[i+1][j-1] == player and board[i+2][j-2] == player and board[i+3][j-3] == player:
                return True
    
    return False

# Check if board is full (draw)
def is_board_full():
    for j in range(COLS):
        if board[0][j] == ' ':
            return False
    return True

# Main game loop
players = PLAYERS[:NUM_PLAYERS]
current_player_index = random.randint(0, NUM_PLAYERS - 1)

print("Welcome to Connect 4!")
print("Players:", ', '.join(players))
print()

game_over = False
while not game_over:
    current_player = players[current_player_index]
    print_board()
    print("Player " + current_player + "'s turn")
    
    # Get input
    valid_input = False
    while not valid_input:
        move = input("Enter column (A-G): ").upper()
        
        if len(move) != 1:
            print("Invalid input! Enter a single letter A-G")
            continue
        
        if move < 'A' or move > 'G':
            print("Invalid input! Enter a letter from A to G")
            continue
        
        col = ord(move) - ord('A')
        
        if not is_valid_move(col):
            print("Column is full or invalid! Choose another column")
            continue
        
        valid_input = True
    
    # Drop piece
    drop_piece(col, current_player)
    
    # Check for win
    if check_win(current_player):
        print_board()
        print("Player " + current_player + " wins!")
        game_over = True
    elif is_board_full():
        print_board()
        print("It's a draw!")
        game_over = True
    else:
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

print("Game Over!")
