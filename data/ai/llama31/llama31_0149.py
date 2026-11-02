import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = "XOVHM"

def create_board():
    """Create an empty board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  " + " ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_player():
    """Get the current player."""
    return CHECKERS[(turn // PLAYERS) % PLAYERS]

def is_valid_move(board, column):
    """Check if a move is valid."""
    return board[0][column] == " "

def make_move(board, column, player):
    """Make a move."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player
            break

def check_win(board, player):
    """Check if the current player has won."""
    # Check horizontal
    for row in board:
        for i in range(COLUMNS - 3):
            if row[i] == player and row[i+1] == player and row[i+2] == player and row[i+3] == player:
                return True
    # Check vertical
    for column in range(COLUMNS):
        for i in range(ROWS - 3):
            if board[i][column] == player and board[i+1][column] == player and board[i+2][column] == player and board[i+3][column] == player:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for column in range(COLUMNS - 3):
            if board[row][column] == player and board[row+1][column+1] == player and board[row+2][column+2] == player and board[row+3][column+3] == player:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for column in range(COLUMNS - 3):
            if board[row][column] == player and board[row-1][column+1] == player and board[row-2][column+2] == player and board[row-3][column+3] == player:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= " " for row in board for cell in row)

board = create_board()
print_board(board)
turn = random.randint(0, PLAYERS - 1)

while True:
    player = get_player()
    while True:
        column = input(f"Player {player}, please enter a column: ")
        if column.isalpha() and 65 <= ord(column.upper()) <= 90 and 0 <= ord(column.upper()) - 65 < COLUMNS:
            column = ord(column.upper()) - 65
            if is_valid_move(board, column):
                make_move(board, column, player)
                break
            else:
                print("Invalid move, column is full.")
        else:
            print("Invalid input, please enter a letter between A and G.")
    print_board(board)
    if check_win(board, player):
        print(f"Player {player} won!")
        break
    elif check_draw(board):
        print("It's a draw!")
        break
    turn += 1
