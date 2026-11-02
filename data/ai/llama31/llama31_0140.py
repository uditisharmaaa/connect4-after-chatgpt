import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with the specified dimensions"""
    board = [[" " for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print("  A B C D E F G")
    for i in range(BOARD_ROWS):
        print("+---" * BOARD_COLUMNS + "+")
        row = "|"
        for j in range(BOARD_COLUMNS):
            row += " " + board[i][j] + " |"
        print(row)
    print("+---" * BOARD_COLUMNS + "+")

def get_random_first_player():
    """Randomly select the first player"""
    return random.randint(0, PLAYERS - 1)

def get_player_input(player, board):
    """Get the column input from the player"""
    while True:
        column = input(f"Player {CHECKERS[player]}, please enter a column (A-{chr(64 + BOARD_COLUMNS)}): ").upper()
        if column.isalpha() and 64 < ord(column) < 64 + BOARD_COLUMNS:
            column = ord(column) - 65
            if board[0][column]!= " ":
                print("Column is full, please choose another column.")
            else:
                return column
        else:
            print("Invalid input, please try again.")

def place_checker(board, column, player):
    """Place the checker in the specified column"""
    for i in range(BOARD_ROWS - 1, -1, -1):
        if board[i][column] == " ":
            board[i][column] = CHECKERS[player]
            break

def check_win(board, player):
    """Check if the player has won"""
    # Check horizontal wins
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLUMNS - 3):
            if board[i][j] == CHECKERS[player] and board[i][j + 1] == CHECKERS[player] and board[i][j + 2] == CHECKERS[player] and board[i][j + 3] == CHECKERS[player]:
                return True
    # Check vertical wins
    for i in range(BOARD_ROWS - 3):
        for j in range(BOARD_COLUMNS):
            if board[i][j] == CHECKERS[player] and board[i + 1][j] == CHECKERS[player] and board[i + 2][j] == CHECKERS[player] and board[i + 3][j] == CHECKERS[player]:
                return True
    # Check diagonal wins (top-left to bottom-right)
    for i in range(BOARD_ROWS - 3):
        for j in range(BOARD_COLUMNS - 3):
            if board[i][j] == CHECKERS[player] and board[i + 1][j + 1] == CHECKERS[player] and board[i + 2][j + 2] == CHECKERS[player] and board[i + 3][j + 3] == CHECKERS[player]:
                return True
    # Check diagonal wins (bottom-left to top-right)
    for i in range(3, BOARD_ROWS):
        for j in range(BOARD_COLUMNS - 3):
            if board[i][j] == CHECKERS[player] and board[i - 1][j + 1] == CHECKERS[player] and board[i - 2][j + 2] == CHECKERS[player] and board[i - 3][j + 3] == CHECKERS[player]:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw"""
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLUMNS):
            if board[i][j] == " ":
                return False
    return True

def main():
    board = create_board()
    print_board(board)
    first_player = get_random_first_player()
    current_player = first_player
    while True:
        column = get_player_input(current_player, board)
        place_checker(board, column, current_player)
        print_board(board)
        if check_win(board, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
