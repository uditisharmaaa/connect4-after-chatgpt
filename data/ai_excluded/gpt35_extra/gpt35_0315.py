import os
import random

# Constants
ROWS = 6
COLUMNS = 7
WIN_LENGTH = 4
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # In order, support up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column headers
    header = "  "
    for i in range(cols):
        header += f" {chr(ord('A') + i)}  "
    print(header)
    # Print top border
    print("+" + "---+" * cols)
    # Print rows
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+" + "---+" * cols)

def valid_column(col_letter, board):
    if len(col_letter) != 1:
        return False
    col_letter = col_letter.upper()
    if not ('A' <= col_letter <= chr(ord('A') + len(board[0]) - 1)):
        return False
    return True

def column_index(col_letter):
    return ord(col_letter.upper()) - ord('A')

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place checker in the lowest available row in the column
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column full; checker not placed
    return None

def check_line(board, start_row, start_col, d_row, d_col, checker):
    # Check WIN_LENGTH checkers in a line from start position and direction (d_row, d_col)
    count = 0
    row, col = start_row, start_col
    for _ in range(WIN_LENGTH):
        if (0 <= row < len(board)) and (0 <= col < len(board[0])) and board[row][col] == checker:
            count += 1
            row += d_row
            col += d_col
        else:
            break
    return count == WIN_LENGTH

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == checker:
                # Check horizontal right
                if check_line(board, r, c, 0, 1, checker):
                    return True
                # Check vertical down
                if check_line(board, r, c, 1, 0, checker):
                    return True
                # Check diagonal down-right
                if check_line(board, r, c, 1, 1, checker):
                    return True
                # Check diagonal down-left
                if check_line(board, r, c, 1, -1, checker):
                    return True
    return False

def check_draw(board):
    # Board is full if no empty spaces in top row (or anywhere really)
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def get_valid_input(player_checker, board):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not valid_column(user_input, board):
            print("Invalid input! Please enter a valid column letter.")
            continue
        col = column_index(user_input)
        if is_column_full(board, col):
            print("Column is full! You lose your turn.")
            return None
        return col

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        col = get_valid_input(player_checker, board)
        if col is None:
            # Player loses turn due to full column, move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        pos = place_checker(board, col, player_checker)
        print_board(board)

        if pos is None:
            # Should not happen due to previous check, but just in case
            print("Unexpected error placing checker.")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_draw(board):
            print("Game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
