import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    return 0 <= column < COLUMNS and board[0][column] == " "

def get_column_input(player, board):
    while True:
        try:
            column = input(f"Player {player}, please enter a column: ").upper()
            column_index = ord(column) - 65
            if is_valid_column(column_index, board):
                return column_index
            else:
                print("Invalid column. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Try again.")

def place_checker(column, player, board):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player
            return

def check_winner(board, player):
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)) or \
               all(board[row + i][col + 3 - i] == player for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board()
    current_player_index = random.randint(0, PLAYERS - 1)
    players = CHECKERS[:PLAYERS]
    print_board(board)

    while True:
        current_player = players[current_player_index]
        column = get_column_input(current_player, board)
        place_checker(column, current_player, board)
        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
