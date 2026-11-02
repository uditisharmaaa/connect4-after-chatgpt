import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')  # Use 'cls' on Windows

def create_board(rows, columns):
    """Creates an empty board with the given rows and columns."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the board to the terminal."""
    column_labels = " ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {column_labels}")
    print(" +" + "---+" * len(board[0]))
    for row in board:
        print(" | " + " | ".join(row) + " |")
        print(" +" + "---+" * len(board[0]))

def is_valid_column(column, board):
    """Checks if the chosen column is valid (exists and has space)."""
    return column.isalpha() and 0 <= ord(column.upper()) - 65 < len(board[0]) and board[0][ord(column.upper()) - 65] == " "

def get_valid_column(board):
    """Asks the player for a valid column until the input is valid."""
    while True:
        column = input("Please enter a valid column: ").strip().upper()
        if is_valid_column(column, board):
            return ord(column) - 65
        print("Invalid column. Try again.")

def place_checker(board, column, checker):
    """Places a checker in the lowest available row of the specified column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            break

def check_winner(board, checker):
    """Checks if the given checker has 4 in a row (horizontal, vertical, diagonal)."""
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c:c + 4] == [checker] * 4:
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (up-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw (no empty spaces left)."""
    return all(cell != " " for row in board for cell in row)

def play_game():
    """Main function to play Connect 4."""
    # Initialize game
    board = create_board(ROWS, COLUMNS)
    num_players = 2
    players = PLAYER_TOKENS[:num_players]
    current_player = random.randint(0, num_players - 1)

    clear_screen()
    print_board(board)

    while True:
        print(f"Player {players[current_player]}'s turn.")
        column = get_valid_column(board)
        place_checker(board, column, players[current_player])

        clear_screen()
        print_board(board)

        # Check for a winner
        if check_winner(board, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    play_game()
