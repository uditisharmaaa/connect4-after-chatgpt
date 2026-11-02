import os
import random

# Global constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    header = "  "
    for col in range(COLS):
        header += chr(ord('A') + col) + "   "
    print(header)
    
    # Print board with rows
    for row in board:
        print("+---" * COLS + "+")
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    print("+---" * COLS + "+")

def is_valid_move(board, col):
    """Check if a move in the given column is valid."""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "

def place_checker(board, col, checker):
    """Place a checker in the given column and return the row."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def get_valid_column(prompt):
    """Get a valid column input from the player."""
    while True:
        user_input = input(prompt).strip().upper()
        
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col = ord(user_input) - ord('A')
        if col < 0 or col >= COLS:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
            continue
        
        return col

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    checker_list = CHECKERS[:NUM_PLAYERS]
    
    print_board(board)
    
    while True:
        current_checker = checker_list[current_player]
        
        while True:
            col = get_valid_column(f"Player {current_checker}, please enter a column: ")
            if is_valid_move(board, col):
                row = place_checker(board, col, current_checker)
                break
            else:
                print("Column is full. Please choose another column.")
        
        print_board(board)
        
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            return
        
        if is_board_full(board):
            print("It's a draw!")
            return
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
