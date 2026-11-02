import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(column_labels)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(column_letter, board):
    if len(column_letter) != 1 or not column_letter.isalpha():
        return False
    column_index = ord(column_letter.upper()) - ord('A')
    if column_index < 0 or column_index >= COLUMNS or board[0][column_index] != " ":
        return False
    return True

def place_checker(column_letter, checker, board):
    column_index = ord(column_letter.upper()) - ord('A')
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            break

def check_for_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    return False

def check_for_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    board = initialize_board(ROWS, COLUMNS)
    player_checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(list(range(NUM_PLAYERS)))

    while True:
        print_board(board)
        player_checker = player_checkers[current_player]
        print(f"Player {player_checker}, please enter a column:")
        column_letter = input().strip()
        
        while not is_valid_input(column_letter, board):
            print("Invalid input. Please enter a valid column letter:")
            column_letter = input().strip()
        
        place_checker(column_letter, player_checker, board)

        if check_for_win(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break
        
        if check_for_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
