import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Maximum 5 players

def initialize_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    line = "+---" * COLUMNS + "+"
    print(header)
    print(line)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print(line)

def get_valid_input():
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if user_input.isalpha() and len(user_input) == 1 and ord(user_input) - 65 < COLUMNS:
            return ord(user_input) - 65
        print("Invalid input. Please enter a valid column.")

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_winner(board, player_checker):
    def check_line(line):
        return any(
            line[i:i+4] == [player_checker]*4
            for i in range(len(line) - 3)
        )

    for row in board:
        if check_line(row):
            return True

    for col in range(COLUMNS):
        if check_line([board[row][col] for row in range(ROWS)]):
            return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if [board[row+i][col+i] for i in range(4)] == [player_checker]*4:
                return True

        for col in range(COLUMNS - 3):
            if [board[row+3-i][col+i] for i in range(4)] == [player_checker]*4:
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    board = initialize_board(ROWS, COLUMNS)
    game_over = False
    player_turn = random.randint(0, PLAYERS - 1)
    while not game_over:
        print_board(board)
        print(f"Player {CHECKERS[player_turn]}, it's your turn.")
        column = get_valid_input()
        if place_checker(board, column, CHECKERS[player_turn]):
            if check_winner(board, CHECKERS[player_turn]):
                print_board(board)
                print(f"Player {CHECKERS[player_turn]} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("The game is a draw!")
                game_over = True
            else:
                player_turn = (player_turn + 1) % PLAYERS
        else:
            print("Column is full! You lost your turn.")

if __name__ == "__main__":
    play_game()
