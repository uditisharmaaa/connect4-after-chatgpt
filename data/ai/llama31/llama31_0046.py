import os
import random
import string

# Constant global variables
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with the specified dimensions"""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board, player_turn):
    """Print the current state of the board"""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| " + " | ".join(row) + " |")
    print("+---+---+---+---+---+---+---+")
    print(f"Player {CHECKERS[player_turn]}, please enter a column: ")

def get_valid_column(board):
    """Get a valid column input from the user"""
    while True:
        column = input().upper()
        if column in string.ascii_uppercase[:BOARD_COLS]:
            column_index = string.ascii_uppercase.index(column)
            if board[0][column_index] == " ":
                return column_index
        print("Invalid input. Please enter a valid column (A-{})".format(string.ascii_uppercase[BOARD_COLS-1]))

def drop_checker(board, column, player):
    """Drop a checker in the specified column"""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = CHECKERS[player]
            return

def check_win(board, player):
    """Check if the current player has won"""
    # Check horizontal wins
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == CHECKERS[player] and row[i+1] == CHECKERS[player] and row[i+2] == CHECKERS[player] and row[i+3] == CHECKERS[player]:
                return True

    # Check vertical wins
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == CHECKERS[player] and board[i+1][col] == CHECKERS[player] and board[i+2][col] == CHECKERS[player] and board[i+3][col] == CHECKERS[player]:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == CHECKERS[player] and board[row+1][col+1] == CHECKERS[player] and board[row+2][col+2] == CHECKERS[player] and board[row+3][col+3] == CHECKERS[player]:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == CHECKERS[player] and board[row-1][col+1] == CHECKERS[player] and board[row-2][col+2] == CHECKERS[player] and board[row-3][col+3] == CHECKERS[player]:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw"""
    return all(all(cell!= " " for cell in row) for row in board)

def main():
    # Initialize the board and players
    board = create_board()
    num_players = 2
    players = [i for i in range(num_players)]
    current_player = random.choice(players)

    # Game loop
    while True:
        print_board(board, current_player)
        column = get_valid_column(board)
        drop_checker(board, column, current_player)
        if check_win(board, current_player):
            print_board(board, current_player)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print_board(board, current_player)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
