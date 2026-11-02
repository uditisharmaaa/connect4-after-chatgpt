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
    # Print column headers
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)) + '  '
    print(header)
    
    # Print top border
    border = '+' + ('---+' * COLS)
    print(border)
    
    # Print each row
    for row in board:
        row_str = '|' + '|'.join(f' {cell} ' for cell in row) + '|'
        print(row_str)
        print(border)

def get_valid_column(board):
    """Prompt the player for a column until a valid input is provided."""
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) != 1 or column < 'A' or column > chr(ord('A') + COLS - 1):
            print(f"Invalid column. Please choose from A to {chr(ord('A') + COLS - 1)}.")
            continue
        
        col_index = ord(column) - ord('A')
        if board[0][col_index] != ' ':
            print("Column is full. Choose another column.")
            continue
        
        return col_index

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return (row, col)
    return None

def check_win(board, row, col, player):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
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

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for cell in board[0])

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def main():
    global current_player
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        clear_screen()
        print_board(board)
        
        col = get_valid_column(board)
        row, _ = place_checker(board, col, current_player)
        
        if check_win(board, row, col, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
