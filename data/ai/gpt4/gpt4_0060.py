import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
MAX_COLUMNS = 26

def initialize_board(rows, cols):
    """Creates an empty game board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board to the console."""
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))  # Column labels
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(board, col):
    """Check if the column is valid and not full."""
    try:
        column_index = ord(col.upper()) - 65
        if 0 <= column_index < len(board[0]):
            return board[0][column_index] == " "
    except:
        pass
    return False

def drop_checker(board, col, checker):
    """Drops a checker in the selected column."""
    column_index = ord(col.upper()) - 65
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return True
    return False

def check_win(board, checker):
    """Checks for any win condition (horizontal, vertical, or diagonal)."""
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for row in board:
        for col in range(cols - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(cols):
        for row in range(rows - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the game ends in a draw (board is fully occupied)."""
    return all(cell != " " for row in board for cell in row)

def get_valid_input(prompt, board):
    """Gets valid column input from the user."""
    while True:
        col = input(prompt).strip().upper()
        if is_valid_column(board, col):
            return col
        print("Invalid input. Please enter a valid column.")

def get_random_player(player_count):
    """Randomly selects the first player."""
    return random.randint(0, player_count - 1)

def main():
    # Game setup
    board = initialize_board(ROWS, COLUMNS)
    players = [PLAYER_CHECKERS[i] for i in range(2)]  # Adjust player count for testing
    current_player = get_random_player(len(players))

    # Game loop
    print_board(board)
    while True:
        print(f"Player {players[current_player]}'s turn.")
        col = get_valid_input("Please enter a column: ", board)
        drop_checker(board, col, players[current_player])

        print_board(board)

        if check_win(board, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % len(players)

if __name__ == "__main__":
    main()
