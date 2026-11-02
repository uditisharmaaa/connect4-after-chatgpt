import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Validate the input
def valid_input(input, board):
    if not input.isalpha() or len(input) != 1:
        return False
    input = input.upper()
    col_index = ord(input) - ord('A')
    if col_index < 0 or col_index >= COLUMNS or board[0][col_index] != ' ':
        return False
    return True

# Place the checker
def place_checker(board, col, checker):
    col_index = ord(col.upper()) - ord('A')
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            break

# Check for win
def check_win(board, checker):
    # Check horizontal, vertical and diagonal
    for row in range(ROWS):
        for col in range(COLUMNS):
            if col <= COLUMNS - 4 and all(board[row][col + i] == checker for i in range(4)):
                return True
            if row <= ROWS - 4 and all(board[row + i][col] == checker for i in range(4)):
                return True
            if row <= ROWS - 4 and col <= COLUMNS - 4:
                if all(board[row + i][col + i] == checker for i in range(4)):
                    return True
                if all(board[row + i][col + 3 - i] == checker for i in range(4)):
                    return True
    return False

# Check for draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Main function
def main():
    players = 2
    board = create_board()
    current_player_index = random.randint(0, players - 1)
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player_index]
        column = input(f"Player {current_checker}, please enter a column: ").strip()
        
        while not valid_input(column, board):
            column = input(f"Invalid input, Player {current_checker}, please enter a valid column: ").strip()
        
        place_checker(board, column, current_checker)
        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % players

if __name__ == "__main__":
    main()
