import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # Between 2 and 5 inclusive
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels A-G
    labels = " ".join([f"  {chr(ord('A') + i)} " for i in range(len(board[0]))])
    print(labels)
    # Print horizontal line
    print("+" + "---+" * len(board[0]))
    for row in board:
        line = "|"
        for cell in row:
            line += f" {cell} |"
        print(line)
        print("+" + "---+" * len(board[0]))

def valid_column_input(input_str, max_col):
    if len(input_str) != 1:
        return False
    c = input_str[0]
    if not ('A' <= c <= chr(ord('A') + max_col - 1)):
        return False
    return True

def column_to_index(c):
    return ord(c) - ord('A')

def place_checker(board, col_idx, checker):
    # Place checker in the lowest empty row in the given column
    for row_idx in range(len(board)-1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    # Column full
    return -1, -1

def check_winner(board, last_row, last_col, checker):
    # Directions: horizontal, vertical, diagonal /
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])
    for dr, dc in directions:
        count = 1  # Include last placed checker
        # Check in positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = last_row - dr, last_col - dc
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
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        checker = players[current_player_idx]
        print(f"Player {checker}, please enter a column:")
        while True:
            user_input = input().upper()
            if not valid_column_input(user_input, COLUMNS):
                print("Invalid input. Please enter a valid column letter:")
                continue
            col_idx = column_to_index(user_input)
            if col_idx < 0 or col_idx >= COLUMNS:
                print("Invalid column. Please enter a valid column letter:")
                continue
            row_idx, col_idx = place_checker(board, col_idx, checker)
            if row_idx == -1:
                # column full, lose turn
                print("Column full. You lose your turn.")
                # Move to next player
                current_player_idx = (current_player_idx + 1) % PLAYERS
                break
            else:
                # Successful move
                print_board(board)
                if check_winner(board, row_idx, col_idx, checker):
                    print(f"Player {checker} won!")
                    return
                if board_full(board):
                    print("The game is a draw!")
                    return
                # Next player's turn
                current_player_idx = (current_player_idx + 1) % PLAYERS
                break

if __name__ == "__main__":
    main()
