import os
import random
import sys

# Constants (configured as per instructions)
ROWS = 6
COLS = 7
MAX_COLS = 26  # Maximum columns (A-Z)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # Set to 2 for the assignment
WIN_LENGTH = 4
EMPTY = " "

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([EMPTY] * cols)
    return board

def print_board(board):
    cols = len(board[0])
    # Print column labels
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    print("+" + "---+" * cols)
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_column_input(board):
    cols = len(board[0])
    letters = [chr(ord('A') + i) for i in range(cols)]
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        if user_input not in letters:
            print("Invalid input. Please enter a column letter from {} to {}.".format(letters[0], letters[-1]))
            continue
        col_idx = ord(user_input) - ord('A')
        # Check if column is full
        if board[0][col_idx] != EMPTY:
            print("Column is full. You lose your turn!")
            return None
        return col_idx

def drop_checker(board, col, checker):
    # Places checker in the lowest available row in the column
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = checker
            return row, col
    return None, None

def is_winning_move(board, row, col, checker):
    return (check_line(board, row, col, 0, 1, checker) + check_line(board, row, col, 0, -1, checker) > WIN_LENGTH - 2 or
            check_line(board, row, col, 1, 0, checker) + check_line(board, row, col, -1, 0, checker) > WIN_LENGTH - 2 or
            check_line(board, row, col, 1, 1, checker) + check_line(board, row, col, -1, -1, checker) > WIN_LENGTH - 2 or
            check_line(board, row, col, 1, -1, checker) + check_line(board, row, col, -1, 1, checker) > WIN_LENGTH - 2)

def check_line(board, row, col, dr, dc, checker):
    count = 0
    for i in range(1, WIN_LENGTH):
        r = row + dr * i
        c = col + dc * i
        if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
        else:
            break
    return count

def is_board_full(board):
    for cell in board[0]:
        if cell == EMPTY:
            return False
    return True

def main():
    # Initialization
    board = create_board(ROWS, COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)
    print(f"Player {players[current_player_idx]} starts!")

    while True:
        current_checker = players[current_player_idx]
        print(f"Player {current_checker},", end=" ")
        col_idx = get_valid_column_input(board)
        if col_idx is None:
            # Lose turn if column is full
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        row, col = drop_checker(board, col_idx, current_checker)
        clear_screen()
        print_board(board)

        if is_winning_move(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        if is_board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
