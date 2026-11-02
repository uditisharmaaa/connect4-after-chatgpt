import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def initialize_board():
    """Initialize the board with empty spaces."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the board with columns labeled A, B, C, etc."""
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(BOARD_COLS)]
    print('  ' + '   '.join(headers))
    
    # Print each row with borders
    for row in board:
        print('+---+' * BOARD_COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    # Print bottom border
    print('+---+' * BOARD_COLS)

def is_valid_column(column):
    """Check if the column input is valid (uppercase letter within range)."""
    if len(column) != 1:
        return False
    col_char = column.upper()
    return 'A' <= col_char <= chr(ord('A') + BOARD_COLS - 1)

def get_column_index(column):
    """Convert column letter to index (e.g., 'A' -> 0)."""
    return ord(column.upper()) - ord('A')

def drop_checker(board, column, checker):
    """Drop a checker into the specified column and return the row where it lands."""
    col_index = get_column_index(column)
    for row_index in range(BOARD_ROWS - 1, -1, -1):
        if board[row_index][col_index] == ' ':
            board[row_index][col_index] = checker
            return row_index
    return -1  # Column is full

def check_win(board, row, col):
    """Check if the current move caused a win."""
    checker = board[row][col]
    
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # Include the current checker
        
        # Check in one direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    players = PLAYERS[:NUM_PLAYERS]
    
    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {players[current_player]}, please enter a column: ", end='')
        column = input().strip()
        
        if not is_valid_column(column):
            print("Invalid input. Please enter a valid column (A-G).")
            input("Press Enter to continue...")
            continue
        
        col_index = get_column_index(column)
        if board[0][col_index] != ' ':  # Column is full
            print("Column is full. Try another column.")
            input("Press Enter to continue...")
            continue
        
        row = drop_checker(board, column, players[current_player])
        if check_win(board, row, col_index):
            os.system('clear')
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break
        
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
