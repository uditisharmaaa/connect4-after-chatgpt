import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board():
    board = []
    for _ in range(BOARD_ROWS):
        row = []
        for _ in range(BOARD_COLUMNS):
            row.append(" ")
        board.append(row)
    return board

# Print the board
def print_board(board, current_player):
    print("  A B C D E F G")
    for i in range(BOARD_ROWS):
        print("+---" * BOARD_COLUMNS + "+")
        row = ""
        for j in range(BOARD_COLUMNS):
            row += "| " + board[i][j] + " "
        print(row + "|")
    print("+---" * BOARD_COLUMNS + "+")
    print("Player " + CHECKERS[current_player-1] + ", please enter a column:")

# Get player's move
def get_move():
    while True:
        move = input().strip().upper()
        if move in "ABCDEFG" and ord(move) - 65 < BOARD_COLUMNS:
            return ord(move) - 65
        else:
            print("Invalid input. Please enter a column letter.")

# Check if column is full
def is_column_full(board, column):
    return board[0][column]!= " "

# Check for a win
def check_win(board, player):
    checker = CHECKERS[player-1]
    # Check horizontal locations for win
    for c in range(BOARD_COLUMNS-3):
        for r in range(BOARD_ROWS):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # Check vertical locations for win
    for c in range(BOARD_COLUMNS):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # Check positively sloped diagonals
    for c in range(BOARD_COLUMNS-3):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # Check negatively sloped diagonals
    for c in range(BOARD_COLUMNS-3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

# Check for a draw
def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

# Main game loop
def play_game():
    board = create_board()
    current_player = random.randint(1, PLAYERS)
    while True:
        os.system('clear')
        print_board(board, current_player)
        column = get_move()
        if is_column_full(board, column):
            print("Column is full. Try again.")
            continue
        for row in range(BOARD_ROWS-1, -1, -1):
            if board[row][column] == " ":
                board[row][column] = CHECKERS[current_player-1]
                break
        if check_win(board, current_player):
            os.system('clear')
            print_board(board, current_player)
            print("Player " + CHECKERS[current_player-1] + " won!")
            break
        if check_draw(board):
            os.system('clear')
            print_board(board, current_player)
            print("It's a draw!")
            break
        current_player = (current_player % PLAYERS) + 1

play_game()
