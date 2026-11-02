import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def create_board():
    """Create a new game board with the specified dimensions."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board to the console."""
    os.system('clear')
    print("  " + " ".join(LETTERS[:COLUMNS]))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def validate_input(column, board):
    """Validate the player's input."""
    if len(column)!= 1 or column.upper() not in LETTERS[:COLUMNS]:
        return False
    column = LETTERS.index(column.upper())
    if board[0][column]!= " ":
        return False
    return True

def place_checker(column, player, board):
    """Place a checker on the board."""
    column = LETTERS.index(column.upper())
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player
            break

def check_win(player, board):
    """Check for a win."""
    # Horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True
    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True
    # Diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True
    # Diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True
    return False

def check_draw(board):
    """Check for a draw."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    while True:
        print_board(board)
        print("Player " + current_player + ", please enter a column:")
        column = input().upper()
        while not validate_input(column, board):
            print("Invalid input. Please try again.")
            column = input().upper()
        place_checker(column, current_player, board)
        if check_win(current_player, board):
            print_board(board)
            print("Player " + current_player + " won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
