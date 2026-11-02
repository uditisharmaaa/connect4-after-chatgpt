import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current board state."""
    os.system('clear')
    # Print column headers
    print("  ", end="")
    for i in range(COLS):
        print(f" {chr(65 + i)}  ", end="")
    print()
    
    # Print rows
    for row in board:
        print("+" + "---+" * COLS)
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+" + "---+" * COLS)

def is_valid_column(col_letter, board):
    """Check if the column input is valid."""
    if len(col_letter) != 1 or not col_letter.isalpha() or not col_letter.isupper():
        return False
    col_index = ord(col_letter) - 65
    if col_index < 0 or col_index >= COLS:
        return False
    return board[0][col_index] == " "

def drop_checker(board, col_letter, checker):
    """Drop a checker into the specified column."""
    col_index = ord(col_letter) - 65
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the specified checker has won."""
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is full."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    """Main game loop."""
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_index]
        print(f"Player {current_checker}, please enter a column: ", end="")
        col_input = input().strip()
        
        if not is_valid_column(col_input, board):
            print("Invalid input. Try again.")
            continue
        
        drop_checker(board, col_input, current_checker)
        print_board(board)
        
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if is_board_full(board):
            print("It's a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
