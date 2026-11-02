import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS_COUNT = 2  # Must be between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]  # up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column labels A-G
    labels = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(labels)
    for row in board:
        print("+" + "---+"*cols)
        print("| " + " | ".join(row) + " |")
    print("+" + "---+"*cols)

def is_valid_column(input_str, cols):
    if len(input_str) != 1:
        return False
    letter = input_str[0]
    if letter < 'A' or letter >= chr(ord('A') + cols):
        return False
    return True

def column_index(letter):
    return ord(letter) - ord('A')

def place_checker(board, col_idx, checker):
    # Place checker in the lowest available row in col_idx
    for row_idx in range(len(board)-1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    return -1, -1  # column full

def check_four_in_a_row(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    rows = len(board)
    cols = len(board[0])
    while 0 <= row < rows and 0 <= col < cols and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count

def has_won(board, row, col, checker):
    # Check all directions from the newly placed checker:
    # Horizontal (left and right), Vertical (up and down),
    # Diagonal (two directions)
    directions = [
        ((0, -1), (0, 1)),      # horizontal
        ((-1, 0), (1, 0)),      # vertical
        ((-1, -1), (1, 1)),     # diagonal top-left to bottom-right
        ((-1, 1), (1, -1)),     # diagonal top-right to bottom-left
    ]
    for dir1, dir2 in directions:
        count1 = check_four_in_a_row(board, row, col, dir1[0], dir1[1], checker) - 1
        count2 = check_four_in_a_row(board, row, col, dir2[0], dir2[1], checker) - 1
        # include the placed checker itself (+1), so total is:
        total = count1 + count2 + 1
        if total >= 4:
            return True
    return False

def board_full(board):
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    return True

def get_next_player_idx(current_idx, players_count):
    return (current_idx + 1) % players_count

def main():
    # Validate PLAYERS_COUNT in allowed range
    if PLAYERS_COUNT < 2 or PLAYERS_COUNT > 5:
        print("Error: Number of players must be between 2 and 5.")
        return

    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS_COUNT]

    current_player_idx = random.randint(0, PLAYERS_COUNT -1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        input_prompt = f"Player {current_checker}, please enter a column: "
        while True:
            user_input = input(input_prompt).strip().upper()
            if not is_valid_column(user_input, COLUMNS):
                print(f"Invalid input. Please enter a letter between A and {chr(ord('A')+COLUMNS-1)}.")
                continue
            col = column_index(user_input)
            placed_row, placed_col = place_checker(board, col, current_checker)
            if placed_row == -1:
                # column full: turn lost
                break  # end input loop, move to next player
            else:
                # valid move placed
                break

        print_board(board)

        if placed_row != -1:
            # check win
            if has_won(board, placed_row, placed_col, current_checker):
                print(f"Player {current_checker} won!")
                break
            # check draw
            if board_full(board):
                print("The game is a draw!")
                break

        current_player_idx = get_next_player_idx(current_player_idx, PLAYERS_COUNT)

if __name__ == "__main__":
    main()
