import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def initialize_board():
    """Initialize an empty board with ROWS x COLS dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    
    # Print the board rows
    border = "+" + ("---+" * COLS)
    print(border)
    for row in board:
        print("| " + " | ".join(cell for cell in row) + " |")
        print(border)

def get_valid_column(board):
    """Prompt the current player for a column and validate the input."""
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) != 1 or column < 'A' or column > chr(65 + COLS - 1):
            print(f"Invalid column. Please enter a letter from A to {chr(65 + COLS - 1)}.")
            continue
        col_idx = ord(column) - ord('A')
        if board[0][col_idx] != " ":
            print("Column is full. Please choose another column.")
            continue
        return col_idx

def place_checker(board, col_idx, checker):
    """Place the checker in the lowest available row of the specified column."""
    for row_idx in reversed(range(ROWS)):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return (row_idx, col_idx)
    return None

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(cell != " " for cell in board[0])

def main():
    global current_player
    board = initialize_board()
    current_player = random.choice(CHECKERS)
    print_board(board)
    
    while True:
        col_idx = get_valid_column(board)
        pos = place_checker(board, col_idx, current_player)
        print_board(board)
        
        if check_win(board, pos[0], pos[1], current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
