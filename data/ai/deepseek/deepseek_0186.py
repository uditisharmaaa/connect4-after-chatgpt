import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # Only use the necessary checkers

def create_board():
    """Create an empty game board initialized with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Print column headers
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)]) + '  '
    print(header)
    
    # Print the board rows with borders
    for row in board:
        border = '+' + ('---+' * COLS)
        empty_row = '|' + ('   |' * COLS)
        filled_row = '|' + ''.join([f' {cell} |' for cell in row])
        print(border)
        print(filled_row if any(cell != ' ' for cell in row) else empty_row)
    print('+' + ('---+' * COLS))

def is_valid_column(col):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    col = col.upper()
    return col >= 'A' and col <= chr(65 + COLS - 1)

def get_column_index(col):
    """Convert the column letter to a 0-based index."""
    return ord(col.upper()) - ord('A')

def drop_checker(board, col, checker):
    """Drop a checker into the specified column."""
    col_index = get_column_index(col)
    for row in reversed(range(ROWS)):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check if the specified player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    for row in board:
        if ' ' in row:
            return False
    return True

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
        while True:
            col = input(f"Player {current_player}, please enter a column: ")
            if is_valid_column(col):
                col_index = get_column_index(col)
                if board[0][col_index] == ' ':  # Column is not full
                    break
                else:
                    print("Column is full. Try another column.")
            else:
                print(f"Invalid input. Please enter a letter from A to {chr(65 + COLS - 1)}.")
        
        if not drop_checker(board, col, current_player):
            print("Column is full. You lose your turn.")
        
        clear_screen()
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to the next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
