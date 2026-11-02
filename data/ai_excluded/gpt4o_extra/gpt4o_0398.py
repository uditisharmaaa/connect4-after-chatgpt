import os
import random


# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]


def initialize_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    os.system('clear')
    column_labels = "  " + "   ".join([chr(65 + i) for i in range(len(board[0]))])
    print(column_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")


def get_valid_columns(board):
    return [chr(65 + i) for i in range(len(board[0])) if board[0][i] == " "]


def validate_input(input_char, valid_columns):
    return input_char in valid_columns


def place_checker(board, column, checker):
    column_index = ord(column) - 65
    for row in range(len(board) - 1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = checker
            return


def check_winner(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
                
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    return False


def check_draw(board):
    return all(board[0][i] != " " for i in range(COLUMNS))


def main():
    board = initialize_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        current_player = CHECKERS[current_player_index]
        valid_columns = get_valid_columns(board)

        if not valid_columns:
            print("The game is a draw!")
            break

        player_input = input(f"Player {current_player}, please enter a column: ").upper()

        while not validate_input(player_input, valid_columns):
            player_input = input(f"Invalid input. Player {current_player}, please enter a valid column ({', '.join(valid_columns)}): ").upper()

        place_checker(board, player_input, current_player)
        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS


if __name__ == "__main__":
    main()
