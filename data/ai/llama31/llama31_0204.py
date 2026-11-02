import os
import random
import string

# Global constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """
    Creates a 2D board with the specified dimensions, initialized with whitespaces.
    """
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """
    Prints the current state of the board.
    """
    os.system('clear')
    print("  " + " ".join(string.ascii_uppercase[:BOARD_COLS]))
    for row in board:
        print("+---" * BOARD_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_COLS + "+")

def is_valid_move(board, col):
    """
    Checks if a move is valid (i.e., the column is not full).
    """
    return board[0][col] == " "

def get_next_open_row(board, col):
    """
    Returns the index of the next open row in the specified column.
    """
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1  # Column is full

def drop_checker(board, row, col, checker):
    """
    Drops a checker into the specified column.
    """
    board[row][col] = checker

def check_win(board, checker):
    """
    Checks if the specified player has won.
    """
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

    return False

def check_draw(board):
    """
    Checks if the game is a draw (i.e., the board is full and no player has won).
    """
    return all(cell!= " " for row in board for cell in row)

def game():
    """
    The main game loop.
    """
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        move = input().strip().upper()

        if move not in string.ascii_uppercase[:BOARD_COLS]:
            print("Invalid input. Please enter a column letter.")
            continue

        col = ord(move) - ord('A')
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue

        row = get_next_open_row(board, col)
        drop_checker(board, row, col, current_player)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

game()
