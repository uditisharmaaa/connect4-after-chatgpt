import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize an empty game board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column labels
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print board rows
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    
    print('+---' * COLS + '+')

def get_valid_column():
    """Prompt the player for a column input and validate it."""
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not col.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        col_num = ord(col) - ord('A')
        if col_num < 0 or col_num >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        if board[0][col_num] != ' ':
            print("Column is full. Please choose another column.")
            continue
        return col_num

def place_checker(board, col, checker):
    """Place the checker in the lowest available row of the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1  # Column is full (shouldn't happen since input is validated)

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    # Check horizontal
    count = 1
    left = col - 1
    while left >= 0 and board[row][left] == checker:
        count += 1
        left -= 1
    right = col + 1
    while right < COLS and board[row][right] == checker:
        count += 1
        right += 1
    if count >= 4:
        return True

    # Check vertical
    count = 1
    up = row - 1
    while up >= 0 and board[up][col] == checker:
        count += 1
        up -= 1
    down = row + 1
    while down < ROWS and board[down][col] == checker:
        count += 1
        down += 1
    if count >= 4:
        return True

    # Check diagonal (top-left to bottom-right)
    count = 1
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= 4:
        return True

    # Check diagonal (top-right to bottom-left)
    count = 1
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= 4:
        return True

    return False

def check_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != ' ' for cell in board[0])

def play_game():
    """Run the main game loop."""
    global current_player
    board = initialize_board()
    print_board(board)
    
    while True:
        col = get_valid_column()
        row = place_checker(board, col, CHECKERS[current_player])
        print_board(board)
        
        if check_win(board, row, col, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if check_draw(board):
            print("Game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

# Main game setup
current_player = random.randint(0, PLAYERS - 1)
play_game()
