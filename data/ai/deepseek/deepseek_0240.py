import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board():
    """Create and initialize the game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    os.system('clear')
    # Print column headers
    print(' '.join([f'  {chr(65 + i)} ' for i in range(COLS)]))
    # Print each row with borders
    for row in board:
        print('+---+' * COLS)
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
    print('+---+' * COLS)

def get_valid_column(board):
    """Prompt the current player for a valid column input."""
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not col.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        col_idx = ord(col) - ord('A')
        if col_idx < 0 or col_idx >= COLS:
            print(f"Column out of range. Please enter a letter between A-{chr(65 + COLS - 1)}.")
            continue
        if board[0][col_idx] != ' ':
            print("Column is full. Please choose another column.")
            continue
        return col_idx

def place_checker(board, col, player):
    """Place the player's checker in the lowest available row of the column."""
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the current move resulted in a win."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    """Check if the game is a draw (all cells filled)."""
    return all(cell != ' ' for row in board for cell in row)

# Initialize game
board = create_board()
current_player = random.choice(PLAYERS)
game_over = False

# Main game loop
while not game_over:
    print_board(board)
    col = get_valid_column(board)
    row = place_checker(board, col, current_player)
    
    if check_win(board, row, col, current_player):
        print_board(board)
        print(f"Player {current_player} won!")
        game_over = True
    elif check_draw(board):
        print_board(board)
        print("Game ended in a draw!")
        game_over = True
    else:
        # Switch to the next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]
