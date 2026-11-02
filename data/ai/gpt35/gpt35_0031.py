import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers
    headers = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(headers)
    # Print horizontal separators and rows
    for row in board:
        print("+" + "---+" * cols)
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * cols)

def is_valid_column(input_str, cols):
    if len(input_str) != 1:
        return False
    if input_str not in string.ascii_uppercase[:cols]:
        return False
    return True

def column_index_from_letter(letter):
    return string.ascii_uppercase.index(letter)

def is_column_full(board, col_idx):
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    # Place checker in the lowest available position in the column
    for row_idx in reversed(range(len(board))):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    # Column full
    return None

def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_direction(delta_row, delta_col):
        count = 0
        r, c = row + delta_row, col + delta_col
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += delta_row
            c += delta_col
        return count

    # Directions: horizontal, vertical, diagonal /
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # count includes the placed checker itself
        count += count_direction(dr, dc)
        count += count_direction(-dr, -dc)
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    # If the top row has any empty space, board not full
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def main():
    rows = ROWS
    cols = COLUMNS
    players_count = 2  # set to 2 players as per submission instructions
    checkers = PLAYERS[:players_count]

    board = create_board(rows, cols)
    current_player_idx = random.randint(0, players_count - 1)

    while True:
        print_board(board)
        current_checker = checkers[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "

        # Input validation loop
        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_column(user_input, cols):
                print("Invalid input. Please enter a valid column letter.")
                continue
            col = column_index_from_letter(user_input)
            if is_column_full(board, col):
                # Player loses turn if column full (print notification)
                print(f"Column {user_input} is full. You lose your turn.")
                break
            else:
                placed_pos = place_checker(board, col, current_checker)
                break

        # If placed_pos is None => column full, skip win and draw checks
        if placed_pos:
            row_placed, col_placed = placed_pos
            if check_win(board, row_placed, col_placed, current_checker):
                print_board(board)
                print(f"Player {current_checker} won!")
                return
            if board_full(board):
                print_board(board)
                print("The game is a draw.")
                return

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % players_count

if __name__ == "__main__":
    main()
