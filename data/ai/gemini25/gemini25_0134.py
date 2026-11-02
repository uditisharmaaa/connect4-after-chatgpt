import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LENGTH = 4

# --- Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    """
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f"   {string.ascii_uppercase[col_index]}", end="")
    print()

    # Print the board with separators
    for row_index in range(len(board)):
        print(" +", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()
        print(" |", end="")
        for col_index in range(len(board[0])):
            print(f" {board[row_index][col_index]} |", end="")
        print()
    
    # Print the bottom separator
    print(" +", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()


def get_column_input(player_checker, num_cols):
    """
    Gets and validates column input from the player.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_letter = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_letter) != 1 or col_letter not in string.ascii_uppercase[:num_cols]:
                print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
                continue
            
            col_index = ord(col_letter) - ord('A')
            return col_index
        except Exception:
            print("Invalid input. Please enter a single uppercase letter.")


def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    for row_index in range(len(board) - 1, -1, -1):  # Start from bottom row
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = player_checker
            return True
    return False # Column is full

def check_win(board, player_checker, win_length):
    """
    Checks if the current player has won the game.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - win_length + 1):
            if all(board[r][c + i] == player_checker for i in range(win_length)):
                return True

    # Check vertical
    for r in range(rows - win_length + 1):
        for c in range(cols):
            if all(board[r + i][c] == player_checker for i in range(win_length)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - win_length + 1):
        for c in range(cols - win_length + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_length)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_length - 1, rows):
        for c in range(cols - win_length + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_length)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for row in board:
        if " " in row:
            return False
    return True

def play_connect_4():
    """
    Main function to play the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        player_checker = CHECKERS[current_player_index]
        print_board(board)

        valid_move = False
        while not valid_move:
            col_index = get_column_input(player_checker, NUM_COLS)
            
            if col_index < 0 or col_index >= NUM_COLS:
                print(f"Column '{string.ascii_uppercase[col_index]}' is out of bounds. Please choose a column between A and {string.ascii_uppercase[NUM_COLS-1]}.")
            elif not drop_checker(board, col_index, player_checker):
                print(f"Column {string.ascii_uppercase[col_index]} is full. Please choose another column.")
            else:
                valid_move = True

        # Check for win after a valid move
        if check_win(board, player_checker, WIN_LENGTH):
            print_board(board)
            print(f"Player {player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# --- Game Start ---
if __name__ == "__main__":
    play_connect_4()
