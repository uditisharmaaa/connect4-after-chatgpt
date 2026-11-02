import os
import random
import string

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4  # Number of checkers in a row for a win

def clear_screen():
    os.system('clear')

def create_board(rows=ROWS, cols=COLS):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers
    header = "  "
    for i in range(cols):
        header += "  " + string.ascii_uppercase[i] + " "
    print(header)
    # Print board with separators
    row_separator = "+" + "---+" * cols
    for row in board:
        print(row_separator)
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    print(row_separator)

def valid_column_input(user_input, board):
    if len(user_input) != 1:
        return False
    letter = user_input.upper()
    if letter < 'A' or letter >= chr(ord('A') + len(board[0])):
        return False
    col_index = ord(letter) - ord('A')
    # Check if column is full
    if board[0][col_index] != " ":
        return False
    return True

def place_checker(board, col_letter, checker):
    col = ord(col_letter.upper()) - ord('A')
    # Place checker in the lowest empty spot in the column
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Should never get here if input validated correctly,
    # but returns None if column is full (loses turn)
    return None

def check_win(board, r, c, checker):
    rows = len(board)
    cols = len(board[0])

    def count_direction(dr, dc):
        count = 0
        rr, cc = r + dr, c + dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc
        return count

    # directions pairs: horizontal, vertical, diagonal /, diagonal \
    directions = [ (0,1), (1,0), (1,1), (1,-1) ]

    for dr, dc in directions:
        total = 1  # counting current position
        total += count_direction(dr, dc)
        total += count_direction(-dr, -dc)
        if total >= WIN_COUNT:
            return True
    return False

def board_full(board):
    return all(cell != " " for cell in board[0])

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS -1)

    print_board(board)
    print(f"Player {players[current_player_idx]} starts first!")

    while True:
        player_checker = players[current_player_idx]
        prompt = f"Player {player_checker}, please enter a column: "

        # Input validation loop
        while True:
            user_input = input(prompt).strip().upper()
            if not valid_column_input(user_input, board):
                # Check if input is a letter in range to handle full columns specifically
                if len(user_input) == 1 and 'A' <= user_input <= chr(ord('A') + COLS - 1):
                    # Column is full, player loses turn (skip input again)
                    # Announce losing turn
                    print(f"Column {user_input} is full. Player {player_checker} loses the turn.")
                    break
                else:
                    print("Invalid input. Please enter a valid non-full column letter (A-G).")
            else:
                break

        # If input invalid due to full column, skip turn
        if len(user_input) == 1 and 'A' <= user_input <= chr(ord('A') + COLS - 1) and not valid_column_input(user_input, board):
            # lose turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            if board_full(board):
                print("Draw! The board is full.")
                break
            continue

        if not valid_column_input(user_input, board):
            # This means input wasn't a valid column (e.g. 'Z' or invalid string),
            # This case handled above already by looping for input again, here just continue
            continue

        # Place checker now
        position = place_checker(board, user_input, player_checker)
        if position is None:
            # Should never happen if validation above is correct
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            if board_full(board):
                print("Draw! The board is full.")
                break
            continue

        print_board(board)

        r, c = position

        if check_win(board, r, c, player_checker):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("Draw! The board is full.")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
