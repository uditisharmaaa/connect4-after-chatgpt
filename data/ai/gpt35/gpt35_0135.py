import os
import random
import string

# Constants (set for submission)
ROWS = 6
COLUMNS = 7
PLAYERS = 2

# Checkers for players in order
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels A... depending on columns
    letters = string.ascii_uppercase[:len(board[0])]
    print("  " + "   ".join(letters))
    # Print each row with separators
    for row in board:
        print("+" + "---+" * len(row))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * len(board[0]))

def input_to_col_idx(user_input, columns):
    user_input = user_input.strip().upper()
    if len(user_input) != 1:
        return None
    if user_input not in string.ascii_uppercase[:columns]:
        return None
    return string.ascii_uppercase.index(user_input)

def column_full(board, col_idx):
    # If top cell of the column is occupied, column is full
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    # Place the checker in the lowest available space in the column
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    return None  # column full, no place found

def check_for_win(board, checker, row, col):
    rows = len(board)
    cols = len(board[0])

    def count_dir(dx, dy):
        count = 0
        r, c = row + dy, col + dx
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dy
            c += dx
        return count

    # Check all directions: horizontal, vertical, two diagonals
    directions = [
        (1, 0),   # horizontal right
        (0, 1),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal up-right
    ]
    for dx, dy in directions:
        # Count same checkers in positive and negative directions
        total = 1 + count_dir(dx, dy) + count_dir(-dx, -dy)
        if total >= 4:
            return True
    return False

def board_full(board):
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    # Validate PLAYERS in [2,5] and checkers available
    if not (2 <= PLAYERS <= 5):
        print("Invalid number of players. Must be between 2 and 5.")
        return
    players_checkers = CHECKERS[:PLAYERS]

    # Randomly select starting player index
    current_player = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        player_checker = players_checkers[current_player]
        print(f"Player {player_checker}, please enter a column:")

        col_idx = None
        # Input validation loop for column choice
        while True:
            user_input = input().strip().upper()
            col_idx = input_to_col_idx(user_input, COLUMNS)
            if col_idx is None:
                print("Invalid input. Please enter a valid column letter (A-G):")
                continue
            if column_full(board, col_idx):
                # Column full, player loses turn
                print("Column is full. You lose your turn.")
                break
            # Valid and not full column, break to place checker
            break

        if col_idx is not None and not column_full(board, col_idx):
            placed = place_checker(board, col_idx, player_checker)
            row_placed, col_placed = placed

            print_board(board)

            # Check for win condition
            if check_for_win(board, player_checker, row_placed, col_placed):
                print(f"Player {player_checker} won!")
                break

            # Check for draw condition
            if board_full(board):
                print("The game is a draw!")
                break
        else:
            # No checker placed, just print board and continue
            print_board(board)

        # Next player (wrap around)
        current_player = (current_player + 1) % PLAYERS


if __name__ == "__main__":
    main()
