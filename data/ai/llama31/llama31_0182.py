import os
import random

# Global constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Create the board
board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

# Function to print the board
def print_board():
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for i in range(NUM_ROWS):
        print('+---+---+---+---+---+---+---+')
        row = '|'
        for j in range(NUM_COLS):
            row += ' ' + board[i][j] + ' |'
        print(row)
    print('+---+---+---+---+---+---+---+')

# Function to get the next player
def get_next_player(current_player):
    return (current_player + 1) % NUM_PLAYERS

# Function to check if the input is valid
def is_valid_input(input_str):
    if len(input_str)!= 1:
        return False
    if ord(input_str.upper()) < ord('A') or ord(input_str.upper()) > ord('G'):
        return False
    return True

# Function to check if a column is full
def is_column_full(col):
    return board[NUM_ROWS-1][col]!= ' '

# Function to place a checker in a column
def place_checker(col, checker):
    for i in range(NUM_ROWS-1, -1, -1):
        if board[i][col] == ' ':
            board[i][col] = checker
            return

# Function to check for a win
def check_win(player_checker):
    # Check horizontal locations for win
    for c in range(NUM_COLS-3):
        for r in range(NUM_ROWS):
            if board[r][c] == player_checker and board[r][c+1] == player_checker and board[r][c+2] == player_checker and board[r][c+3] == player_checker:
                return True

    # Check vertical locations for win
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS-3):
            if board[r][c] == player_checker and board[r+1][c] == player_checker and board[r+2][c] == player_checker and board[r+3][c] == player_checker:
                return True

    # Check positively sloped diagonals
    for c in range(NUM_COLS-3):
        for r in range(NUM_ROWS-3):
            if board[r][c] == player_checker and board[r+1][c+1] == player_checker and board[r+2][c+2] == player_checker and board[r+3][c+3] == player_checker:
                return True

    # Check negatively sloped diagonals
    for c in range(NUM_COLS-3):
        for r in range(3, NUM_ROWS):
            if board[r][c] == player_checker and board[r-1][c+1] == player_checker and board[r-2][c+2] == player_checker and board[r-3][c+3] == player_checker:
                return True

# Function to check for a draw
def check_draw():
    for c in range(NUM_COLS):
        if board[NUM_ROWS-1][c] == ' ':
            return False
    return True

# Initialize the game
current_player = random.randint(0, NUM_PLAYERS-1)
print_board()

# Main game loop
while True:
    player_checker = CHECKERS[current_player]
    print("Player " + player_checker + ", please enter a column:")
    input_str = input().upper()
    while not is_valid_input(input_str) or is_column_full(ord(input_str)-ord('A')):
        print("Invalid input. Please try again.")
        input_str = input().upper()
    place_checker(ord(input_str)-ord('A'), player_checker)
    print_board()
    if check_win(player_checker):
        print("Player " + player_checker + " won!")
        break
    elif check_draw():
        print("It's a draw!")
        break
    current_player = get_next_player(current_player)
