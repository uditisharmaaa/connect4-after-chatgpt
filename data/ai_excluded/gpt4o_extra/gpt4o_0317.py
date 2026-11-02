import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
LETTERS = [chr(i) for i in range(ord('A'), ord('A') + COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(LETTERS))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def get_input(current_player):
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if column in LETTERS:
            index = LETTERS.index(column)
            if board[0][index] == " ":
                return index
        print("Invalid input, please enter a valid column.")

def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

def check_winner(board, checker):
    # Horizontal check
    for row in board:
        for col in range(COLUMNS - 3):
            if all(cell == checker for cell in row[col:col + 4]):
                return True
    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Diagonal checks
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Game setup
board = create_board()
current_player_index = random.choice(range(PLAYERS))
print_board(board)

# Game loop
while True:
    column = get_input(CHECKERS[current_player_index])
    drop_checker(board, column, CHECKERS[current_player_index])
    print_board(board)
    
    if check_winner(board, CHECKERS[current_player_index]):
        print(f"Player {CHECKERS[current_player_index]} won!")
        break
    if check_draw(board):
        print("The game is a draw!")
        break

    current_player_index = (current_player_index + 1) % PLAYERS
