import os
import random

# Constants
NUM_ROWS = 6
NUM_COLUMNS = 7
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Max 5 players
VALID_COLUMNS = [chr(65 + i) for i in range(NUM_COLUMNS)]  # ['A', 'B', 'C', ..., 'G']

def clear_screen():
    os.system('clear')  # Use 'cls' on Windows

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    header = "  " + "   ".join(VALID_COLUMNS[:len(board[0])])
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_input(column):
    return column in VALID_COLUMNS

def find_next_empty_row(board, column_index):
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][column_index] == " ":
            return row
    return None

def check_win(board, symbol):
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Check vertical
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check diagonal (down-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonal (up-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(NUM_COLUMNS))

def main():
    # Initialize the board and players
    board = create_board(NUM_ROWS, NUM_COLUMNS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")

        # Get valid input
        while True:
            column = input().strip().upper()
            if not is_valid_input(column):
                print("Invalid input! Please enter a valid column (e.g., A-G).")
                continue

            column_index = VALID_COLUMNS.index(column)
            next_empty_row = find_next_empty_row(board, column_index)
            if next_empty_row is None:
                print("That column is full! Choose another one.")
            else:
                break

        # Place the checker
        board[next_empty_row][column_index] = current_player

        clear_screen()
        print_board(board)

        # Check for win or draw
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
