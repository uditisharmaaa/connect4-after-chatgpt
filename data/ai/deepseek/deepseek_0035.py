import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board():
    """Initialize the board with empty cells."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels and borders."""
    # Print column headers
    header = '  ' + '   '.join(chr(65 + i) for i in range(COLS)) + '  '
    print(header)
    
    # Print top border
    top_border = '+' + ('---+' * COLS)
    print(top_border)
    
    # Print each row
    for row in board:
        row_str = '|' + '|'.join(f' {cell} ' for cell in row) + '|'
        print(row_str)
        print(top_border)

def is_valid_column(col):
    """Check if column input is valid."""
    if len(col) != 1 or not col.isalpha():
        return False
    col_num = ord(col.upper()) - 65
    return 0 <= col_num < COLS

def get_drop_position(board, col):
    """Get the lowest empty row in the specified column."""
    col_num = ord(col.upper()) - 65
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_num] == ' ':
            return row, col_num
    return -1, -1  # Column is full

def place_checker(board, row, col, player):
    """Place the player's checker in the specified position."""
    board[row][col] = player

def check_win(board, row, col, player):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # The current cell
        
        # Search in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        
        # Search in negative direction
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
    return all(cell != ' ' for row in board for cell in row)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player = random.choice(PLAYERS)
    clear_screen()
    print_board(board)
    
    while True:
        # Get player input
        col = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        # Validate input
        if not is_valid_column(col):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        row, col_num = get_drop_position(board, col)
        if row == -1:
            print("Column is full. Please choose another column.")
            continue
        
        # Place checker and check win/draw
        place_checker(board, row, col_num, current_player)
        clear_screen()
        print_board(board)
        
        if check_win(board, row, col_num, current_player):
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
