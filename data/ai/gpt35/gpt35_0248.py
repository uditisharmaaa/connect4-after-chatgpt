import os
import random

# Constants
ROWS = 6            # Number of rows
COLUMNS = 7         # Number of columns (max 26)
NUM_PLAYERS = 2     # Number of players (2-5)
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS))
    print(header)
    # Print board rows with separators
    sep = "+" + "---+"*COLUMNS
    for row in range(ROWS):
        print(sep)
        line = "|"
        for col in range(COLUMNS):
            line += " " + board[row][col] + " |"
        print(line)
    print(sep)

def valid_column_input(user_input):
    if len(user_input) != 1:
        return False
    c = user_input.upper()
    if 'A' <= c <= chr(ord('A') + COLUMNS - 1):
        return True
    return False

def get_column_index(user_input):
    return ord(user_input.upper()) - ord('A')

def place_checker(board, col, checker):
    # Start from bottom row to top
    for r in reversed(range(ROWS)):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None  # Column full

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    r, c = start_row, start_col
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col
    return count

def check_win(board, row, col, checker):
    # Check all directions for 4 in a row including the placed checker
    directions = [
        ((0, 1), (0, -1)),     # horizontal right, left
        ((1, 0), (-1, 0)),     # vertical down, up
        ((1, 1), (-1, -1)),    # diagonal down-right, up-left
        ((1, -1), (-1, 1))     # diagonal down-left, up-right
    ]
    for (d1, d2) in directions:
        count = 1  # count the placed checker itself
        count += check_direction(board, row + d1[0], col + d1[1], d1[0], d1[1], checker)
        count += check_direction(board, row + d2[0], col + d2[1], d2[0], d2[1], checker)
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    print_board(board)  # Show initially empty board
    while not game_over:
        checker = players[current_player_index]
        prompt = f"Player {checker}, please enter a column: "
        while True:
            user_input = input(prompt).strip()
            if not valid_column_input(user_input):
                continue
            col = get_column_index(user_input)
            placement = place_checker(board, col, checker)
            if placement is None:
                # column full - turn lost
                break
            row, col = placement
            break
        # if placement is None, turn lost – skip win check and move to next player
        if placement is None:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            game_over = True
            continue
        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            game_over = True
            continue

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
