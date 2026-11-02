import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for up to 5 players

def create_board(rows, cols):
    """Create and initialize the game board with empty spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the game board with columns labeled A, B, C, etc."""
    # Print column headers
    header = '   ' + '   '.join([chr(ord('A') + i) for i in range(len(board[0]))])
    print(header)
    
    # Print each row
    border = '+' + ('---+' * len(board[0]))
    for row in board:
        print(border)
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
    print(border)

def is_valid_column(col, cols):
    """Check if the column input is valid (single uppercase letter within range)."""
    if len(col) != 1:
        return False
    col_char = col[0]
    return col_char.isupper() and ord(col_char) - ord('A') >= 0 and ord(col_char) - ord('A') < cols

def get_column_index(col):
    """Convert column letter to index (A -> 0, B -> 1, etc.)."""
    return ord(col) - ord('A')

def drop_checker(board, col_index, checker):
    """Drop a checker into the specified column and return the row where it landed."""
    for row in range(len(board)-1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    return -1  # Column is full

def check_win(board, row, col, checker):
    """Check if the given checker placement results in a win."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    
    for dr, dc in directions:
        count = 1
        # Search in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Search in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the game is a draw (all columns full)."""
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(ROWS, COLS)
    players = PLAYERS
    checkers = CHECKERS[:players]
    current_player = random.randint(0, players - 1)
    
    clear_screen()
    print_board(board)
    
    while True:
        checker = checkers[current_player]
        print(f"Player {checker}, please enter a column: ")
        col_input = input().strip().upper()
        
        if not is_valid_column(col_input, COLS):
            print("Invalid input! Please enter a column letter (A-G).")
            continue
        
        col_index = get_column_index(col_input)
        row = drop_checker(board, col_index, checker)
        
        if row == -1:
            print("Column is full! Please choose another column.")
            continue
        
        clear_screen()
        print_board(board)
        
        if check_win(board, row, col_index, checker):
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            print("Game is a draw!")
            break
        
        current_player = (current_player + 1) % players

if __name__ == "__main__":
    main()
