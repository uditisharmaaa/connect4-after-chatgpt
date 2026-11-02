import os
import random
import sys

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2  # Must be between 2 and 5 inclusive
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column headers
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(headers)
    # Print rows
    for r in range(rows):
        print("+" + "---+" * cols)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+" + "---+" * cols)

def is_valid_column(col, cols):
    return col.isalpha() and col.upper() >= 'A' and col.upper() < chr(ord('A') + cols)

def column_to_index(col):
    return ord(col.upper()) - ord('A')

def find_row_for_checker(board, col_idx):
    # The checker falls to the lowest empty spot in the selected column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return -1  # Column full

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])
    needed = 4

    # Horizontal check
    for r in range(rows):
        for c in range(cols - needed + 1):
            if all(board[r][c + i] == checker for i in range(needed)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - needed + 1):
            if all(board[r + i][c] == checker for i in range(needed)):
                return True

    # Diagonal down-right check
    for r in range(rows - needed + 1):
        for c in range(cols - needed + 1):
            if all(board[r + i][c + i] == checker for i in range(needed)):
                return True

    # Diagonal down-left check
    for r in range(rows - needed + 1):
        for c in range(needed - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(needed)):
                return True

    return False

def is_draw(board):
    # If no empty spaces in top row (or anywhere) - draw
    return all(cell != " " for cell in board[0])

def get_next_player_index(current_index, total_players):
    return (current_index + 1) % total_players

def main():
    # Initialization
    if PLAYERS < 2 or PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        sys.exit(1)

    board = create_board(ROWS, COLS)
    checkers = CHECKERS[:PLAYERS]

    # Random starting player
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = checkers[current_player]
        print(f"Player {player_checker}, please enter a column:")
        inp = input().strip()
        while True:
            if not inp:
                print(f"Invalid input. Player {player_checker}, please enter a column:")
            elif not is_valid_column(inp, COLS):
                print(f"Invalid column. Player {player_checker}, please enter a column:")
            else:
                col_idx = column_to_index(inp)
                row_idx = find_row_for_checker(board, col_idx)
                if row_idx == -1:
                    # Column full, player loses turn, no input repetition
                    # Just break to end turn
                    break
                else:
                    # Place checker
                    board[row_idx][col_idx] = player_checker
                    break
            inp = input().strip()

        print_board(board)

        # If checker was actually placed
        if row_idx != -1:
            if check_winner(board, player_checker):
                print(f"Player {player_checker} won!")
                break
            if is_draw(board):
                print("Game is a draw!")
                break

        # Next player's turn
        current_player = get_next_player_index(current_player, PLAYERS)

if __name__ == "__main__":
    main()
