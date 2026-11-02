import random
import os

ROWS = 6
COLS = 7
PLAYER_COUNT = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']
board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')
    print("  " + "   ".join(chr(i) for i in range(ord('A'), ord('A') + COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def valid_input(input):
    return len(input) == 1 and input.isalpha() and 'A' <= input <= chr(ord('A') + COLS - 1)

def make_move(player, column):
    col_index = ord(column) - ord('A')
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = player
            return True
    return False

def check_win(player):
    for row in range(ROWS):
        for col in range(COLS):
            if (col <= COLS - 4 and all(board[row][col + i] == player for i in range(4))) or \
               (row <= ROWS - 4 and all(board[row + i][col] == player for i in range(4))) or \
               (row <= ROWS - 4 and col <= COLS - 4 and all(board[row + i][col + i] == player for i in range(4))) or \
               (row >= 3 and col <= COLS - 4 and all(board[row - i][col + i] == player for i in range(4))):
                return True
    return False

def check_draw():
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    current_player = random.choice(PLAYERS[:PLAYER_COUNT])
    print_board()
    while True:
        print(f"Player {current_player}, please enter a column:")
        user_input = input().strip().upper()
        if not valid_input(user_input):
            print("Invalid input. Please enter a valid column.")
            continue
        if not make_move(current_player, user_input):
            print("Column full. Turn lost.")
        else:
            print_board()
            if check_win(current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw():
                print("It's a draw!")
                break
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % PLAYER_COUNT]

play_game()
