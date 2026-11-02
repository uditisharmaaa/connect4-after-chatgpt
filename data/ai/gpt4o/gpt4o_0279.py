import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYER_COUNT]
COLUMN_NAMES = [chr(c) for c in range(ord('A'), ord('A') + COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(COLUMN_NAMES))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_random_player():
    return random.choice(range(PLAYER_COUNT))

def is_valid_input(input_char):
    return input_char in COLUMN_NAMES

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_for_win(board, checker):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == checker:
                if check_direction(board, r, c, checker, 0, 1) or \
                   check_direction(board, r, c, checker, 1, 0) or \
                   check_direction(board, r, c, checker, 1, 1) or \
                   check_direction(board, r, c, checker, 1, -1):
                    return True
    return False

def check_direction(board, r, c, checker, dr, dc):
    count = 0
    for i in range(4):
        rr, cc = r + dr * i, c + dc * i
        if 0 <= rr < ROWS and 0 <= cc < COLUMNS and board[rr][cc] == checker:
            count += 1
    return count == 4

def check_for_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    board = create_board()
    current_player_index = get_random_player()
    print_board(board)
    while True:
        player_checker = CHECKERS[current_player_index]
        while True:
            player_input = input(f"Player {player_checker}, please enter a column: ").upper()
            if is_valid_input(player_input):
                column_index = COLUMN_NAMES.index(player_input)
                if place_checker(board, column_index, player_checker):
                    break
                else:
                    print("Column is full, try another column.")
            else:
                print("Invalid input, try again.")
        
        print_board(board)
        
        if check_for_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        if check_for_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % PLAYER_COUNT

if __name__ == "__main__":
    play_game()
