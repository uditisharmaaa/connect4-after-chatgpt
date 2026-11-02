import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checker identifiers for the players

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(column + 65) for column in range(len(board[0]))))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def get_valid_columns(board):
    valid_columns = []
    for column_index in range(len(board[0])):
        if board[0][column_index] == ' ':
            valid_columns.append(chr(column_index + 65))
    return valid_columns

def place_checker(board, column, checker):
    for row_index in range(len(board)-1, -1, -1):
        if board[row_index][column] == ' ':
            board[row_index][column] = checker
            return

def check_for_win(board, checker):
    # Horizontal
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True
    # Vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    # Diagonal /
    for col in range(len(board[0]) - 3):
        for row in range(3, len(board)):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    # Diagonal \
    for col in range(len(board[0]) - 3):
        for row in range(len(board) - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    return False

def check_for_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player_index = random.choice(range(PLAYERS))

    while True:
        print_board(board)
        current_checker = players[current_player_index]
        valid_columns = get_valid_columns(board)

        if not valid_columns:
            print("The game is a draw.")
            break

        column_choice = input(f"Player {current_checker}, please enter a column ({', '.join(valid_columns)}): ").upper()

        if column_choice not in valid_columns:
            print(f"Invalid input. Please choose from {', '.join(valid_columns)}.")
            continue

        column_index = ord(column_choice) - 65
        place_checker(board, column_index, current_checker)

        if check_for_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if check_for_draw(board):
            print_board(board)
            print("The game is a draw.")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
