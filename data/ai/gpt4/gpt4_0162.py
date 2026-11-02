import os
import random

# Constants for board dimensions and player settings
ROWS = 6
COLUMNS = 7
PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # Allowed checkers for up to 5 players

def create_board():
    """
    Create an empty board for the game.
    """
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """
    Prints the board to the console.
    """
    os.system('clear')
    # Print column labels
    column_labels = '  '.join(chr(65 + i) for i in range(COLUMNS))
    print(f"  {column_labels}")
    print("+---" * COLUMNS + "+")

    # Print board cells
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_move(board, column):
    """
    Check if the move is valid.
    """
    return column >= 0 and column < COLUMNS and board[0][column] == " "

def get_column_from_input():
    """
    Prompt the player for input and validate column choice.
    """
    while True:
        try:
            column_letter = input("Please enter a column: ").strip().upper()
            column = ord(column_letter) - 65
            if 0 <= column < COLUMNS:
                return column
            else:
                print("Invalid column. Choose a valid column (A-G).")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid column.")

def place_checker(board, column, checker):
    """
    Place the checker in the correct position in the column.
    """
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

def check_win(board, checker):
    """
    Check if the given player with `checker` has won.
    """
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (
                check_direction(board, row, col, checker, 0, 1) or  # Horizontal
                check_direction(board, row, col, checker, 1, 0) or  # Vertical
                check_direction(board, row, col, checker, 1, 1) or  # Diagonal down-right
                check_direction(board, row, col, checker, 1, -1)    # Diagonal down-left
            ):
                return True
    return False

def check_direction(board, row, col, checker, row_delta, col_delta):
    """
    Check for 4 in a row in a specific direction (row_delta, col_delta).
    """
    count = 0
    for i in range(4):
        r, c = row + i * row_delta, col + i * col_delta
        if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
        else:
            break
    return count == 4

def is_board_full(board):
    """
    Check if the board is completely filled.
    """
    return all(cell != " " for cell in board[0])

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board()
    player_checkers = PLAYER_CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)
    print(f"Player {player_checkers[current_player]} starts the game!")

    while True:
        print_board(board)
        print(f"Player {player_checkers[current_player]}'s turn.")
        column = get_column_from_input()

        if is_valid_move(board, column):
            place_checker(board, column, player_checkers[current_player])

            if check_win(board, player_checkers[current_player]):
                print_board(board)
                print(f"Player {player_checkers[current_player]} won!")
                break

            if is_board_full(board):
                print_board(board)
                print("The game is a draw!")
                break

            current_player = (current_player + 1) % PLAYERS
        else:
            print("Column full or invalid. Try again.")

if __name__ == "__main__":
    main()
