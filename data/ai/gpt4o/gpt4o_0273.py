import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    header = "  " + "   ".join(LETTERS[:len(board[0])])
    separator = "+---" * len(board[0]) + "+"
    print(header)
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)

def is_valid_input(input, columns):
    return input in LETTERS[:columns]

def get_lowest_empty_row(board, column_index):
    for row_index in range(len(board)-1, -1, -1):
        if board[row_index][column_index] == " ":
            return row_index
    return -1

def place_checker(board, column_index, checker):
    row_index = get_lowest_empty_row(board, column_index)
    if row_index != -1:
        board[row_index][column_index] = checker
        return True
    return False

def check_for_win(board, player_checker):
    # Horizontal check
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == player_checker and row[col + 1] == player_checker and row[col + 2] == player_checker and row[col + 3] == player_checker:
                return True
    
    # Vertical check
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == player_checker and board[row + 1][col] == player_checker and board[row + 2][col] == player_checker and board[row + 3][col] == player_checker:
                return True

    # Diagonal check (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == player_checker and board[row + 1][col + 1] == player_checker and board[row + 2][col + 2] == player_checker and board[row + 3][col + 3] == player_checker:
                return True
    
    # Diagonal check (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == player_checker and board[row - 1][col + 1] == player_checker and board[row - 2][col + 2] == player_checker and board[row - 3][col + 3] == player_checker:
                return True
    
    return False

def check_for_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, PLAYERS - 1)
    current_checker = CHECKERS[current_player_index]

    clear_screen()
    print_board(board)
    
    while True:
        print(f"Player {current_checker}, please enter a column:")
        player_input = input().strip().upper()

        if not is_valid_input(player_input, COLUMNS):
            print("Invalid input. Try again.")
            continue

        column_index = LETTERS.index(player_input)
        
        if not place_checker(board, column_index, current_checker):
            print("Column full. Turn lost.")
            current_player_index = (current_player_index + 1) % PLAYERS
            current_checker = CHECKERS[current_player_index]
            continue

        clear_screen()
        print_board(board)

        if check_for_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if check_for_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS
        current_checker = CHECKERS[current_player_index]

play_game()
