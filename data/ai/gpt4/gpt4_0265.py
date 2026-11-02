import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board."""
    os.system('clear')  # Clear the screen for a fresh board display
    column_labels = "  ".join(chr(ord('A') + i) for i in range(COLUMNS))  # Column letters
    print(f"  {column_labels}")
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    """Check if the selected column is valid."""
    if column < 0 or column >= COLUMNS:
        return False
    if board[0][column] != " ":
        return False
    return True

def place_checker(column, player, board):
    """Place a checker in the selected column."""
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom row
        if board[row][column] == " ":
            board[row][column] = player
            return row, column

def check_win(row, column, player, board):
    """Check if the player has won."""
    # Check horizontal
    for col in range(max(0, column - 3), min(COLUMNS - 3, column) + 1):
        if all(board[row][col + i] == player for i in range(4)):
            return True

    # Check vertical
    for r in range(max(0, row - 3), min(ROWS - 3, row) + 1):
        if all(board[r + i][column] == player for i in range(4)):
            return True

    # Check diagonal (bottom-left to top-right)
    for delta in range(-3, 1):
        if 0 <= row + delta < ROWS - 3 and 0 <= column + delta < COLUMNS - 3:
            if all(board[row + delta + i][column + delta + i] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for delta in range(-3, 1):
        if 0 <= row - delta < ROWS - 3 and 0 <= column + delta < COLUMNS - 3:
            if all(board[row - delta - i][column + delta + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board()
    num_players = 2  # Fixed for submission, can be 2-5
    players = PLAYERS[:num_players]  # Players selected
    current_player = random.randint(0, num_players - 1)  # Random first player

    print_board(board)
    print(f"Player {players[current_player]} starts!")

    while True:
        print_board(board)
        print(f"Player {players[current_player]}, please enter a column:")
        user_input = input().strip().upper()

        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a valid column letter.")
            continue

        column = ord(user_input) - ord('A')
        if not is_valid_column(column, board):
            print("Invalid move. Please choose a non-full column within bounds.")
            continue

        row, col = place_checker(column, players[current_player], board)

        if check_win(row, col, players[current_player], board):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
