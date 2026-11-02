import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels and borders."""
    # Clear the screen
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column labels
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print the board
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---+' * COLS)

def get_valid_column():
    """Prompt the player to enter a column and validate the input."""
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) != 1 or not column.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        col_index = ord(column) - ord('A')
        if col_index < 0 or col_index >= COLS:
            print(f"Column out of range. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        return col_index

def place_checker(board, col, player):
    """Place the player's checker in the lowest available row of the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col
    return None

def check_win(board, row, col, player):
    """Check if the player has won by placing a checker at (row, col)."""
    # Directions: (row, col) offsets for 4 directions (horizontal, vertical, 2 diagonals)
    directions = [
        (0, 1),  # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal /
        (1, -1)   # diagonal \
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """Check if all spaces on the board are occupied."""
    return all(cell != ' ' for row in board for cell in row)

# Main game loop
def play_game():
    global current_player
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        col = get_valid_column()
        result = place_checker(board, col, current_player)
        if result is None:
            print("Column is full. Try another column.")
            continue
        
        row, _ = result
        print_board(board)
        
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_board_full(board):
            print("Game over. It's a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == '__main__':
    play_game()
