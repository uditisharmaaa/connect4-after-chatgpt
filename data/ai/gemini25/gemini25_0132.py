import os
import random
import string

# --- Global Constants (Adjust these for different game setups) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]  # Limit checkers based on NUM_PLAYERS
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Board Initialization and Printing ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board filled with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Clears the screen and prints the Connect 4 board with column labels.
    """
    os.system('clear')  # Clear the terminal screen

    # Print column labels (A, B, C, ...)
    col_labels = string.ascii_uppercase[:len(board[0])]
    print("  " + "   ".join(col_labels))

    # Print top border
    print("+" + "---+".join([""] * len(board[0])))

    # Print rows with checkers and separators
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+".join([""] * len(board[0])))

# --- Game Logic ---

def get_player_input(player_checker, board_cols):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    col_labels = string.ascii_uppercase[:board_cols]
    while True:
        try:
            user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
            
            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = col_labels.find(user_input)

            if col_index == -1:
                print(f"Invalid column '{user_input}'. Please choose from {', '.join(col_labels)}.")
            else:
                return col_index
        except Exception:
            print("An unexpected error occurred. Please try again.")


def place_checker(board, col, player_checker):
    """
    Places the player's checker in the lowest available space in the given column.
    Returns True if the checker was placed successfully, False if the column is full.
    """
    for row in range(len(board) - 1, -1, -1):  # Iterate from bottom to top
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    return False  # Column is full

def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won horizontally, vertically, or diagonally.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - win_condition + 1):
            if all(board[r][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - win_condition + 1):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - win_condition + 1):
        for c in range(cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_condition - 1, rows):
        for c in range(cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for row in board:
        if " " in row:
            return False  # There's an empty space, not a draw yet
    return True  # Board is full

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_checker = None

    print_board(board)
    print(f"Player {CHECKERS[current_player_index]} goes first!")

    while not game_over:
        player_checker = CHECKERS[current_player_index]

        col_input_valid = False
        while not col_input_valid:
            chosen_col_index = get_player_input(player_checker, NUM_COLS)
            if place_checker(board, chosen_col_index, player_checker):
                col_input_valid = True
            else:
                print(f"Column {string.ascii_uppercase[chosen_col_index]} is full. Please choose another column.")
        
        print_board(board)

        if check_win(board, player_checker, WIN_CONDITION):
            winner_checker = player_checker
            game_over = True
        elif check_draw(board):
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_game()
