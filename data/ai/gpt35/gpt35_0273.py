import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    clear_screen()
    # Print column headers A-G
    header = "  "
    for i in range(len(board[0])):
        header += " " + chr(ord('A') + i) + "  "
    print(header)
    # Print rows with separators
    line = "+" + "---+" * len(board[0])
    for row in board:
        print(line)
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    print(line)

def get_valid_column_input(player, board):
    cols = len(board[0])
    while True:
        col_input = input(f"Player {player}, please enter a column: ")
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a letter corresponding to a column.")
            continue
        col_letter = col_input.upper()
        col_index = ord(col_letter) - ord('A')
        if col_index < 0 or col_index >= cols:
            print("Invalid column. Please enter a valid column letter.")
            continue
        # Check if column is full
        if board[0][col_index] != " ":
            # Column full, player loses turn
            return -1
        return col_index

def place_checker(board, col_index, checker):
    # Start from bottom row and go up to find first empty cell
    for row in range(len(board)-1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    # Should never get here because we check if column is full before
    return -1, -1

def check_win(board, checker, row, col):
    rows = len(board)
    cols = len(board[0])

    # Directions: horizontal, vertical, diagonal /
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1

        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    # Setup
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]

    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_index]
        col = get_valid_column_input(player_checker, board)
        if col == -1:
            # Column full, lose turn
            print(f"Column is full, Player {player_checker} loses turn.")
            current_player_index = (current_player_index + 1) % PLAYERS
            continue

        row, col = place_checker(board, col, player_checker)
        print_board(board)

        if check_win(board, player_checker, row, col):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
