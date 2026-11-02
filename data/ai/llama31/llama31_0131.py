import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with the given dimensions."""
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(*row))
    print("+---+---+---+---+---+---+---+")

def is_valid_move(board, column):
    """Check if a move is valid (i.e., the column is not full)."""
    return board[0][column] == " "

def get_player_checker(player):
    """Get the checker for the given player."""
    return CHECKERS[player]

def place_checker(board, player, column):
    """Place the player's checker in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = get_player_checker(player)
            break

def check_win(board, player):
    """Check if the given player has won."""
    checker = get_player_checker(player)
    # Check horizontal
    for row in board:
        for i in range(COLUMNS - 3):
            if row[i] == checker and row[i + 1] == checker and row[i + 2] == checker and row[i + 3] == checker:
                return True
    # Check vertical
    for col in range(COLUMNS):
        for i in range(ROWS - 3):
            if board[i][col] == checker and board[i + 1][col] == checker and board[i + 2][col] == checker and board[i + 3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(board[0][i]!= " " for i in range(COLUMNS))

def game():
    """Play the game."""
    board = create_board()
    players = list(range(PLAYERS))
    random.shuffle(players)
    current_player = 0
    while True:
        print_board(board)
        print("Player", get_player_checker(current_player), ", please enter a column:")
        while True:
            try:
                column = ord(input().upper()) - ord('A')
                if column < 0 or column >= COLUMNS:
                    raise ValueError
                if not is_valid_move(board, column):
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Please enter a letter between A and G.")
        place_checker(board, current_player, column)
        if check_win(board, current_player):
            print_board(board)
            print("Player", get_player_checker(current_player), "won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    game()
