import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and initialize the game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    os.system('clear')  # Clear screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def choose_first_player():
    """Randomly select the first player."""
    return random.randint(0, len(PLAYERS) - 1)

def is_valid_input(col_input):
    """Check if the input is a valid column."""
    return len(col_input) == 1 and col_input.isalpha() and ord(col_input.upper()) - 65 < COLS

def get_column_index(col_input):
    """Convert column input (A-G) to index (0-6)."""
    return ord(col_input.upper()) - 65

def drop_checker(board, col, player):
    """Place a checker in the specified column."""
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    """Check for a win condition: horizontal, vertical, or diagonal."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    current_player_index = choose_first_player()

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        col_input = input(f"Player {current_player}, please enter a column: ")

        if not is_valid_input(col_input):
            print("Invalid input. Please try again.")
            continue

        col = get_column_index(col_input)
        if drop_checker(board, col, current_player):
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print("Column is full. Try another column.")

if __name__ == "__main__":
    main()
