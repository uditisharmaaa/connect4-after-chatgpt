import os
import random

# Global constants
BOARD_ROWS = 6
BOARD_COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
NUMBER_OF_PLAYERS = 2

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    headers = "  " + "   ".join(chr(65 + i) for i in range(len(board[0]))) + "  "
    print(headers)
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(row) + "+")

def is_valid_input(user_input, columns):
    return len(user_input) == 1 and user_input.isalpha() and 'A' <= user_input <= chr(65 + columns - 1)

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_for_winner(board, checker):
    rows, columns = len(board), len(board[0])

    # Check horizontal
    for row in range(rows):
        for col in range(columns - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(columns):
        for row in range(rows - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, rows):
        for col in range(columns - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal \
    for row in range(rows - 3):
        for col in range(columns - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(BOARD_ROWS, BOARD_COLUMNS)
    current_player_index = random.randint(0, NUMBER_OF_PLAYERS - 1)
    
    while True:
        clear_screen()
        print_board(board)
        current_checker = PLAYER_CHECKERS[current_player_index]
        user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()

        while not is_valid_input(user_input, BOARD_COLUMNS):
            user_input = input("Invalid input. Please enter a valid column: ").strip().upper()

        column_index = ord(user_input) - 65
        if place_checker(board, column_index, current_checker):
            if check_for_winner(board, current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                break
            elif check_for_draw(board):
                clear_screen()
                print_board(board)
                print("The game is a draw!")
                break
            current_player_index = (current_player_index + 1) % NUMBER_OF_PLAYERS
        else:
            print("Column is full, turn is lost.")

if __name__ == "__main__":
    main()
