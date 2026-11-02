import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board


def print_board(board):
    clear_screen()
    # Print column headers
    header = "  "
    for i in range(len(board[0])):
        header += "  " + chr(ord('A') + i) + " "
    print(header)
    # Print the board
    line = "+" + "---+" * len(board[0])
    for row in board:
        print(line)
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    print(line)


def is_valid_column(col_char, columns):
    if len(col_char) != 1:
        return False
    col_char = col_char.upper()
    if 'A' <= col_char <= chr(ord('A') + columns - 1):
        return True
    return False


def get_column_index(col_char):
    return ord(col_char.upper()) - ord('A')


def place_checker(board, col, checker):
    # Place checker at lowest available row in column col
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return -1, -1  # column full


def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # check one direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False


def board_full(board):
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    return True


def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        user_input = input().strip().upper()

        if not is_valid_column(user_input, COLUMNS):
            print("Invalid input. Please enter a valid column letter.")
            continue

        col_index = get_column_index(user_input)
        row_index, col_index_placed = place_checker(board, col_index, current_checker)

        if row_index == -1:
            # Column full, player loses turn
            print("Column is full. You lose your turn.")
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_win(board, row_index, col_index_placed, current_checker):
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS


if __name__ == "__main__":
    main()
