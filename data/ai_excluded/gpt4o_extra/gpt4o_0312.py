import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    # Print row contents
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    if column < 0 or column >= COLUMNS:
        return False
    if board[0][column] != " ":
        return False
    return True

def drop_checker(board, column, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal locations for win
    for r in range(ROWS):
        for c in range(COLUMNS-3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True

    # Check vertical locations for win
    for r in range(ROWS-3):
        for c in range(COLUMNS):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True

    # Check positive diagonal
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True

    # Check negative diagonal
    for r in range(3, ROWS):
        for c in range(COLUMNS-3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True

    return False

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Set to 2 for submission
    players = [CHECKERS[i] for i in range(num_players)]

    current_player_index = random.randint(0, num_players - 1)
    current_checker = players[current_player_index]

    clear_screen()
    print_board(board)

    # Game loop
    while True:
        print(f"Player {current_checker}, please enter a column:")
        column_input = input().strip().upper()

        if len(column_input) != 1 or not ('A' <= column_input <= 'G'):
            print("Invalid input. Please enter a valid column (A-G).")
            continue

        column = ord(column_input) - ord('A')

        if is_valid_column(column, board):
            drop_checker(board, column, current_checker)
            clear_screen()
            print_board(board)

            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break

            if check_draw(board):
                print("It's a draw!")
                break

            # Switch player
            current_player_index = (current_player_index + 1) % num_players
            current_checker = players[current_player_index]
        else:
            print("Column is full or invalid. Try a different column.")

if __name__ == "__main__":
    main()
