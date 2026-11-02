import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(labels))
    for row in board:
        print("+" + "---+" * len(row))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * len(board[0]))

def is_valid_column(input_col, cols):
    if len(input_col) != 1:
        return False
    col_upper = input_col.upper()
    if not ('A' <= col_upper <= chr(ord('A') + cols -1)):
        return False
    return True

def get_column_index(column_letter):
    return ord(column_letter.upper()) - ord('A')

def place_checker(board, col_idx, checker):
    # Place the checker at the lowest empty spot in the column
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    # Column full
    return None

def check_direction(board, start_row, start_col, d_row, d_col, checker):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] == checker:
        count += 1
        row += d_row
        col += d_col
    return count

def check_win(board, row, col, checker):
    # Check horizontal
    count = 1
    count += check_direction(board, row, col -1, 0, -1, checker)
    count += check_direction(board, row, col +1, 0, 1, checker)
    if count >= WIN_LENGTH:
        return True

    # Check vertical
    count = 1
    count += check_direction(board, row -1, col, -1, 0, checker)
    count += check_direction(board, row +1, col, 1, 0, checker)
    if count >= WIN_LENGTH:
        return True

    # Check diagonal /
    count = 1
    count += check_direction(board, row -1, col +1, -1, 1, checker)
    count += check_direction(board, row +1, col -1, 1, -1, checker)
    if count >= WIN_LENGTH:
        return True

    # Check diagonal \
    count = 1
    count += check_direction(board, row -1, col -1, -1, -1, checker)
    count += check_direction(board, row +1, col +1, 1, 1, checker)
    if count >= WIN_LENGTH:
        return True

    return False

def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "

        # Input validation loop
        while True:
            user_input = input(prompt).strip()
            if not is_valid_column(user_input, COLS):
                print(f"Invalid input. Please enter a letter from A to {chr(ord('A') + COLS -1)}.")
                continue
            col_idx = get_column_index(user_input)
            placed_pos = place_checker(board, col_idx, current_checker)
            if placed_pos is None:
                # Column full, player loses turn
                # According to spec: "If the column is already completely filled with checkers, the turn is invalid and the player loses the turn."
                # So we do not retry input, just skip to next player
                print(f"Column {user_input.upper()} is full. Turn lost.")
                placed_pos = None
                break
            else:
                break

        print_board(board)

        if placed_pos is not None:
            r, c = placed_pos
            if check_win(board, r, c, current_checker):
                print(f"Player {current_checker} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break

        # Move to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
