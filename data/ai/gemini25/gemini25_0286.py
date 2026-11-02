import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]


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
    Clears the screen and prints the current state of the Connect 4 board.
    """
    os.system('clear')  # Clear the console

    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS[:len(board[0])]))

    # Print board rows
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")


# --- Game Logic Functions ---
def get_player_input(player_checker, board_cols):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number if valid.
    """
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").upper()

        if not col_input:
            print("Invalid input. Please enter a letter (e.g., A, B).")
            continue

        if col_input not in COLUMN_LABELS[:board_cols]:
            print(f"Invalid column. Please choose from {', '.join(COLUMN_LABELS[:board_cols])}.")
            continue

        col_index = ord(col_input) - ord('A')
        return col_index


def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if the checker was successfully dropped, False otherwise (column full).
    """
    # Iterate from the bottom row up
    for row_index in range(len(board) - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = player_checker
            return True
    return False  # Column is full


def check_win(board, player_checker, win_count):
    """
    Checks if the current player has won the game.
    Returns True if a win is found, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - win_count + 1):
            if all(board[r][c + i] == player_checker for i in range(win_count)):
                return True

    # Check vertical
    for r in range(rows - win_count + 1):
        for c in range(cols):
            if all(board[r + i][c] == player_checker for i in range(win_count)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - win_count + 1):
        for c in range(cols - win_count + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_count)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_count - 1, rows):
        for c in range(cols - win_count + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_count)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is full, indicating a draw.
    Returns True if it's a draw, False otherwise.
    """
    for row in board:
        if " " in row:
            return False  # There's still an empty space
    return True  # Board is full


# --- Main Game Function ---
def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = players[current_player_index]

    game_over = False

    while not game_over:
        print_board(board)
        current_player_checker = players[current_player_index]

        col_index = get_player_input(current_player_checker, NUM_COLS)

        if drop_checker(board, col_index, current_player_checker):
            # Checker was successfully dropped
            if check_win(board, current_player_checker, WIN_CONDITION):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("It's a draw!")
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # Column was full, current player's turn is invalid, they lose the turn
            print("That column is full. Please choose another column.")
            # The current_player_index does NOT change, so the player effectively loses their turn.
            # To rephrase the assignment: "If the column is already completely filled with checkers,
            # the turn is invalid and the player loses the turn." This implies the current player
            # still has to make a valid move. The phrase "the turn is not lost" (for invalid input)
            # and "the player loses the turn" (for full column) are slightly contradictory or
            # ambiguous. Assuming "loses the turn" means the next player plays, but the previous
            # print statement indicates the current player keeps trying until a valid move.
            # Let's interpret "loses the turn" as "the turn ends without a valid placement for that player,
            # and the next player's turn begins".
            # If the interpretation is that they keep trying for a valid column *without* losing the turn,
            # then the current code (not changing current_player_index) for 'full column' is correct.
            # Given the phrasing "the turn is not lost" for *invalid input* but "loses the turn" for *full column*,
            # I will assume that the turn IS lost for a full column, meaning the player index advances.
            # If the user input is invalid, they are asked again *without* the player changing.
            # If the column is full, the player *loses* the turn and the next player plays.
            print("Player " + current_player_checker + " loses this turn.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


# --- Start the Game ---
if __name__ == "__main__":
    play_connect_4()
