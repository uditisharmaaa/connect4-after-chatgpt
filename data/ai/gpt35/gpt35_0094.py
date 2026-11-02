import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(labels))
    # Print board rows
    for r in range(len(board)):
        print("+" + "---+" * len(board[0]))
        print("| " + " | ".join(board[r]) + " |")
    print("+" + "---+" * len(board[0]))

def valid_column(input_str, board):
    if len(input_str) != 1:
        return False
    upper = input_str.upper()
    if upper < 'A' or upper >= chr(ord('A') + len(board[0])):
        return False
    col = ord(upper) - ord('A')
    # Check if column is full
    return board[0][col] == " "

def get_column_input(player_checker, board):
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not valid_column(col_input, board):
            print("Invalid input or column is full. Please try again.")
            continue
        return ord(col_input) - ord('A')

def place_checker(board, col, checker):
    # Place checker in the lowest available space in column
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column full, return None (shouldn't happen if input is validated)
    return None, None

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, row, col, checker):
    # Check all four directions with count logic:
    # Horizontal: (0, -1) and (0, 1)
    # Vertical: (-1, 0) and (1, 0)
    # Diagonal 1: (-1, -1) and (1, 1)
    # Diagonal 2: (-1, 1) and (1, -1)
    directions = [
        ((0, -1), (0, 1)),
        ((-1, 0), (1, 0)),
        ((-1, -1), (1, 1)),
        ((-1, 1), (1, -1)),
    ]
    for d1, d2 in directions:
        count = 1  # including the current checker
        count += check_direction(board, row + d1[0], col + d1[1], d1[0], d1[1], checker)
        count += check_direction(board, row + d2[0], col + d2[1], d2[0], d2[1], checker)
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)
    print(f"Player {players[current_player_index]} goes first!")

    while True:
        checker = players[current_player_index]
        col = get_column_input(checker, board)
        row, col = place_checker(board, col, checker)

        print_board(board)

        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
