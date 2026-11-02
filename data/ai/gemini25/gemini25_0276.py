import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns supported by label generation
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Board Initialization and Display ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def get_column_labels(cols):
    """
    Generates uppercase letter labels for columns (A, B, C, ...).
    """
    return [chr(ord('A') + i) for i in range(cols)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    """
    os.system('clear')  # Clear the screen

    column_labels = get_column_labels(len(board[0]))
    print("  " + "   ".join(column_labels))
    print("+---" * len(board[0]) + "+")

    for row in board:
        row_str = "|"
        for cell in row:
            row_str += f" {cell} |"
        print(row_str)
        print("+---" * len(board[0]) + "+")

# --- Game Logic ---

def get_player_input(player_checker, board):
    """
    Prompts the current player for a column choice and validates the input.
    Returns the 0-indexed column number.
    """
    column_labels = get_column_labels(len(board[0]))
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()

        if not user_input:
            print("Invalid input. Please enter a column letter (e.g., A).")
            continue

        if user_input not in column_labels:
            print(f"Invalid column. Please enter a letter from {column_labels[0]} to {column_labels[-1]}.")
            continue

        col_index = column_labels.index(user_input)

        if board[0][col_index] != " ":
            print(f"Column {user_input} is full. Please choose another column.")
            continue

        return col_index

def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if the checker was dropped, False if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True
    return False # Should not be reached if get_player_input validates correctly

def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.
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

    # Check positive diagonal (bottom-left to top-right)
    for r in range(rows - win_condition + 1):
        for c in range(cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(win_condition - 1, rows):
        for c in range(cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full (a draw).
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Function ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Player {PLAYER_CHECKERS[current_player_index]} goes first!")

    game_over = False

    while not game_over:
        player_checker = PLAYER_CHECKERS[current_player_index]

        col_index = get_player_input(player_checker, board)
        
        # Drop checker only after valid input (column not full)
        drop_checker(board, col_index, player_checker)
        
        print_board(board)

        if check_win(board, player_checker, WIN_CONDITION):
            print(f"Player {player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full! It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_connect_4()
