import os
import random

# Constants (modify these as needed for different board sizes or number of players)
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the game board."""
    clear_screen()
    column_labels = "   ".join(chr(65 + i) for i in range(len(board[0])))  # Column letters: A, B, C...
    print(f"  {column_labels}")
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def is_valid_column(column, board):
    """Check if a column is a valid choice for a move."""
    if not (column.isalpha() and len(column) == 1):  # Ensure it's a single letter
        return False
    column_index = ord(column.upper()) - ord('A')
    if column_index < 0 or column_index >= len(board[0]):  # Out of range
        return False
    if board[0][column_index] != " ":  # Column is full
        return False
    return True

def get_next_open_row(column_index, board):
    """Get the next available row in the specified column."""
    for row in range(len(board)-1, -1, -1):
        if board[row][column_index] == " ":
            return row
    return -1  # Column is full

def drop_checker(row, column_index, checker, board):
    """Place the player's checker in the specified column."""
    board[row][column_index] = checker

def check_win(board, checker):
    """Check if the specified checker has won the game."""
    # Check horizontal
    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonals (bottom-left to top-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonals (top-left to bottom-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(board[0][col] != " " for col in range(len(board[0])))

def main():
    # Initialize the game
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    # Game loop
    while True:
        print_board(board)
        print(f"Player {players[current_player_index]}, please enter a column:")
        user_input = input().strip().upper()

        if not is_valid_column(user_input, board):
            print("Invalid input. Try again.")
            continue

        column_index = ord(user_input) - ord('A')
        row = get_next_open_row(column_index, board)

        if row == -1:
            print("Column is full. Try another column.")
            continue

        # Drop checker and check for win/draw
        drop_checker(row, column_index, players[current_player_index], board)

        if check_win(board, players[current_player_index]):
            print_board(board)
            print(f"Player {players[current_player_index]} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
