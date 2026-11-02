import os
import random

ROWS, COLS = 6, 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

def is_valid_column(col, board):
    if col < 0 or col >= COLS or board[0][col] != ' ':
        return False
    return True

def place_checker(col, checker, board):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            break

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if all(board[r][c+i] == checker for i in range(4) if c+i < COLS):
                return True
            if all(board[r+i][c] == checker for i in range(4) if r+i < ROWS):
                return True
            if all(board[r+i][c+i] == checker for i in range(4) if r+i < ROWS and c+i < COLS):
                return True
            if all(board[r-i][c+i] == checker for i in range(4) if r-i >= 0 and c+i < COLS):
                return True
    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board(ROWS, COLS)
    player_checkers = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        print(f"Player {player_checkers[current_player]}, please enter a column: ", end='')
        while True:
            col_input = input().upper()
            if len(col_input) == 1 and col_input.isalpha():
                col = ord(col_input) - 65
                if is_valid_column(col, board):
                    break
            print("Invalid input, please try again: ", end='')

        place_checker(col, player_checkers[current_player], board)
        print_board(board)

        if check_win(board, player_checkers[current_player]):
            print(f"Player {player_checkers[current_player]} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

main()
