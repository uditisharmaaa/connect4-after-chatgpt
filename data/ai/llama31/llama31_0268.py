import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS = 2

def create_board():
    """Create a 2D board with whitespaces"""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print("  A", end="   ")
    for col in range(1, BOARD_COLS):
        print(chr(65 + col), end="   ")
    print()
    print("+---" * BOARD_COLS + "+")
    for row in range(BOARD_ROWS):
        print("|", end="   ")
        for col in range(BOARD_COLS):
            print(board[row][col], end="   ")
        print("|")
        print("+---" * BOARD_COLS + "+")

def get_player_order():
    """Randomly select the order of players"""
    players = random.sample(range(PLAYERS), PLAYERS)
    return players

def get_checker(player):
    """Get the checker symbol for a given player"""
    return CHECKERS[player]

def is_valid_input(col):
    """Check if the input column is valid"""
    if not col.isalpha():
        return False
    col = ord(col.upper()) - 65
    return 0 <= col < BOARD_COLS

def get_input(board, player):
    """Get the input column from the user"""
    while True:
        col = input(f"Player {get_checker(player)}, please enter a column: ")
        if is_valid_input(col):
            col = ord(col.upper()) - 65
            if board[0][col]!= " ":
                print("Column is full, please choose another column.")
            else:
                return col
        else:
            print("Invalid input, please enter a letter between A and G.")

def place_checker(board, col, player):
    """Place a checker in the given column"""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = get_checker(player)
            return

def check_win(board, player):
    """Check if the current player has won"""
    checker = get_checker(player)
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
    """Check if the game is a draw"""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True

def main():
    board = create_board()
    players = get_player_order()
    current_player = 0
    while True:
        print_board(board)
        col = get_input(board, current_player)
        place_checker(board, col, current_player)
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {get_checker(current_player)} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
