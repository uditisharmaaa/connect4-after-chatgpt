import os
import random

# CONSTANTS
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers A-G (or more if needed)
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(headers)
    # Print the board with separators
    sep = "+" + "---+" * len(board[0])
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)

def input_to_col(user_input):
    user_input = user_input.strip().upper()
    if len(user_input) != 1:
        return None
    col = ord(user_input) - ord('A')
    if 0 <= col < COLS:
        return col
    return None

def valid_move(board, col):
    # A move is valid if column in range and has at least one empty cell
    if col is None or not (0 <= col < COLS):
        return False
    return board[0][col] == " "

def place_checker(board, col, checker):
    """
    Places a checker in the lowest available row in the given column.
    Returns True if placed successfully, False if column full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r][c+i] == checker for i in range(WIN_COUNT)):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - WIN_COUNT + 1):
            if all(board[r+i][c] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal down-right check
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal down-left check
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(WIN_COUNT - 1, COLS):
            if all(board[r+i][c-i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def check_draw(board):
    # Draw if top row is full (i.e. no empty space in any column)
    return all(cell != " " for cell in board[0])

def next_player_index(current_index):
    return (current_index + 1) % NUM_PLAYERS

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    while True:
        checker = players[current_player_index]
        prompt = f"Player {checker}, please enter a column: "

        col = None
        lost_turn = False
        while True:
            user_input = input(prompt)
            col = input_to_col(user_input)
            if col is None:
                # invalid input, ask again
                continue
            if not valid_move(board, col):
                # column full -> lose turn
                lost_turn = True
                break
            else:
                # valid move
                break

        if lost_turn:
            # lose turn silently (per spec)
            current_player_index = next_player_index(current_player_index)
            print_board(board)
            continue

        place_checker(board, col, checker)
        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print("The game is a draw.")
            break

        current_player_index = next_player_index(current_player_index)

if __name__ == "__main__":
    main()
