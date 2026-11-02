import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Supports up to 5 players

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Clear screen before printing
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print('  ' + '   '.join(letters[:COLUMNS]))
    print('+' + '---+' * COLUMNS)
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '---+' * COLUMNS)

def player_input():
    while True:
        col = input("Player {}, please enter a column: ".format(player_symbols[current_player]))
        if col.upper() in valid_inputs and board[0][ord(col.upper()) - 65] == ' ':
            return ord(col.upper()) - 65
        print("Invalid input, try again.")

def place_checker(col, symbol):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row, col

def check_winner(row, col):
    def check_direction(dx, dy):
        count = 0
        for d in range(-3, 4):
            r, c = row + d * dy, col + d * dx
            if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_symbols[current_player]:
                count += 1
            else:
                count = 0
            if count >= 4:
                return True
        return False

    return (check_direction(1, 0) or   # Horizontal
            check_direction(0, 1) or   # Vertical
            check_direction(1, 1) or   # Diagonal ascending
            check_direction(1, -1))    # Diagonal descending

def check_draw():
    return all(board[0][c] != ' ' for c in range(COLUMNS))

# Initialize game state
board = create_board(ROWS, COLUMNS)
player_symbols = CHECKERS[:PLAYERS]
valid_inputs = [chr(65 + i) for i in range(COLUMNS)]

# Randomly choose first player
current_player = random.randint(0, PLAYERS - 1)

# Print initial board
print_board(board)

# Game loop
while True:
    col = player_input()
    row, col = place_checker(col, player_symbols[current_player])
    print_board(board)
    if check_winner(row, col):
        print("Player {} won!".format(player_symbols[current_player]))
        break
    if check_draw():
        print("The game is a draw!")
        break
    current_player = (current_player + 1) % PLAYERS
