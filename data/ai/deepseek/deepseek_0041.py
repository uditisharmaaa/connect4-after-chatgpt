import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    
    # Print each row with borders
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(cell for cell in row) + " |")
    
    # Print bottom border
    print("+---" * COLS + "+")

def is_valid_column(col, board):
    """Check if the column is valid and has space."""
    if not col or len(col) != 1:
        return False
    
    col_idx = ord(col.upper()) - ord('A')
    if col_idx < 0 or col_idx >= COLS:
        return False
    
    # Check if column has space
    return board[0][col_idx] == " "

def drop_checker(board, col, symbol):
    """Drop the checker in the specified column and return the row where it lands."""
    col_idx = ord(col.upper()) - ord('A')
    
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = symbol
            return row
    
    return -1  # Shouldn't happen if column is validated first

def check_win(board, row, col, symbol):
    """Check if the last move caused a win."""
    # Directions: (row, col) offsets for 4 directions (horizontal, vertical, 2 diagonals)
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)  # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # The current cell is already the symbol
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main game loop."""
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    symbols = PLAYER_SYMBOLS[:PLAYERS]
    
    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {symbols[current_player]}, please enter a column: ")
        
        col = input().strip().upper()
        if not is_valid_column(col, board):
            print("Invalid input. Please enter a valid column letter (A-G).")
            input("Press Enter to continue...")
            continue
        
        col_idx = ord(col) - ord('A')
        row = drop_checker(board, col, symbols[current_player])
        
        if check_win(board, row, col_idx, symbols[current_player]):
            os.system('clear')
            print_board(board)
            print(f"Player {symbols[current_player]} won!")
            break
        
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
