import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_COUNT = NUM_PLAYERS

def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(COLS))
    print(column_labels)
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def get_player_choice(player):
    choice = input(f"Player {player}, please enter a column: ").upper()
    while not (len(choice) == 1 and 'A' <= choice < chr(65 + COLS)):
        choice = input(f"Invalid column! Player {player}, please enter a column: ").upper()
    return choice

def place_checker(board, column, checker):
    col_idx = ord(column) - 65
    for row_idx in range(ROWS-1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    players = CHECKERS[:PLAYER_COUNT]
    current_player_idx = random.randint(0, PLAYER_COUNT - 1)
    print_board(board)

    while True:
        current_player = players[current_player_idx]
        column_choice = get_player_choice(current_player)
        
        if not place_checker(board, column_choice, current_player):
            print("Column full! Turn lost.")
        else:
            print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYER_COUNT

main()
