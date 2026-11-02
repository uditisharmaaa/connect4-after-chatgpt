import os
import random

# Constants (changeable for different board sizes or player counts)
ROWS = 6              # Number of rows on the board
COLS = 7              # Number of columns on the board (max 26)
PLAYERS = 2           # Number of players (2 to 5)
WIN_COUNT = 4         # Number of consecutive checkers to win
CHECKERS = ["X", "O", "V", "H", "M"]  # Possible checkers for players

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates an empty board (2D list) filled with spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board to the console with column labels and separators."""
    clear_screen()
    # Print column labels (letters starting from 'A')
    labels = "  " + "   ".join(chr(ord('A') + i) for i in range(COLS))
    print(labels)
    
    # Print rows with separators and spaces
    h_line = "+" + "---+" * COLS
    for row in range(ROWS):
        print(h_line)
        row_str = "|"
        for col in range(COLS):
            row_str += f" {board[row][col]} |"
        print(row_str)
    print(h_line)

def select_starting_player():
    """Randomly select which player starts the game."""
    return random.randint(0, PLAYERS - 1)

def is_valid_column(col_char):
    """Check if the input character corresponds to a valid column."""
    if len(col_char) != 1:
        return False
    col = ord(col_char) - ord('A')
    return 0 <= col < COLS

def get_column_index(col_char):
    """Convert column letter to index."""
    return ord(col_char) - ord('A')

def place_checker(board, col, checker):
    """
    Place the checker in the lowest empty position within the column.
    Return True if placement succeeded, False if the column is full.
    """
    # Start from the bottom row and go up to find empty space
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check if the specified checker has 4 consecutive in any direction."""
    # Check horizontal
    for row in range(ROWS):
        count = 0
        for col in range(COLS):
            if board[row][col] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check vertical
    for col in range(COLS):
        count = 0
        for row in range(ROWS):
            if board[row][col] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - WIN_COUNT + 1):
        for col in range(COLS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[row + i][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(WIN_COUNT - 1, ROWS):
        for col in range(COLS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[row - i][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    return False

def check_draw(board):
    """Check if the board is full with no empty spaces."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def get_player_input(current_player):
    """
    Prompt the player for input and validate it.
    Returns a valid column index or None if the column is full.
    """
    checker = CHECKERS[current_player]
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        if not is_valid_column(user_input):
            # Invalid input, ask again
            continue
        col = get_column_index(user_input)
        return col

def main():
    # Create game board
    board = create_board()

    # Randomly choose starting player
    current_player = select_starting_player()

    # Show initial board
    print_board(board)

    while True:
        checker = CHECKERS[current_player]
        col = get_player_input(current_player)

        # Try to place checker in column; if column full, player loses turn
        if not place_checker(board, col, checker):
            # Inform player about full column and lose turn
            print(f"Column {chr(ord('A') + col)} is full. Player {checker} loses the turn.")
            input("Press Enter to continue...")
            # Advance to next player turn
            current_player = (current_player + 1) % PLAYERS
            print_board(board)
            continue

        # Successfully placed checker, print updated board
        print_board(board)

        # Check if current player won
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The board is full. The game is a draw!")
            break

        # Advance to next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
