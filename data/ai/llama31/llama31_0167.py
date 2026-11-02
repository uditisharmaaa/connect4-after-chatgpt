import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2

def create_board():
    """Create an empty Connect 4 board."""
    board = [[" " for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board, player_turn):
    """Print the Connect 4 board."""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("|", end=" ")
        for cell in row:
            print(cell, end=" | ")
        print()
    print("+---+---+---+---+---+---+---+")
    print(f"Player {PLAYER_CHECKERS[player_turn]}, please enter a column:")

def get_player_move(board):
    """Get a valid move from the player."""
    while True:
        move = input().upper()
        if move not in "ABCDEFG":
            print("Invalid move. Please enter a column letter (A-G).")
        elif board[0][ord(move) - ord('A')]!= " ":
            print("Column is full. Please enter a different column.")
        else:
            return ord(move) - ord('A')

def drop_checker(board, column, checker):
    """Drop a checker into the specified column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

def check_win(board, player_turn):
    """Check if the current player has won."""
    checker = PLAYER_CHECKERS[player_turn]
    # Check horizontal wins
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == checker:
                return True
    # Check vertical wins
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == checker:
                return True
    # Check diagonal wins (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == checker:
                return True
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == checker:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def game():
    """Play a game of Connect 4."""
    board = create_board()
    player_turn = random.randint(0, NUM_PLAYERS - 1)
    while True:
        print_board(board, player_turn)
        column = get_player_move(board)
        drop_checker(board, column, PLAYER_CHECKERS[player_turn])
        if check_win(board, player_turn):
            print_board(board, player_turn)
            print(f"Player {PLAYER_CHECKERS[player_turn]} won!")
            break
        elif check_draw(board):
            print_board(board, player_turn)
            print("It's a draw!")
            break
        player_turn = (player_turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    game()
