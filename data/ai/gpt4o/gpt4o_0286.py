import os
import random

# Constants
NUM_PLAYERS = 2
BOARD_ROWS = 6
BOARD_COLS = 7
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")
    
# Check for win
def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == checker and row[col+1] == checker and row[col+2] == checker and row[col+3] == checker:
                return True
    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True
    # Check diagonals
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    return False

# Check for draw
def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def play_game():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        col = None
        
        while True:
            move = input(f"Player {checker}, please enter a column: ").upper()
            if len(move) == 1 and move.isalpha() and 'A' <= move <= chr(ord('A') + BOARD_COLS - 1):
                col = ord(move) - ord('A')
                if drop_checker(board, col, checker):
                    break
                else:
                    print(f"Column {move} is full. You lose your turn.")
                    break
            else:
                print("Invalid input. Please try again.")
        
        print_board(board)
        
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

# Start the game
play_game()
