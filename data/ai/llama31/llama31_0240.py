import os
import random

# Constant global variables
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with the given dimensions."""
    return [[" " for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("|", end=" ")
        for cell in row:
            print(cell, end=" | ")
        print()
    print("+---+---+---+---+---+---+---+")

def is_valid_input(input_str):
    """Check if the user input is a valid column letter."""
    return len(input_str) == 1 and 'A' <= input_str.upper() <= chr(65 + BOARD_WIDTH - 1)

def get_column_index(input_str):
    """Convert the column letter to a 0-based index."""
    return ord(input_str.upper()) - 65

def is_valid_move(board, column):
    """Check if the move is valid (i.e., the column is not full)."""
    return board[0][column] == " "

def make_move(board, player, column):
    """Place the player's checker in the given column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = CHECKERS[player]
            break

def check_win(board, player):
    """Check if the player has won."""
    # Check horizontal locations for win
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT):
            if board[r][c] == CHECKERS[player] and board[r][c + 1] == CHECKERS[player] and board[r][c + 2] == CHECKERS[player] and board[r][c + 3] == CHECKERS[player]:
                return True

    # Check vertical locations for win
    for c in range(BOARD_WIDTH):
        for r in range(BOARD_HEIGHT - 3):
            if board[r][c] == CHECKERS[player] and board[r + 1][c] == CHECKERS[player] and board[r + 2][c] == CHECKERS[player] and board[r + 3][c] == CHECKERS[player]:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT - 3):
            if board[r][c] == CHECKERS[player] and board[r + 1][c + 1] == CHECKERS[player] and board[r + 2][c + 2] == CHECKERS[player] and board[r + 3][c + 3] == CHECKERS[player]:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_WIDTH - 3):
        for r in range(3, BOARD_HEIGHT):
            if board[r][c] == CHECKERS[player] and board[r - 1][c + 1] == CHECKERS[player] and board[r - 2][c + 2] == CHECKERS[player] and board[r - 3][c + 3] == CHECKERS[player]:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw (i.e., the board is full)."""
    return all(cell!= " " for row in board for cell in row)

def game():
    board = create_board()
    print_board(board)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        input_str = input(f"Player {CHECKERS[current_player]}, please enter a column: ")
        if not is_valid_input(input_str):
            print("Invalid input. Please try again.")
            continue
        column = get_column_index(input_str)
        if not is_valid_move(board, column):
            print("Invalid move. Please try again.")
            continue
        make_move(board, current_player, column)
        print_board(board)
        if check_win(board, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

game()
