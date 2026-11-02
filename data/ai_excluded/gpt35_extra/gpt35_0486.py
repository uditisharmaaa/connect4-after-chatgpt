import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = "  "
    for i in range(COLUMNS):
        headers += chr(ord('A') + i) + "   "
    print(headers.rstrip())
    # Print rows
    separator = "+" + "---+" * COLUMNS
    for row in range(ROWS):
        print(separator)
        line = "|"
        for col in range(COLUMNS):
            line += " " + board[row][col] + " |"
        print(line)
    print(separator)

def is_valid_column(col):
    return 0 <= col < COLUMNS

def column_not_full(board, col):
    return board[0][col] == " "

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None  # Column full

def check_winner(board, checker):
    # Horizontal check
    for r in range(ROWS):
        count = 0
        for c in range(COLUMNS):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0
    # Vertical check
    for c in range(COLUMNS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0
    # Diagonal checks
    # Down-right
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLUMNS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r + i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True
    # Down-left
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(WIN_COUNT - 1, COLUMNS):
            count = 0
            for i in range(WIN_COUNT):
                if board[r + i][c - i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True
    return False

def board_full(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True

def get_player_input(player_checker):
    prompt = f"Player {player_checker}, please enter a column: "
    while True:
        inp = input(prompt).strip()
        if len(inp) != 1 or not ('A' <= inp <= chr(ord('A') + COLUMNS -1)):
            # Invalid length or not a valid column letter
            continue
        col = ord(inp) - ord('A')
        return col

def main():
    board = create_board()
    current_player_index = random.randint(0, PLAYERS -1)
    player_checkers = CHECKERS[:PLAYERS]

    print_board(board)

    while True:
        player_checker = player_checkers[current_player_index]
        col = get_player_input(player_checker)

        if not is_valid_column(col):
            # Invalid column letter (should not happen due to input check, but just in case)
            continue

        if not column_not_full(board, col):
            # Column full, lose turn
            current_player_index = (current_player_index + 1) % PLAYERS
            continue

        row = get_next_open_row(board, col)
        board[row][col] = player_checker

        print_board(board)

        if check_winner(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("The game is a draw.")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
