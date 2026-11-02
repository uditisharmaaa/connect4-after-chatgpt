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

# Game variables
current_player = 0
game_over = False
players = []
for i in range(NUM_PLAYERS):
    players.append(PLAYER_SYMBOLS[i])

# Pick random first player
current_player = random.randint(0, NUM_PLAYERS - 1)

def print_board():
    os.system('clear')
    print("  A B C D E F G")
    for i in range(ROWS):
        print(str(i + 1) + " ", end="")
        for j in range(COLS):
            print(board[i][j] + " ", end="")
        print()
    print()

def is_valid_move(col):
    if col < 0 or col >= COLS:
        return False
    if board[0][col] != ' ':
        return False
    return True

def drop_piece(col, symbol):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == ' ':
            board[i][col] = symbol
            return i
    return -1

def check_win(row, col, symbol):
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == symbol:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == symbol:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (down-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r = start_row
    c = start_col
    while r < ROWS and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (down-left)
    count = 0
    start_row = row - min(row, COLS - 1 - col)
    start_col = col + min(row, COLS - 1 - col)
    r = start_row
    c = start_col
    while r < ROWS and c >= 0:
        if board[r][c] == symbol:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c -= 1
    
    return False

def check_draw():
    for i in range(COLS):
        if board[0][i] == ' ':
            return False
    return True

# Game loop
print("Connect 4!")
print("Players: " + str(players))
print()

while not game_over:
    print_board()
    print("Player " + players[current_player] + "'s turn")
    
    # Get input
    move = input("Enter column (A-G): ").upper()
    
    # Validate input
    if len(move) != 1:
        print("Invalid input! Press Enter to continue...")
        input()
        continue
    
    if move < 'A' or move > 'G':
        print("Invalid column! Press Enter to continue...")
        input()
        continue
    
    col = ord(move) - ord('A')
    
    if not is_valid_move(col):
        print("Column is full! Press Enter to continue...")
        input()
        continue
    
    # Drop piece
    row = drop_piece(col, players[current_player])
    
    # Check for win
    if check_win(row, col, players[current_player]):
        print_board()
        print("Player " + players[current_player] + " wins!")
        game_over = True
    elif check_draw():
        print_board()
        print("It's a draw!")
        game_over = True
    else:
        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS
