import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUMBER_OF_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Create the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # For UNIX/Linux systems
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

# Check if a move is valid
def is_valid_move(column, board):
    return 0 <= column < COLUMNS and board[0][column] == ' '

# Get the next open row for a column
def get_next_open_row(column, board):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            return row
    return None

# Place the checker
def place_checker(column, checker, board):
    row = get_next_open_row(column, board)
    board[row][column] = checker

# Check for a win
def check_win(checker, board):
    # Horizontal Check
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Vertical Check
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Ascending Diagonal Check
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Descending Diagonal Check
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

# Main function
def connect4():
    board = create_board()
    player_turn = random.randint(0, NUMBER_OF_PLAYERS - 1)
    game_over = False

    print_board(board)

    while not game_over:
        current_checker = CHECKERS[player_turn]
        print(f"Player {current_checker}, please enter a column (A-G):")

        valid_move = False
        while not valid_move:
            input_col = input().upper()

            if input_col and 'A' <= input_col <= 'Z':
                column = ord(input_col) - 65

                if is_valid_move(column, board):
                    place_checker(column, current_checker, board)
                    valid_move = True
                else:
                    print("Invalid move! The column is full or invalid. Try again:")
            else:
                print("Invalid input! Please enter a valid column (A-G):")

        print_board(board)

        if check_win(current_checker, board):
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            player_turn = (player_turn + 1) % NUMBER_OF_PLAYERS

if __name__ == "__main__":
    connect4()
