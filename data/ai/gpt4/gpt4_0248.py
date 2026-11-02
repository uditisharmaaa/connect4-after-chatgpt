import os
import random

# Constants (can be modified for different board sizes and number of players)
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Symbols for players
NUM_PLAYERS = 2  # Default to 2 players

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))  # A, B, C, ...
    separator = "+---" * len(board[0]) + "+"
    print(column_labels)
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)

def is_valid_column(choice, board):
    if len(choice) != 1 or not choice.isalpha() or choice.upper() < 'A' or choice.upper() > chr(65 + len(board[0]) - 1):
        return False
    column = ord(choice.upper()) - 65
    return any(row[column] == " " for row in board)

def drop_checker(board, column, symbol):
    for row in reversed(board):  # Start from the bottom
        if row[column] == " ":
            row[column] = symbol
            return

def check_winner(board, symbol):
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == symbol for i in range(4)):
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == symbol for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == symbol for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == symbol for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialize game
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)  # Random start player
    print_board(board)

    # Main game loop
    while True:
        print(f"Player {players[current_player]}, it's your turn.")
        column_choice = input("Please enter a column (e.g., A-G): ").strip()

        if not is_valid_column(column_choice, board):
            print("Invalid column. Please try again.")
            continue

        column_index = ord(column_choice.upper()) - 65
        drop_checker(board, column_index, players[current_player])
        print_board(board)

        # Check for a win
        if check_winner(board, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Alternate turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
