import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = '  ' + '   '.join(chr(65 + i) for i in range(len(board[0])))
    print(header)
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_input(column_input, board):
    valid_columns = [chr(65 + i) for i in range(len(board[0]))]
    return column_input in valid_columns and not is_column_full(column_input, board)

def is_column_full(column_input, board):
    col_index = ord(column_input) - 65
    return all(row[col_index] != " " for row in board)

def place_checker(column_input, board, checker):
    col_index = ord(column_input) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            break

def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == checker and row[col] == row[col+1] == row[col+2] == row[col+3]:
                return True
    
    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == checker and board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col]:
                return True

    # Check diagonal (down-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]:
                return True

    # Check diagonal (up-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]:
                return True

    return False

def is_board_full(board):
    return all(row[col] != " " for col in range(len(board[0])) for row in board)

def main():
    board = create_board(ROWS, COLS)
    players_checkers = CHECKERS[:PLAYERS]
    current_player = random.choice(players_checkers)

    while True:
        print_board(board)

        column_input = input(f"Player {current_player}, please enter a column: ").upper()

        if is_valid_input(column_input, board):
            place_checker(column_input, board, current_player)

            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break

            if is_board_full(board):
                print_board(board)
                print("It's a draw!")
                break

            current_player = players_checkers[(players_checkers.index(current_player) + 1) % PLAYERS]
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    main()
