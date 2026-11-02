import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Supports up to 5 players

def create_board(rows, cols):
    """Initialize the Connect 4 board with empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Clear the screen and print the current state of the board."""
    os.system('clear')  # Use 'cls' for Windows
    # Print column headers
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))
    print("+---" * COLS + "+")

    # Print the board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(column):
    """Check if the input column is valid."""
    return column.isalpha() and column.upper() in [chr(i) for i in range(65, 65 + COLS)]

def is_valid_move(board, column):
    """Check if the move can be made in the specified column."""
    col_index = ord(column.upper()) - 65
    return board[0][col_index] == " "

def place_checker(board, column, checker):
    """Place the checker at the lowest available position in the specified column."""
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            break

def check_for_win(board, checker):
    """Check if the given checker has a winning position."""
    # Check horizontal win
    for row in board:
        for col in range(COLS - 3):
            if row[col:col + 4] == [checker] * 4:
                return True

    # Check vertical win
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (\) win
    for col in range(COLS - 3):
        for row in range(ROWS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (/) win
    for col in range(COLS - 3):
        for row in range(3, ROWS):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    """Check if the board is completely filled (draw)."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Run the Connect 4 game."""
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        player_checker = CHECKERS[current_player]
        move = input(f"Player {player_checker}, please enter a column: ").strip().upper()

        if not is_valid_column(move) or not is_valid_move(board, move):
            print("Invalid move. Try again.")
            continue

        place_checker(board, move, player_checker)
        print_board(board)

        if check_for_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_for_draw(board):
            print("The game is a draw!")
            break

        # Switch players
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
