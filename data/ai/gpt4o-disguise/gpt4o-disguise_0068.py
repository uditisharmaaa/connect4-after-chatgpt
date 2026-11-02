import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    print("\n  " + "   ".join([chr(c) for c in range(65, 65 + COLUMNS)]))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_valid_column(board):
    while True:
        col_input = input("Please enter a column: ").upper()
        if col_input.isalpha() and len(col_input) == 1:
            col_num = ord(col_input) - 65
            if 0 <= col_num < COLUMNS and board[0][col_num] == ' ':
                return col_num
        print("Invalid input. Try again.")

def drop_checker(board, col, checker):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == ' ':
            board[i][col] = checker
            break

def check_four_in_row(board, player):
    # Horizontal Check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col:col + 4].count(player) == 4:
                return True
    # Vertical Check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if [board[row + i][col] for i in range(4)].count(player) == 4:
                return True
    # Diagonal Checks
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if [board[row + i][col + i] for i in range(4)].count(player) == 4:
                return True
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if [board[row - i][col + i] for i in range(4)].count(player) == 4:
                return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player_index]}'s turn.")
        col = get_valid_column(board)
        drop_checker(board, col, CHECKERS[current_player_index])

        clear_screen()
        print_board(board)

        if check_four_in_row(board, CHECKERS[current_player_index]):
            print(f"Player {CHECKERS[current_player_index]} won!")
            break
        elif check_draw(board):
            print("Game is a draw!")
            break
        current_player_index = (current_player_index + 1) % PLAYERS

play_game()
