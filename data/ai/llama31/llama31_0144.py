import os
import random
import string

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with specified rows and columns"""
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Print the board with column labels"""
    print("  " + " ".join(string.ascii_uppercase[:BOARD_COLS]))
    print("+" + "---+" * BOARD_COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * BOARD_COLS)

def is_valid_input(col):
    """Check if user input is valid"""
    if not col.isalpha():
        return False
    col = ord(col.upper()) - ord('A')
    if col < 0 or col >= BOARD_COLS:
        return False
    return True

def is_valid_move(board, col):
    """Check if a move is valid (column is not full)"""
    col = ord(col.upper()) - ord('A')
    return board[0][col] == " "

def make_move(board, player, col):
    """Make a move by placing a checker in the specified column"""
    col = ord(col.upper()) - ord('A')
    for row in reversed(range(BOARD_ROWS)):
        if board[row][col] == " ":
            board[row][col] = CHECKERS[player]
            return

def check_win(board):
    """Check if there is a winner"""
    # Check horizontal locations for win
    for c in range(BOARD_COLS-3):
        for r in range(BOARD_ROWS):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3]!= " ":
                return True
    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c]!= " ":
                return True
    # Check positively sloped diagonals
    for c in range(BOARD_COLS-3):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3]!= " ":
                return True
    # Check negatively sloped diagonals
    for c in range(BOARD_COLS-3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3]!= " ":
                return True

def check_draw(board):
    """Check if the game is a draw"""
    for col in range(BOARD_COLS):
        if board[0][col] == " ":
            return False
    return True

def game():
    """Main game loop"""
    board = create_board()
    players = random.sample(range(NUM_PLAYERS), NUM_PLAYERS)
    current_player = 0

    while True:
        os.system('clear')
        print_board(board)
        print("Player", CHECKERS[players[current_player]], "please enter a column:")
        col = input()
        while not is_valid_input(col) or not is_valid_move(board, col):
            if not is_valid_input(col):
                print("Invalid input. Please enter a letter from A to G.")
            else:
                print("Invalid move. Column is full.")
            col = input()
        make_move(board, players[current_player], col)
        if check_win(board):
            os.system('clear')
            print_board(board)
            print("Player", CHECKERS[players[current_player]], "won!")
            break
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

game()
