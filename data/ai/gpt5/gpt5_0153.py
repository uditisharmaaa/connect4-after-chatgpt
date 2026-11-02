import os
import random
import string

# Constants (submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
TOKENS = ["X", "O", "V", "H", "M"]  # in order

WIN_LENGTH = 4  # always 4 in a row to win

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])
    letters = list(string.ascii_uppercase[:cols])

    # Column headers
    header = "  " + "   ".join(letters)
    print(header)
    # Horizontal separator
    sep = "+" + "+".join(["---"] * cols) + "+"
    # Rows
    for r in range(rows):
        print(sep)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(sep)

def get_player_tokens(num_players):
    return TOKENS[:num_players]

def is_valid_column_input(inp, cols):
    if len(inp) != 1:
        return False
    if inp < 'A' or inp > 'Z':
        return False
    index = ord(inp) - ord('A')
    return 0 <= index < cols

def drop_checker(board, col_index, token):
    # Place token in the lowest available row in col_index
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = token
            return True
    return False  # column full

def check_win(board, token):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1)   # down-left
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == token and count < WIN_LENGTH:
                    count += 1
                    rr += dr
                    cc += dc
                if count >= WIN_LENGTH:
                    return True
    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    # Safety checks
    if COLS > 26:
        print("Maximum supported columns is 26.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        return

    board = create_board(ROWS, COLS)
    players = get_player_tokens(NUM_PLAYERS)
    current = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        token = players[current]
        # Prompt for input, ensure valid letter input
        user_input = ""
        while True:
            print(f"Player {token}, please enter a column:")
            user_input = input().strip().upper()
            if is_valid_column_input(user_input, COLS):
                break
            else:
                clear_screen()
                print_board(board)
                print("Invalid input. Please enter a valid column letter.")

        col_index = ord(user_input) - ord('A')

        # Try to drop checker
        placed = drop_checker(board, col_index, token)

        # Always clear and print after the attempt
        clear_screen()
        print_board(board)

        if not placed:
            print(f"Column {user_input} is full. Turn lost.")
            # Move to next player
            current = (current + 1) % NUM_PLAYERS
            # Continue to next turn
            # (No win/draw check since board didn't change)
            continue

        # Check for win
        if check_win(board, token):
            print(f"Player {token} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
