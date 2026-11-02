import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Global Variables (initialized later) ---
board = []
players = []
current_player_index = 0

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the empty board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    os.system('clear')  # Clear the screen

    # Print column labels
    col_labels = string.ascii_uppercase[:NUM_COLS]
    print("  " + "   ".join(col_labels))

    # Print board content
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

# --- Game Logic Functions ---

def get_column_from_input(prompt):
    """
    Prompts the player for a column input and validates it.

    Args:
        prompt (str): The message to display to the user.

    Returns:
        int: The 0-based index of the chosen column, or -1 if input is invalid.
    """
    while True:
        user_input = input(prompt).upper()
        if len(user_input) == 1 and user_input in string.ascii_uppercase:
            col_index = ord(user_input) - ord('A')
            if 0 <= col_index < NUM_COLS:
                return col_index
            else:
                print(f"Invalid column: '{user_input}'. Please enter a letter between A and {string.ascii_uppercase[NUM_COLS - 1]}.")
        else:
            print(f"Invalid input: '{user_input}'. Please enter a single uppercase letter (e.g., A).")

def drop_checker(board, col, player_checker):
    """
    Drops a player's checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col (int): The 0-based index of the column to drop the checker into.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = player_checker
            return True
    return False

def check_win(board, player_checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal wins
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical wins
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check positive diagonal wins (bottom-left to top-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check negative diagonal wins (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Loop ---

def main():
    global board, players, current_player_index

    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    game_over = False
    winner = None

    while not game_over:
        print_board(board)
        current_player_checker = players[current_player_index]
        print(f"Player {current_player_checker}, it's your turn.")

        col_input = -1
        while col_input == -1:
            col_input = get_column_from_input(f"Player {current_player_checker}, please enter a column: ")
            if col_input != -1 and not drop_checker(board, col_input, current_player_checker):
                print(f"Column {string.ascii_uppercase[col_input]} is full. Please choose another column.")
                col_input = -1 # Reset to ask for input again

        if check_win(board, current_player_checker):
            print_board(board)
            winner = current_player_checker
            game_over = True
        elif check_draw(board):
            print_board(board)
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print_board(board)
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
