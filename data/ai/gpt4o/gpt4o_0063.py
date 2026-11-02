import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYER_COUNT]

def create_board():
    """Create an empty board with spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear screen before printing
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_input(user_input):
    """Check if user input is a valid column."""
    return user_input.isalpha() and 65 <= ord(user_input.upper()) < 65 + COLS

def get_next_open_row(board, col):
    """Find the next open row in the chosen column."""
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def is_winning_move(board, checker):
    """Check for winning move."""
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertically
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check positively sloped diagonals
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check negatively sloped diagonals
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    """Check if board is full for a draw."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    print_board(board)
    current_player = random.choice(range(PLAYER_COUNT))
    
    # Game loop
    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column_input = input("> ").strip()
        
        if not is_valid_input(column_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col = ord(column_input.upper()) - 65
        row = get_next_open_row(board, col)
        
        if row is None:
            print("Column is full. Turn is invalid and lost.")
            current_player = (current_player + 1) % PLAYER_COUNT
            continue
        
        board[row][col] = CHECKERS[current_player]
        print_board(board)
        
        if is_winning_move(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if is_draw(board):
            print("Game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
