import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty board with NUM_ROWS rows and NUM_COLS columns"""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear')

def print_board(board):
    """Print the current state of the board"""
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(NUM_COLS)))
    
    # Print rows with borders
    border = "+" + ("---+" * NUM_COLS)
    for row in board:
        print(border)
        print("| " + " | ".join(cell for cell in row) + " |")
    print(border)

def get_random_first_player():
    """Return a random player index to start the game"""
    return random.randint(0, NUM_PLAYERS - 1)

def get_valid_column_input(current_player):
    """Ask the current player for a column until valid input is provided"""
    while True:
        column_input = input(f"Player {PLAYER_SYMBOLS[current_player]}, please enter a column: ").upper()
        if len(column_input) != 1:
            print("Invalid input. Please enter a single letter from A to " + chr(65 + NUM_COLS - 1))
            continue
        
        column = ord(column_input) - ord('A')
        if 0 <= column < NUM_COLS:
            return column
        else:
            print(f"Invalid column. Please choose from A to {chr(65 + NUM_COLS - 1)}")

def place_checker(board, column, player_symbol):
    """Place the player's checker in the specified column if possible"""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player_symbol
            return True  # Successfully placed
    return False  # Column is full

def check_win(board, row, col):
    """Check if the last move resulted in a win"""
    symbol = board[row][col]
    
    # Check horizontal
    count = 1
    # Left
    left = col - 1
    while left >= 0 and board[row][left] == symbol:
        count += 1
        left -= 1
    # Right
    right = col + 1
    while right < NUM_COLS and board[row][right] == symbol:
        count += 1
        right += 1
    if count >= 4:
        return True
    
    # Check vertical
    count = 1
    # Down
    down = row + 1
    while down < NUM_ROWS and board[down][col] == symbol:
        count += 1
        down += 1
    if count >= 4:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Top-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == symbol:
        count += 1
        r -= 1
        c -= 1
    # Bottom-right
    r, c = row + 1, col + 1
    while r < NUM_ROWS and c < NUM_COLS and board[r][c] == symbol:
        count += 1
        r += 1
        c += 1
    if count >= 4:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Top-right
    r, c = row - 1, col + 1
    while r >= 0 and c < NUM_COLS and board[r][c] == symbol:
        count += 1
        r -= 1
        c += 1
    # Bottom-left
    r, c = row + 1, col - 1
    while r < NUM_ROWS and c >= 0 and board[r][c] == symbol:
        count += 1
        r += 1
        c -= 1
    if count >= 4:
        return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (all cells filled)"""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main game loop"""
    board = initialize_board()
    current_player = get_random_first_player()
    
    while True:
        clear_screen()
        print_board(board)
        
        column = get_valid_column_input(current_player)
        placed = place_checker(board, column, PLAYER_SYMBOLS[current_player])
        
        if not placed:
            print("Column is full. You lose your turn!")
            continue
        
        # Check for win
        for row in range(NUM_ROWS):
            if board[row][column] == PLAYER_SYMBOLS[current_player]:
                if check_win(board, row, column):
                    clear_screen()
                    print_board(board)
                    print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
                    return
        
        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            return
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
