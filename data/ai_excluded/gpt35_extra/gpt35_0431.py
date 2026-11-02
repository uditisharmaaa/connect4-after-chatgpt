import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # up to 5 players, use first n in order

# Board alphabet label (max 26 columns)
COLUMN_LABELS = string.ascii_uppercase[:COLUMNS]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(COLUMN_LABELS))
    for r in range(len(board)):
        print("+---" * COLUMNS + "+")
        row_str = "|"
        for c in range(COLUMNS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * COLUMNS + "+")

def is_valid_column_choice(choice):
    return choice in COLUMN_LABELS

def place_checker(board, col_index, checker):
    # Place checker in the lowest empty spot in the col_index column
    # Return True if placed, False if column full
    for row in reversed(range(ROWS)):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False  # column full

def board_full(board):
    # Check if no empty spaces anywhere
    for row in board:
        if " " in row:
            return False
    return True

def check_winner(board, checker):
    # Winning condition: 4 in a row horizontally, vertically or diagonally
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    # Vertical check
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Diagonal "\" check
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    # Diagonal "/" check
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def input_column(player_checker):
    while True:
        choice = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not choice:
            print("Invalid input. Please enter a column letter.")
            continue
        if len(choice) != 1:
            print("Invalid input length. Enter a single uppercase letter.")
            continue
        if not choice.isalpha():
            print("Invalid input. Enter a letter corresponding to a column.")
            continue
        if not is_valid_column_choice(choice):
            print(f"Invalid column '{choice}'. Valid columns are: {', '.join(COLUMN_LABELS)}")
            continue
        return choice

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS_COUNT]

    # Randomly select first player
    current_player_index = random.randint(0, PLAYERS_COUNT - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        choice = input_column(current_checker)
        col_index = COLUMN_LABELS.index(choice)
        placed = place_checker(board, col_index, current_checker)
        if not placed:
            # Turn lost
            print(f"Column {choice} is full. Player {current_checker} loses the turn.")
            current_player_index = (current_player_index + 1) % PLAYERS_COUNT
            print_board(board)
            continue

        print_board(board)

        # Check win
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if board_full(board):
            print("The game is a draw.")
            break

        current_player_index = (current_player_index + 1) % PLAYERS_COUNT

if __name__ == "__main__":
    main()
