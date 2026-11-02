import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Create and return an empty board with NUM_ROWS rows and NUM_COLS columns."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column labels
    col_labels = [chr(ord('A') + i) for i in range(NUM_COLS)]
    print("  " + "   ".join(col_labels))
    
    # Print the board rows with borders
    border = "+" + ("---+" * NUM_COLS)
    for row in board:
        print(border)
        print("| " + " | ".join(row) + " |")
    print(border)

def get_random_first_player():
    """Return a random player number (0 to NUM_PLAYERS - 1)."""
    return random.randint(0, NUM_PLAYERS - 1)

def get_valid_column(current_player, board):
    """Prompt the player for a valid column input until one is provided."""
    while True:
        try:
            col_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").upper()
            if len(col_input) != 1 or col_input < 'A' or col_input > chr(ord('A') + NUM_COLS - 1):
                raise ValueError("Invalid column. Please enter a letter from A to " + chr(ord('A') + NUM_COLS - 1))
            
            col = ord(col_input) - ord('A')
            if board[0][col] != " ":
                print("Column is full. Choose another column.")
                continue
            
            return col
        except ValueError as e:
            print(e)

def place_checker(board, col, current_player):
    """Place the current player's checker in the specified column."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = CHECKERS[current_player]
            return row
    return -1  # Column is full (shouldn't happen due to prior validation)

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
        for step in [1, -1]:
            r, c = row + step * dr, col + step * dc
            while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
                count += 1
                r += step * dr
                c += step * dc
                if count == 4:
                    return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != " " for cell in board[0])

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = get_random_first_player()
    print_board(board)
    
    while True:
        col = get_valid_column(current_player, board)
        row = place_checker(board, col, current_player)
        print_board(board)
        
        if check_win(board, row, col, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
