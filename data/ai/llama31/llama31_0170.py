import os
import random

# Constant global variables
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    """
    Creates a 2D board with all elements initialized with whitespaces (" ").
    """
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """
    Prints the current state of the board.
    """
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---" * BOARD_COLS)
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_COLS)

def validate_input(player, column):
    """
    Validates the user input.
    """
    if not column.isalpha():
        return False
    if column.upper() not in "ABCDEFG":
        return False
    column_idx = ord(column.upper()) - ord('A')
    if column_idx < 0 or column_idx >= BOARD_COLS:
        return False
    if board[0][column_idx]!= " ":
        return False
    return True

def place_checker(board, player, column):
    """
    Places a checker in the specified column.
    """
    column_idx = ord(column.upper()) - ord('A')
    for row_idx in range(BOARD_ROWS - 1, -1, -1):
        if board[row_idx][column_idx] == " ":
            board[row_idx][column_idx] = player
            break

def check_win(board, player):
    """
    Checks for a win in all directions (horizontally, vertically, diagonally).
    """
    # Check horizontal
    for row_idx in range(BOARD_ROWS):
        for col_idx in range(BOARD_COLS - 3):
            if board[row_idx][col_idx] == player and \
               board[row_idx][col_idx + 1] == player and \
               board[row_idx][col_idx + 2] == player and \
               board[row_idx][col_idx + 3] == player:
                return True
    # Check vertical
    for row_idx in range(BOARD_ROWS - 3):
        for col_idx in range(BOARD_COLS):
            if board[row_idx][col_idx] == player and \
               board[row_idx + 1][col_idx] == player and \
               board[row_idx + 2][col_idx] == player and \
               board[row_idx + 3][col_idx] == player:
                return True
    # Check diagonal (top-left to bottom-right)
    for row_idx in range(BOARD_ROWS - 3):
        for col_idx in range(BOARD_COLS - 3):
            if board[row_idx][col_idx] == player and \
               board[row_idx + 1][col_idx + 1] == player and \
               board[row_idx + 2][col_idx + 2] == player and \
               board[row_idx + 3][col_idx + 3] == player:
                return True
    # Check diagonal (bottom-left to top-right)
    for row_idx in range(3, BOARD_ROWS):
        for col_idx in range(BOARD_COLS - 3):
            if board[row_idx][col_idx] == player and \
               board[row_idx - 1][col_idx + 1] == player and \
               board[row_idx - 2][col_idx + 2] == player and \
               board[row_idx - 3][col_idx + 3] == player:
                return True
    return False

def check_draw(board):
    """
    Checks if the board is full (draw).
    """
    for row in board:
        if " " in row:
            return False
    return True

def main():
    global board
    board = create_board()
    num_players = 2
    players = PLAYERS[:num_players]
    current_player_idx = random.randint(0, num_players - 1)
    while True:
        os.system('clear')
        print_board(board)
        print("Player", players[current_player_idx], "turn.")
        while True:
            column = input("Enter a column (A-G): ")
            if validate_input(players[current_player_idx], column):
                place_checker(board, players[current_player_idx], column)
                break
            else:
                print("Invalid input. Try again.")
        if check_win(board, players[current_player_idx]):
            os.system('clear')
            print_board(board)
            print("Player", players[current_player_idx], "won!")
            break
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("Draw!")
            break
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
