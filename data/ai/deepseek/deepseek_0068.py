import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
WIN_LENGTH = 4

def initialize_board():
    """Initialize an empty board with given dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def print_board(board):
    """Print the current state of the board."""
    # Print column headers (A, B, C, ...)
    print('  ' + '   '.join([chr(65 + i) for i in range(BOARD_COLS)]))
    
    # Print the board rows with borders
    border = '+' + ('---+' * BOARD_COLS)
    print(border)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print(border)

def is_valid_column(column):
    """Check if the column input is valid."""
    if len(column) != 1:
        return False
    col_char = column.upper()
    return col_char >= 'A' and col_char <= chr(65 + BOARD_COLS - 1)

def get_column_index(column):
    """Convert column letter to index (A -> 0, B -> 1, etc.)."""
    return ord(column.upper()) - 65

def drop_checker(board, column, player_symbol):
    """Place the player's checker in the specified column."""
    col_idx = get_column_index(column)
    for row_idx in range(BOARD_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = player_symbol
            return (row_idx, col_idx)
    return None  # Column is full

def check_win(board, row, col):
    """Check if the last move resulted in a win."""
    symbol = board[row][col]
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)  # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    
    clear_screen()
    print_board(board)
    
    while not game_over:
        player_symbol = PLAYER_SYMBOLS[current_player]
        print(f"Player {player_symbol}, please enter a column: ", end='')
        column = input().strip()
        
        if not is_valid_column(column):
            print("Invalid input. Please enter a valid column (A-G).")
            continue
        
        col_idx = get_column_index(column)
        if board[0][col_idx] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        position = drop_checker(board, column, player_symbol)
        clear_screen()
        print_board(board)
        
        if check_win(board, position[0], position[1]):
            print(f"Player {player_symbol} won!")
            game_over = True
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
