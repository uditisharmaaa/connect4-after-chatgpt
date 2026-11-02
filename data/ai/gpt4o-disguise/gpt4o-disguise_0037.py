import random
import os

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(i + ord('A')) for i in range(COLS)))
    print("+---" * COLS + "+")
    for r in board:
        print("| " + " | ".join(r) + " |")
        print("+---" * COLS + "+")

def get_player_input(current_player):
    while True:
        col_choice = input(f"Player {CHECKERS[current_player]}, please enter a column: ").upper()
        if len(col_choice) == 1 and 'A' <= col_choice <= chr(ord('A') + COLS - 1):
            col_num = ord(col_choice) - ord('A')
            if board[0][col_num] == " ":
                return col_num
        print("Invalid input. Try again.")

def place_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            break

def check_for_win(board, checker):
    def check_direction(dx, dy):
        for row in range(ROWS):
            for col in range(COLS):
                if all(0 <= row + k*dy < ROWS and 0 <= col + k*dx < COLS and board[row + k*dy][col + k*dx] == checker for k in range(4)):
                    return True
        return False
    
    return check_direction(1, 0) or check_direction(0, 1) or check_direction(1, 1) or check_direction(1, -1)

def check_for_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

board = create_board()
current_player = random.randint(0, PLAYERS - 1)
print_board(board)

while True:
    col_choice = get_player_input(current_player)
    place_checker(board, col_choice, CHECKERS[current_player])
    print_board(board)

    if check_for_win(board, CHECKERS[current_player]):
        print(f"Player {CHECKERS[current_player]} won!")
        break
    elif check_for_draw(board):
        print("The game is a draw.")
        break

    current_player = (current_player + 1) % PLAYERS
