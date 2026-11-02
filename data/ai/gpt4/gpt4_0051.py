import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY = " "

# Helper functions
def clear_screen():
    os.system('clear')  # Use 'cls' for Windows

def initialize_board():
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    columns = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(columns)
    print("+---" * COLUMNS + "+")

    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(board, col):
    return 0 <= col < COLUMNS and board[0][col] == EMPTY

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == EMPTY:
            row[col] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != EMPTY for row in board for cell in row)

def get_column_input():
    while True:
        user_input = input("Please enter a column (A-G): ").strip().upper()
        if len(user_input) == 1 and 'A' <= user_input <= chr(ord('A') + COLUMNS - 1):
            return ord(user_input) - ord('A')
        print("Invalid input. Try again.")

def main():
    # Initialize game
    board = initialize_board()
    player_order = [CHECKERS[i] for i in range(PLAYERS)]
    random.shuffle(player_order)  # Randomize first player
    clear_screen()
    print_board(board)

    # Game loop
    current_player = 0
    while True:
        print(f"Player {player_order[current_player]}'s turn.")
        col = get_column_input()

        if is_valid_column(board, col):
            drop_checker(board, col, player_order[current_player])
            clear_screen()
            print_board(board)

            # Check win
            if check_winner(board, player_order[current_player]):
                print(f"Player {player_order[current_player]} won!")
                break

            # Check draw
            if is_draw(board):
                print("It's a draw!")
                break

            current_player = (current_player + 1) % PLAYERS
        else:
            print("Column full or invalid choice. Try again.")

if __name__ == "__main__":
    main()
