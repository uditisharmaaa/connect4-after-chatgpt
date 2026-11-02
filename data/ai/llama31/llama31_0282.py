import os
import random

# Constant global variables
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Function to create the board
def create_board():
    board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return board

# Function to print the board
def print_board(board):
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for i in range(NUM_ROWS):
        print("+---+---+---+---+---+---+---+")
        for j in range(NUM_COLS):
            print("| {} |".format(board[i][j]), end="")
        print()
    print("+---+---+---+---+---+---+---+")

# Function to get the column from user input
def get_column():
    while True:
        column = input("Enter a column (A-{}): ".format(chr(ord('A') + NUM_COLS - 1)))
        if len(column) == 1 and 'A' <= column <= chr(ord('A') + NUM_COLS - 1):
            return ord(column) - ord('A')
        print("Invalid input. Please try again.")

# Function to place a checker on the board
def place_checker(board, player, column):
    for i in range(NUM_ROWS - 1, -1, -1):
        if board[i][column] == " ":
            board[i][column] = CHECKERS[player]
            return True
    return False

# Function to check for a win
def check_win(board, player):
    # Check horizontal locations for win
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS):
            if board[r][c] == CHECKERS[player] and board[r][c+1] == CHECKERS[player] and board[r][c+2] == CHECKERS[player] and board[r][c+3] == CHECKERS[player]:
                return True

    # Check vertical locations for win
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == CHECKERS[player] and board[r+1][c] == CHECKERS[player] and board[r+2][c] == CHECKERS[player] and board[r+3][c] == CHECKERS[player]:
                return True

    # Check positively sloped diagonals
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == CHECKERS[player] and board[r+1][c+1] == CHECKERS[player] and board[r+2][c+2] == CHECKERS[player] and board[r+3][c+3] == CHECKERS[player]:
                return True

    # Check negatively sloped diagonals
    for c in range(NUM_COLS - 3):
        for r in range(3, NUM_ROWS):
            if board[r][c] == CHECKERS[player] and board[r-1][c+1] == CHECKERS[player] and board[r-2][c+2] == CHECKERS[player] and board[r-3][c+3] == CHECKERS[player]:
                return True

    return False

# Function to check for a draw
def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

# Main game loop
def game_loop():
    board = create_board()
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)
    current_player = 0
    while True:
        print_board(board)
        print("Player {}, please enter a column:".format(CHECKERS[players[current_player]]))
        column = get_column()
        if place_checker(board, players[current_player], column):
            if check_win(board, players[current_player]):
                print_board(board)
                print("Player {} won!".format(CHECKERS[players[current_player]]))
                break
            elif check_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            current_player = (current_player + 1) % NUM_PLAYERS
        else:
            print("Column is full. Please try again.")

# Start the game
game_loop()
