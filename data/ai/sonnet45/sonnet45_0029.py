import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board"""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current board state"""
    os.system('clear')
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(f" {chr(65 + i)}  ", end="")
    print()
    
    # Print rows with borders
    for row in board:
        print("+" + "---+" * COLS)
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+" + "---+" * COLS)

def is_valid_move(board, col):
    """Check if a move is valid"""
    return 0 <= col < COLS and board[0][col] == " "

def place_checker(board, col, checker):
    """Place a checker in the specified column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win"""
    # Horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Diagonal (bottom-left to top-right)
    count = 0
    start_r = row - min(row, col)
    start_c = col - min(row, col)
    while start_r < ROWS and start_c < COLS:
        if board[start_r][start_c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        start_r += 1
        start_c += 1
    
    # Diagonal (top-left to bottom-right)
    count = 0
    start_r = row + min(ROWS - 1 - row, col)
    start_c = col - min(ROWS - 1 - row, col)
    while start_r >= 0 and start_c < COLS:
        if board[start_r][start_c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        start_r -= 1
        start_c += 1
    
    return False

def is_board_full(board):
    """Check if the board is full"""
    return all(board[0][c] != " " for c in range(COLS))

def play_game():
    """Main game loop"""
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        
        # Get valid input
        while True:
            user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
            
            if len(user_input) != 1 or not user_input.isalpha():
                print("Invalid input. Please enter a letter.")
                continue
            
            col = ord(user_input) - 65
            
            if col < 0 or col >= COLS:
                print("Invalid column. Please try again.")
                continue
            
            if not is_valid_move(board, col):
                print("Column is full. You lose your turn.")
                break
            
            # Place checker and check for win
            row = place_checker(board, col, checker)
            print_board(board)
            
            if check_win(board, row, col, checker):
                print(f"Player {checker} won!")
                return
            
            if is_board_full(board):
                print("It's a draw!")
                return
            
            break
        
        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
