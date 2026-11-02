import os
import random
import string

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5

def create_board():
    """
    Creates a 2D board with all elements initialized to whitespace.
    """
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """
    Prints the current state of the board.
    """
    print("  A B C D E F G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} |".format(" | ".join(row)))
    print("+---+---+---+---+---+---+---+")

def get_players(num_players):
    """
    Returns a list of players, each represented by a unique character.
    """
    players = []
    chars = ["X", "O", "V", "H", "M"]
    for i in range(num_players):
        players.append(chars[i])
    return players

def get_next_player(players, current_player):
    """
    Returns the next player in the list of players.
    """
    return players[(players.index(current_player) + 1) % len(players)]

def is_valid_input(board, col):
    """
    Checks if the input is a valid column and if the column is not full.
    """
    if not col.isalpha() or not col.upper() in string.ascii_uppercase[:BOARD_COLS]:
        return False
    col_idx = string.ascii_uppercase.index(col.upper())
    return board[0][col_idx] == " "

def get_column(board, col):
    """
    Returns the column index corresponding to the input column.
    """
    return string.ascii_uppercase.index(col.upper())

def place_checker(board, player, col):
    """
    Places the player's checker in the specified column.
    """
    col_idx = get_column(board, col)
    for row in reversed(board):
        if row[col_idx] == " ":
            row[col_idx] = player
            break

def check_win(board, player):
    """
    Checks if the player has won by examining all possible winning combinations.
    """
    # Check horizontal wins
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == player and row[i + 1] == player and row[i + 2] == player and row[i + 3] == player:
                return True

    # Check vertical wins
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == player and board[i + 1][col] == player and board[i + 2][col] == player and board[i + 3][col] == player:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

def check_draw(board):
    """
    Checks if the game is a draw by examining if the board is full.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def game():
    """
    The main game loop.
    """
    board = create_board()
    players = get_players(2)
    current_player = random.choice(players)

    while True:
        os.system('clear')
        print_board(board)
        print("Player {}, please enter a column:".format(current_player))
        col = input().strip()

        while not is_valid_input(board, col):
            print("Invalid input. Please try again.")
            col = input().strip()

        place_checker(board, current_player, col)

        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print("Player {} won!".format(current_player))
            break

        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player = get_next_player(players, current_player)

if __name__ == "__main__":
    game()
