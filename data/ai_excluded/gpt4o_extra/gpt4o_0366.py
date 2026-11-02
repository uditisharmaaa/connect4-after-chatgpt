import os
import random

# Constants for board dimensions and number of players
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Function to create an empty board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(i) for i in range(65, 65+COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")
        
# Function to check if column is valid
def is_valid_column(column):
    return 0 <= column < COLS

# Function to get lowest available row in column
def get_next_open_row(board, column):
    for r in range(ROWS-1, -1, -1):
        if board[r][column] == ' ':
            return r
    return -1

# Function to check for win
def check_win(board, checker):
    # Check horizontal locations
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # Check vertical locations
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # Check positively sloped diagonals
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # Check negatively sloped diagonals
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

# Function to check for draw
def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

# Main game function
def play_game():
    board = create_board()
    game_over = False
    turn = random.randint(0, NUM_PLAYERS-1)
    
    while not game_over:
        print_board(board)
        player = f"Player {CHECKERS[turn]}"
        
        valid_input = False
        column = -1
        
        while not valid_input:
            col_input = input(f"{player}, please enter a column (A-{chr(65+COLS-1)}): ")
            if len(col_input) == 1 and 'A' <= col_input < chr(65+COLS):
                column = ord(col_input) - 65
                if is_valid_column(column) and get_next_open_row(board, column) != -1:
                    valid_input = True
                else:
                    print("Invalid column or column is full. Try again.")
            else:
                print("Invalid input. Please enter a valid column letter.")
        
        row = get_next_open_row(board, column)
        board[row][column] = CHECKERS[turn]
        
        if check_win(board, CHECKERS[turn]):
            print_board(board)
            print(f"{player} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        
        turn = (turn + 1) % NUM_PLAYERS

# Start the game
play_game()
