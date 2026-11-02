import random
import os

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
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(row) + "+")

def is_valid_input(column, board):
    return column.isalpha() and 0 <= ord(column) - 65 < len(board[0])

def is_column_full(column, board):
    return board[0][column] != " "

def place_checker(column, checker, board):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

def check_winner(checker, board):
    rows = len(board)
    cols = len(board[0])

    def check_line(a, b, c, d):
        return a == b == c == d == checker

    # Horizontal check
    for row in range(rows):
        for col in range(cols - 3):
            if check_line(board[row][col], board[row][col + 1], board[row][col + 2], board[row][col + 3]):
                return True

    # Vertical check
    for col in range(cols):
        for row in range(rows - 3):
            if check_line(board[row][col], board[row + 1][col], board[row + 2][col], board[row + 3][col]):
                return True

    # Diagonal checks
    for row in range(rows - 3):
        for col in range(cols - 3):
            if check_line(board[row][col], board[row + 1][col + 1], board[row + 2][col + 2], board[row + 3][col + 3]):
                return True

        for col in range(3, cols):
            if check_line(board[row][col], board[row + 1][col - 1], board[row + 2][col - 2], board[row + 3][col - 3]):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def connect_four():
    board = create_board(ROWS, COLUMNS)
    players = 2  # Set number of players
    checkers = CHECKERS[:players]
    current_player = random.choice(range(players))

    while True:
        print_board(board)
        column_input = input(f"Player {checkers[current_player]}, please enter a column: ").strip().upper()

        if not is_valid_input(column_input, board):
            print("Invalid input. Please enter a valid column letter.")
            continue

        column_index = ord(column_input) - 65

        if is_column_full(column_index, board):
            print("Column is full. Please choose another column.")
            continue

        place_checker(column_index, checkers[current_player], board)

        if check_winner(checkers[current_player], board):
            print_board(board)
            print(f"Player {checkers[current_player]} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % players

if __name__ == "__main__":
    connect_four()
