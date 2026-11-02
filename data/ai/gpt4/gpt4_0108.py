import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
CHECKER_SYMBOLS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLS)]  # A, B, C, ...

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Create a board with specified dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    print("  " + "   ".join(COLUMN_LABELS[:len(board[0])]))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def is_valid_column(column, board):
    """Check if the column input is valid."""
    if column not in COLUMN_LABELS:
        return False
    col_idx = COLUMN_LABELS.index(column)
    return any(row[col_idx] == " " for row in board)

def get_empty_row(column, board):
    """Get the index of the lowest empty row in a column."""
    col_idx = COLUMN_LABELS.index(column)
    for row_idx in reversed(range(len(board))):
        if board[row_idx][col_idx] == " ":
            return row_idx
    return None

def place_checker(column, checker, board):
    """Place a checker in the chosen column."""
    row_idx = get_empty_row(column, board)
    col_idx = COLUMN_LABELS.index(column)
    board[row_idx][col_idx] = checker

def check_win(board, checker):
    """Check if a player has won the game."""
    rows, cols = len(board), len(board[0])

    # Check horizontal win
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == checker and all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical win
    for c in range(cols):
        for r in range(rows - 3):
            if board[r][c] == checker and all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == checker and all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if board[r][c] == checker and all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw (no empty cells)."""
    return all(cell != " " for row in board for cell in row)

def switch_player(current_player, total_players):
    """Switch to the next player."""
    return (current_player + 1) % total_players

def main():
    # Setup game
    clear_screen()
    board = create_board(ROWS, COLS)
    num_players = 2
    players = CHECKER_SYMBOLS[:num_players]
    current_player = random.randint(0, num_players - 1)

    # Game loop
    while True:
        clear_screen()
        print_board(board)
        print(f"Player {players[current_player]}'s turn")
        column = input("Please enter a column: ").strip().upper()

        if not is_valid_column(column, board):
            print("Invalid column. Try again.")
            input("Press Enter to continue...")
            continue

        place_checker(column, players[current_player], board)

        # Check for win or draw
        if check_win(board, players[current_player]):
            clear_screen()
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Switch player
        current_player = switch_player(current_player, num_players)

if __name__ == "__main__":
    main()
