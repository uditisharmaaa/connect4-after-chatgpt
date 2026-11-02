import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Create and return an empty board with specified dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the board with column labels and borders."""
    os.system('clear')
    # Print column headers
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(BOARD_COLS)])
    print(header)
    
    # Print each row with borders
    border = '+' + ('---+' * BOARD_COLS)
    print(border)
    for row in board:
        line = '|' + '|'.join([f' {cell} ' for cell in row]) + '|'
        print(line)
        print(border)

def get_valid_column(board):
    """Prompt player for a column input until a valid one is given."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        col = ord(col_input) - ord('A')
        if col < 0 or col >= BOARD_COLS:
            print(f"Column must be between A and {chr(ord('A') + BOARD_COLS - 1)}.")
            continue
        if board[0][col] != ' ':
            print("Column is full. Please choose another column.")
            continue
        return col

def drop_checker(board, col, player):
    """Place the player's checker in the lowest available row of the column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the latest move results in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(cell != ' ' for cell in board[0])

def play_game():
    """Main game loop."""
    global current_player
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        col = get_valid_column(board)
        row = drop_checker(board, col, current_player)
        print_board(board)
        
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    current_player = None
    play_game()
