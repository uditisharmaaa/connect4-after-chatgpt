import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
players = CHECKERS[:PLAYERS]
current_player = random.choice(players)

def print_board():
    os.system('clear')
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_column(letter):
    return ord(letter.upper()) - 65

def is_valid_column(col):
    return 0 <= col < COLS and board[0][col] == ' '

def place_checker(col, player):
    for i in range(ROWS-1, -1, -1):
        if board[i][col] == ' ':
            board[i][col] = player
            break

def check_win(player):
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == player for i in range(4)):
                return True
    
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row+i][col] == player for i in range(4)):
                return True
    
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True
    
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True
    
    return False

def check_draw():
    return all(board[0][col] != ' ' for col in range(COLS))

print_board()
while True:
    col = None
    while col is None:
        input_col = input(f"Player {current_player}, please enter a column: ")
        if len(input_col) == 1 and input_col.isalpha():
            col = get_column(input_col)
            if not is_valid_column(col):
                col = None
    
    place_checker(col, current_player)
    print_board()
    
    if check_win(current_player):
        print(f"Player {current_player} won!")
        break
    elif check_draw():
        print("The game is a draw!")
        break
    
    current_player = players[(players.index(current_player) + 1) % PLAYERS]
