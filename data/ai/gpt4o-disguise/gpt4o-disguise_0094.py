import os
import random

def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    print("  A   B   C   D   E   F   G")
    print("+---+---+---+---+---+---+---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+---+---+---+---+---+---+")

def init_board(cols, rows):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def valid_input(input, cols):
    if len(input) != 1:
        return False
    if not (ord('A') <= ord(input) < ord('A') + cols):
        return False
    return True

def find_row(board, col):
    for i in range(len(board)-1, -1, -1):
        if board[i][col] == " ":
            return i
    return -1

def place_checker(board, col, checker):
    row = find_row(board, col)
    if row == -1:
        return False
    board[row][col] = checker
    return True

def check_win(board, rows, cols, curr_checker):
    for row in range(rows):
        for col in range(cols):
            if check_direction(board, row, col, curr_checker, 1, 0) or check_direction(board, row, col, curr_checker, 0, 1) or check_direction(board, row, col, curr_checker, 1, 1) or check_direction(board, row, col, curr_checker, 1, -1):
                return True
    return False

def check_direction(board, row, col, checker, delta_row, delta_col):
    for step in range(4):
        new_row = row + step * delta_row
        new_col = col + step * delta_col
        if new_row >= len(board) or new_col >= len(board[0]) or new_row < 0 or new_col < 0 or board[new_row][new_col] != checker:
            return False
    return True

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    cols, rows = 7, 6
    board = init_board(cols, rows)
    players = ["X", "O"]
    current_player = random.choice(players)
    game_on = True

    print_board(board)
    while game_on:
        print(f"Player {current_player}, please enter a column:")
        user_input = input().strip()
        if not valid_input(user_input, cols):
            continue
        col = ord(user_input) - ord('A')
        if not place_checker(board, col, current_player):
            continue
        print_board(board)

        if check_win(board, rows, cols, current_player):
            print(f"Player {current_player} won!")
            game_on = False
        elif check_draw(board):
            print("Game is a draw!")
            game_on = False
        else:
            current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    main()
