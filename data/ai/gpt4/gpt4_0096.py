import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checker symbols for up to 5 players
COLUMN_LETTERS = [chr(i) for i in range(65, 65 + COLUMNS)]  # ['A', 'B', 'C', ..., 'G']

def create_board():
    """Creates the game board with empty spaces."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the Connect 4 board."""
    os.system('clear')  # Clear the screen
    print(f"  {'   '.join(COLUMN_LETTERS[:COLUMNS])}")
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_column_index(col_input):
    """Converts column letter to index."""
    if col_input in COLUMN_LETTERS[:COLUMNS]:
        return COLUMN_LETTERS.index(col_input)
    return -1

def is_valid_move(board, col_index):
    """Checks if the move is valid (column is within bounds and not full)."""
    return 0 <= col_index < COLUMNS and board[0][col_index] == ' '

def place_checker(board, col_index, checker):
    """Places the checker in the correct row of the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row, col_index

def check_win(board, checker):
    """Checks if the given checker has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the board is full and no moves are possible."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    # Initialize the game
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)
    print("Welcome to Connect 4!")
    print_board(board)

    # Main game loop
    while True:
        current_player = players[current_player_idx]
        print(f"Player {current_player}, it's your turn.")
        
        # Get user input and validate
        while True:
            col_input = input("Please enter a column: ").strip().upper()
            col_index = get_column_index(col_input)
            if is_valid_move(board, col_index):
                break
            print("Invalid move. Try again.")

        # Place the checker
        place_checker(board, col_index, current_player)
        print_board(board)

        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch player
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
