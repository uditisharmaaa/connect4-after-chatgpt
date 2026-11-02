import os
import random

# Global constants for board size and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2

# Player symbols depending on the number of players
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"][:PLAYERS]

def create_board():
    """Creates a 2D list to represent the Connect 4 board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the Connect 4 board."""
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def get_valid_column(board):
    """Prompts the player for a valid column and returns it."""
    while True:
        column_letter = input("Please enter a column: ")
        if len(column_letter) != 1 or not column_letter.isalpha():
            print("Invalid input. Enter a single letter.")
            continue
        column = ord(column_letter.upper()) - 65
        if column < 0 or column >= COLUMNS:
            print(f"Invalid input. Choose a column between A and {chr(64 + COLUMNS)}.")
            continue
        if board[0][column] != " ":
            print("Column is full. Choose another.")
            continue
        return column

def place_checker(board, column, symbol):
    """Places a checker for the player in the specified column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = symbol
            break

def check_for_win(board, symbol):
    """Checks the board for a win condition for a given symbol."""
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Diagonal (down-right) check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Diagonal (down-left) check
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == symbol for i in range(4)):
                return True

    return False

def check_for_draw(board):
    """Checks if the board is full (draw condition)."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board()
    print_board(board)

    current_player_index = random.randint(0, PLAYERS - 1)
    game_won = False

    while not game_won:
        current_symbol = PLAYER_SYMBOLS[current_player_index]
        print(f"Player {current_symbol}'s turn")
        column = get_valid_column(board)
        place_checker(board, column, current_symbol)
        print_board(board)

        if check_for_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            game_won = True
        elif check_for_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == '__main__':
    main()
