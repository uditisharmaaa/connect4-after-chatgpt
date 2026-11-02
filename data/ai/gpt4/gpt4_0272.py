import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Supports up to 5 players

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Create and return an empty game board."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Display the board."""
    clear_screen()
    column_labels = " ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {column_labels}")
    for row in board:
        print("+---" * len(board[0]) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    """Check if the move is valid (column exists and is not full)."""
    return column.isalpha() and 0 <= ord(column.upper()) - 65 < len(board[0]) and board[0][ord(column.upper()) - 65] == " "

def drop_checker(board, column, checker):
    """Place the checker in the specified column."""
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return

def is_winning_move(board, checker):
    """Check if the last move is a winning move."""
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw (no more valid moves)."""
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialize game
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    # Print initial board
    print_board(board)
    print(f"Player {current_player} starts.")

    while True:
        # Player's turn
        print_board(board)
        move = input(f"Player {current_player}, please enter a column: ").strip()

        # Validate input
        if not is_valid_column(move, board):
            print(f"Invalid move. Try again.")
            continue

        # Drop checker
        drop_checker(board, move, current_player)

        # Check for win
        if is_winning_move(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
