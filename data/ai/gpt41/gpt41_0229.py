import os
import random

# ==== Constants (change these for other configurations) ====
ROWS = 6
COLUMNS = 7   # Max 26 (A-Z)
PLAYERS = 2   # 2-5 players allowed
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

# ==== Utility Functions ====
def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    col_labels = [chr(ord('A') + i) for i in range(COLUMNS)]
    print("  " + "   ".join(col_labels))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_column_from_input(inp):
    if len(inp) != 1 or not inp.isalpha():
        return -1
    col = ord(inp.upper()) - ord('A')
    if 0 <= col < COLUMNS:
        return col
    else:
        return -1

def place_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column is full

def is_full(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True

def check_win(board, row, col, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for sign in [-1, 1]:
            r, c = row + sign*dr, col + sign*dc
            while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
                r += sign*dr
                c += sign*dc
    return False

# ==== Main Game ====
def main():
    board = create_board()
    player_turn = random.randint(0, PLAYERS - 1)
    clear_screen()
    print_board(board)
    while True:
        checker = CHECKERS[player_turn]
        print(f"Player {checker}, please enter a column:")
        inp = input().strip().upper()

        col = get_column_from_input(inp)
        if col == -1:
            print("Invalid input. Please enter a valid column letter.")
            continue

        if board[0][col] != " ":
            print("Column full. You lose your turn.")
            player_turn = (player_turn + 1) % PLAYERS
            clear_screen()
            print_board(board)
            continue

        row = place_checker(board, col, checker)

        clear_screen()
        print_board(board)

        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break

        if is_full(board):
            print("The game is a draw!")
            break

        player_turn = (player_turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
