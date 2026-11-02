import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return empty board"""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels"""
    os.system('clear')
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(f" {chr(65 + i)}  ", end="")
    print()
    
    # Print rows
    for row in board:
        print("+---" * COLS + "+")
        print("| ", end="")
        for cell in row:
            print(f"{cell} | ", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_move(board, col):
    """Check if column has space"""
    return 0 <= col < COLS and board[0][col] == " "

def drop_checker(board, col, checker):
    """Drop checker in column, return row where placed"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if current move wins the game"""
    # Horizontal
    count = 1
    for c in range(col - 1, -1, -1):
        if board[row][c] == checker:
            count += 1
        else:
            break
    for c in range(col + 1, COLS):
        if board[row][c] == checker:
            count += 1
        else:
            break
    if count >= 4:
        return True
    
    # Vertical
    count = 1
    for r in range(row + 1, ROWS):
        if board[r][col] == checker:
            count += 1
        else:
            break
    if count >= 4:
        return True
    
    # Diagonal (/)
    count = 1
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS:
        if board[r][c] == checker:
            count += 1
            r -= 1
            c += 1
        else:
            break
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0:
        if board[r][c] == checker:
            count += 1
            r += 1
            c -= 1
        else:
            break
    if count >= 4:
        return True
    
    # Diagonal (\)
    count = 1
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        if board[r][c] == checker:
            count += 1
            r -= 1
            c -= 1
        else:
            break
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            r += 1
            c += 1
        else:
            break
    if count >= 4:
        return True
    
    return False

def is_board_full(board):
    """Check if board is full"""
    return all(board[0][col] != " " for col in range(COLS))

def play_game():
    """Main game loop"""
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column: ", end="")
        
        user_input = input().strip().upper()
        
        # Validate input
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col = ord(user_input) - ord('A')
        
        if col < 0 or col >= COLS:
            print("Column out of range.")
            continue
        
        if not is_valid_move(board, col):
            print("Column is full.")
            continue
        
        # Drop checker
        row = drop_checker(board, col, checker)
        print_board(board)
        
        # Check win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        # Check draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
