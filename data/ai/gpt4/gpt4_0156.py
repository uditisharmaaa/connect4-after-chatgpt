import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_TOKENS = ["X", "O", "V", "H", "M"][:2]  # Set the token count to match the number of players (2 here)

# Functions
def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column labels
    labels = "  ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {labels}")
    # Print board rows
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    if column < 0 or column >= len(board[0]):
        return False
    return board[0][column] == " "

def get_column_index(column_letter):
    return ord(column_letter.upper()) - 65

def place_checker(board, column, token):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = token
            return

def check_for_win(board, token):
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == token for i in range(4)):
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == token for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == token for i in range(4)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(rows - 3):
        for c in range(3, cols):
            if all(board[r + i][c - i] == token for i in range(4)):
                return True

    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    # Setup
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_TOKENS
    num_players = len(players)
    current_player_index = random.randint(0, num_players - 1)
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, it's your turn!")
        while True:
            column_letter = input("Please enter a column (A-G): ").strip()
            if len(column_letter) != 1 or not column_letter.isalpha():
                print("Invalid input. Enter a single letter for the column.")
                continue

            column_index = get_column_index(column_letter)
            if not (0 <= column_index < COLUMNS):
                print("Invalid column. Please select a column within range.")
                continue

            if not is_valid_column(column_index, board):
                print("Column full. Choose a different column.")
                continue

            break

        place_checker(board, column_index, current_player)
        clear_screen()
        print_board(board)

        # Check for win
        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break

        # Switch player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
