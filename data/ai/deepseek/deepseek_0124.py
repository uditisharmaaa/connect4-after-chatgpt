import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Create and return a blank board."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(BOARD_COLS)]
    print('  ' + '   '.join(headers))
    
    # Print board rows
    border = '+' + ('---+' * BOARD_COLS)
    print(border)
    for row in board:
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        print(border)

def get_valid_column(board):
    """Prompt the player for a valid column input."""
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not col.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        col_idx = ord(col) - ord('A')
        if col_idx < 0 or col_idx >= BOARD_COLS:
            print(f"Column must be between A and {chr(ord('A') + BOARD_COLS - 1)}.")
            continue
        if board[0][col_idx] != ' ':
            print("Column is full. Choose another column.")
            continue
        return col_idx

def place_checker(board, col_idx, symbol):
    """Place the checker in the lowest available row of the column."""
    for row_idx in range(BOARD_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = symbol
            return row_idx, col_idx
    return -1, -1  # Shouldn't happen if column is validated

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Search in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Search in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for cell in board[0])

def clear_screen():
    """Clear the console screen."""
    os.system('clear')

def main():
    global current_player
    board = initialize_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    clear_screen()
    print_board(board)
    
    while True:
        col_idx = get_valid_column(board)
        row_idx, _ = place_checker(board, col_idx, current_player)
        clear_screen()
        print_board(board)
        
        if check_win(board, row_idx, col_idx, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
