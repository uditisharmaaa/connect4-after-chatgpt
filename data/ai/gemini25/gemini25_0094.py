import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    """
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col_index in range(len(board[0])):
        print(f"{string.ascii_uppercase[col_index]}   ", end="")
    print()

    # Print board rows
    for row_index in range(len(board)):
        print("+---" * len(board[0]) + "+")
        print("|", end="")
        for col_index in range(len(board[0])):
            print(f" {board[row_index][col_index]} |", end="")
        print()
    print("+---" * len(board[0]) + "+")

# --- Game Logic Functions ---

def get_column_from_input(prompt, num_cols):
    """
    Prompts the player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) == 1 and user_input.isalpha():
            col_char = user_input[0]
            col_index = ord(col_char) - ord('A')
            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {string.ascii_uppercase[num_cols - 1]}.")
        else:
            print("Invalid input. Please enter a single uppercase letter (e.g., A, B).")

def place_checker(board, col_index, checker):
    """
    Places the checker in the lowest available space in the specified column.
    Returns True if successful, False if the column is full.
    """
    for row_index in range(len(board) - 1, -1, -1):  # Start from the bottom
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return True
    return False

def check_win(board, checker, win_len):
    """
    Checks if the given checker has won the game.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - win_len + 1):
            if all(board[r][c + i] == checker for i in range(win_len)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - win_len + 1):
            if all(board[r + i][c] == checker for i in range(win_len)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - win_len + 1):
        for c in range(cols - win_len + 1):
            if all(board[r + i][c + i] == checker for i in range(win_len)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(rows - win_len + 1):
        for c in range(win_len - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(win_len)):
                return True
    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # An empty space found, not a draw yet
    return True

# --- Main Game Loop ---

def play_game():
    """
    Runs the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly choose first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = current_players[current_player_index]

    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        col_input = get_column_from_input(f"Player {current_checker}, your turn: ", NUM_COLS)

        if place_checker(board, col_input, current_checker):
            if check_win(board, current_checker, WIN_LENGTH):
                print_board(board)
                print(f"Player {current_checker} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("It's a draw!")
                game_over = True
            else:
                # Next player's turn
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
                current_checker = current_players[current_player_index]
        else:
            print(f"Column {string.ascii_uppercase[col_input]} is full. Please choose another column.")
            # Player does not lose turn if column is full, they are asked again.

if __name__ == "__main__":
    play_game()
