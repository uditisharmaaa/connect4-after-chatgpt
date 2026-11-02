import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def is_valid_column(col, cols):
    return 'A' <= col <= chr(ord('A') + cols - 1)

def get_column_index(col):
    return ord(col) - ord('A')

def place_checker(board, col_idx, checker):
    # Check from bottom row upwards for empty slot
    for row_idx in range(len(board) - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    return None  # column full

def check_win(board, r, c, checker):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1

        # Check forward
        rr, cc = r + dr, c + dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc

        # Check backward
        rr, cc = r - dr, c - dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr -= dr
            cc -= dc

        if count >= 4:
            return True

    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    rows = ROWS
    cols = COLUMNS
    num_players = 2  # per assignment submission instructions

    players = PLAYERS[:num_players]

    board = create_board(rows, cols)
    current_player_index = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        prompt = f"Player {current_checker}, please enter a column: "

        valid_input = False
        while not valid_input:
            user_input = input(prompt).strip()
            if len(user_input) != 1 or not is_valid_column(user_input, cols):
                print("Invalid input! Please enter a valid column letter.")
                continue

            col_idx = get_column_index(user_input)
            placement = place_checker(board, col_idx, current_checker)

            if placement is None:
                # Column full, player loses turn
                print(f"Column {user_input} is full. You lose your turn.")
                valid_input = True
            else:
                valid_input = True
                r, c = placement
                print_board(board)

                if check_win(board, r, c, current_checker):
                    print(f"Player {current_checker} won!")
                    return

                if board_full(board):
                    print("The game is a draw!")
                    return

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
