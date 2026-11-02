import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    print(" ", end=" ")
    for label in COLUMN_LABELS:
        print(f" {label} ", end=" ")
    print()
    # Print board rows
    for row in board:
        print("+" + "---+" * COLUMNS)
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+" + "---+" * COLUMNS)

def get_valid_column(player):
    while True:
        col_input = input(f"Player {player}, please enter a column: ").upper()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        if col_input not in COLUMN_LABELS:
            print("Invalid column. Please enter a valid column letter.")
            continue
        col = COLUMN_LABELS.index(col_input)
        return col

def place_checker(board, col, checker):
    # place checker in the lowest available row in the given column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    # Column full
    return False

def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_CONDITION + 1):
            count = 0
            for i in range(WIN_CONDITION):
                if board[row][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_CONDITION:
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_CONDITION + 1):
            count = 0
            for i in range(WIN_CONDITION):
                if board[row + i][col] == checker:
                    count += 1
                else:
                    break
            if count == WIN_CONDITION:
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - WIN_CONDITION + 1):
        for col in range(COLUMNS - WIN_CONDITION + 1):
            count = 0
            for i in range(WIN_CONDITION):
                if board[row + i][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_CONDITION:
                return True

    # Check diagonal (up-right)
    for row in range(WIN_CONDITION - 1, ROWS):
        for col in range(COLUMNS - WIN_CONDITION + 1):
            count = 0
            for i in range(WIN_CONDITION):
                if board[row - i][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_CONDITION:
                return True

    return False

def check_draw(board):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True

def main():
    board = create_board()
    num_players = MAX_PLAYERS
    players = CHECKERS[:num_players]
    current_player_index = random.randint(0, num_players -1)

    print_board(board)

    while True:
        player_checker = players[current_player_index]
        col = get_valid_column(player_checker)
        if not place_checker(board, col, player_checker):
            print("Column full! You lose your turn.")
        else:
            print_board(board)
            if check_winner(board, player_checker):
                print(f"Player {player_checker} won!")
                break
            if check_draw(board):
                print("Game is a draw!")
                break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
