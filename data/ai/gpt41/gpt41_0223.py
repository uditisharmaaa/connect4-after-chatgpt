import os
import random
import string

# -------------- CONSTANTS --------------
ROWS = 6                     # Number of rows (default: 6)
COLS = 7                     # Number of columns (default: 7; Max 26)
PLAYERS = 2                  # Number of players (between 2 and 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']   # Checkers assigned to players, in order

# -------------- GAME FUNCTIONS --------------

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    """Creates a new game board initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board with proper formatting."""
    clear_screen()
    cols = len(board[0])
    # Print column labels
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(letters))
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_columns(board):
    """Returns a list of columns (indices) that are not full."""
    valid_cols = []
    for col in range(len(board[0])):
        if board[0][col] == ' ':
            valid_cols.append(col)
    return valid_cols

def get_player_input(player_checker, board):
    """Prompts the current player for valid column input."""
    cols = len(board[0])
    valid_letters = [string.ascii_uppercase[i] for i in range(cols)]
    valid_cols = get_valid_columns(board)
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in valid_letters:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = valid_letters.index(inp)
        if col not in valid_cols:
            if board[0][col] != ' ':
                print("Column is full. You lose your turn!")
                return None
            else:
                print("Invalid move. Try again.")
                continue
        return col

def drop_checker(board, col, checker):
    """Places the checker in the specified column at the lowest available row."""
    rows = len(board)
    for row in reversed(range(rows)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Should not reach here if column not full

def is_winner(board, checker):
    """Checks if the last move by the player with `checker` has won the game."""
    rows = len(board)
    cols = len(board[0])

    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Diagonal (\)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # Diagonal (/)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    """Checks if the board is completely filled (draw)."""
    return all(cell != ' ' for cell in board[0])

def main():
    # Constants
    rows = ROWS
    cols = COLS
    num_players = PLAYERS
    checkers = CHECKERS[:num_players]

    # Board initialization
    board = create_board(rows, cols)

    # Randomly choose starting player
    current_player = random.randint(0, num_players - 1)

    # Show empty board and start player
    print_board(board)
    print(f"Player {checkers[current_player]} starts!\n")
    input("Press Enter to start...")

    # Game loop
    while True:
        print_board(board)

        # Prompt player's move
        col = get_player_input(checkers[current_player], board)
        if col is None:
            # Player loses turn if column is full
            current_player = (current_player + 1) % num_players
            continue

        drop_checker(board, col, checkers[current_player])

        # Check win
        if is_winner(board, checkers[current_player]):
            print_board(board)
            print(f"Player {checkers[current_player]} won!")
            break

        # Check draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % num_players

# -------------- ENTRY POINT --------------
if __name__ == "__main__":
    main()
