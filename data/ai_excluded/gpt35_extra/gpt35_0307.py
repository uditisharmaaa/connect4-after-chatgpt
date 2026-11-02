import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers: A, B, C, ...
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(header)
    print("+" + "---+" * len(board[0]))
    for row in board:
        row_str = "| " + " | ".join(row) + " |"
        print(row_str)
        print("+" + "---+" * len(board[0]))

def valid_column_letter(letter, columns):
    if len(letter) != 1 or not letter.isalpha() or not letter.isupper():
        return False
    index = ord(letter) - ord('A')
    return 0 <= index < columns

def get_column_index(letter):
    return ord(letter) - ord('A')

def place_checker(board, col_index, checker):
    # From bottom to top find empty spot
    for row_index in reversed(range(len(board))):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return row_index
    # Column full
    return -1

def check_line(line, checker):
    count = 0
    for cell in line:
        if cell == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    return False

def check_horizontal(board, checker):
    for row in board:
        if check_line(row, checker):
            return True
    return False

def check_vertical(board, checker):
    columns = len(board[0])
    rows = len(board)
    for col in range(columns):
        col_vals = [board[row][col] for row in range(rows)]
        if check_line(col_vals, checker):
            return True
    return False

def check_diagonal(board, checker):
    rows = len(board)
    columns = len(board[0])
    # Check / diagonals
    for row in range(rows - WIN_COUNT + 1):
        for col in range(columns - WIN_COUNT + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_COUNT)):
                return True
    # Check \ diagonals
    for row in range(WIN_COUNT - 1, rows):
        for col in range(columns - WIN_COUNT + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_COUNT)):
                return True
    return False

def check_win(board, checker):
    return (
        check_horizontal(board, checker)
        or check_vertical(board, checker)
        or check_diagonal(board, checker)
    )

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    checkers = CHECKERS[:PLAYERS]

    # Choose random player to start
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)
    print(f"Player {checkers[current_player_index]} starts!")

    while True:
        checker = checkers[current_player_index]
        valid_input = False

        # Input loop for valid column
        while not valid_input:
            user_input = input(f"Player {checker}, please enter a column: ").strip()
            if not valid_column_letter(user_input, COLUMNS):
                continue  # invalid input, ask again
            col = get_column_index(user_input)
            # Check if column full
            if board[0][col] != " ":  # top cell occupied = full
                # Player loses turn if column full
                valid_input = True
                col = -1
                break
            else:
                valid_input = True

        if col == -1:
            # Column full, player loses turn, go to next player
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue

        # Place checker
        row_placed = place_checker(board, col, checker)
        print_board(board)

        # Check win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player turn
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
