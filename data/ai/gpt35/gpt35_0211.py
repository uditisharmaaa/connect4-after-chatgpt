import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4
PLAYERS_COUNT = 2  # Set to 2 players for submission
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Print column labels
    header = "  "
    for i in range(columns):
        header += "  " + chr(ord('A') + i) + " "
    print(header)
    # Print the board rows
    for r in range(len(board)):
        print("+---" * columns + "+")
        row_str = "|"
        for c in range(columns):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+---" * columns + "+")

def is_valid_column(input_str, columns):
    if len(input_str) != 1:
        return False
    column_index = ord(input_str) - ord('A')
    return 0 <= column_index < columns

def column_full(board, col_idx):
    # If top row in this column is occupied, column is full
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    # Start from bottom row, place checker in first empty spot
    for row_idx in reversed(range(len(board))):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    return None  # Should not happen if column_full is checked

def check_win(board, checker, r, c):
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1), # diagonal down-left
    ]
    rows = len(board)
    columns = len(board[0])

    for dr, dc in directions:
        count = 1
        # Check forward direction
        rr, cc = r + dr, c + dc
        while 0 <= rr < rows and 0 <= cc < columns and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc
        # Check backward direction
        rr, cc = r - dr, c - dc
        while 0 <= rr < rows and 0 <= cc < columns and board[rr][cc] == checker:
            count += 1
            rr -= dr
            cc -= dc

        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    # Board is full if no spaces in top row
    return all(cell != " " for cell in board[0])

def main():
    rows = ROWS
    columns = COLUMNS
    players_count = PLAYERS_COUNT

    # Validate constants for submission requirements
    if rows != 6 or columns != 7:
        raise ValueError("Board dimensions must be 6 rows x 7 columns")
    if players_count != 2:
        raise ValueError("Number of players must be 2 for submission")

    board = create_board(rows, columns)
    players = CHECKERS[:players_count]

    # Randomly select starting player (index)
    current_player_idx = random.randint(0, players_count -1)

    while True:
        print_board(board)
        current_checker = players[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "

        # Input loop
        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_column(user_input, columns):
                # Invalid input: wrong length or letter out of range
                print("Invalid column. Please enter a valid column letter.")
                continue
            col_idx = ord(user_input) - ord('A')
            if column_full(board, col_idx):
                # Column full: lose turn
                print(f"Column {user_input} is full. You lose your turn.")
                break
            # Valid and has space
            placed = place_checker(board, col_idx, current_checker)
            if placed:
                r, c = placed
                # Check win
                if check_win(board, current_checker, r, c):
                    print_board(board)
                    print(f"Player {current_checker} won!")
                    return
                # Check draw after placing
                if board_full(board):
                    print_board(board)
                    print("The game is a draw.")
                    return
                break
            else:
                # This should not happen because column_full checked
                print(f"Could not place checker in column {user_input}. Try again.")

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % players_count

if __name__ == "__main__":
    main()
