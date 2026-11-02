import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create an empty board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board state."""
    os.system('clear')  # Clear the terminal screen
    # Print column labels
    col_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))  # A, B, C...
    print(col_labels)

    # Print board rows
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def get_valid_column(board, column_input):
    """Convert and validate the column input."""
    if len(column_input) != 1 or not column_input.isalpha():
        return None
    col = ord(column_input.upper()) - ord('A')
    if 0 <= col < len(board[0]) and board[0][col] == " ":
        return col
    return None

def drop_checker(board, col, checker):
    """Drop a checker into the specified column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current player has won."""
    # Horizontal check
    for row in board:
        for col in range(len(row) - 3):
            if all(cell == checker for cell in row[col:col+4]):
                return True

    # Vertical check
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal check (\ direction)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Diagonal check (/ direction)
    for row in range(len(board) - 3):
        for col in range(3, len(board[0])):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full."""
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialize game settings
    board = create_board(ROWS, COLS)
    num_players = 2  # Number of players (can be changed)
    player_checkers = CHECKERS[:num_players]

    # Randomly select the first player
    current_player = random.randint(0, num_players - 1)

    # Game loop
    while True:
        # Display the board
        print_board(board)

        # Current player's turn
        print(f"Player {player_checkers[current_player]}'s turn:")
        column_input = input("Please enter a column (A-G): ")

        # Validate input and update board
        col = get_valid_column(board, column_input)
        if col is None:
            print("Invalid input. Please try again.")
            input("Press Enter to continue...")
            continue
        
        drop_checker(board, col, player_checkers[current_player])

        # Check for a win
        if check_win(board, player_checkers[current_player]):
            print_board(board)
            print(f"Player {player_checkers[current_player]} won!")
            break

        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
