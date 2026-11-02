import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4

# Players and their checkers in order
PLAYERS_SYMBOLS = ["X", "O", "V", "H", "M"]

# Configuration for this assignment submission
NUMBER_OF_PLAYERS = 2


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    columns = len(board[0])
    rows = len(board)
    # Print column labels
    headers = [chr(ord('A') + i) for i in range(columns)]
    print("  " + "   ".join(headers))
    # Print board rows
    for row in range(rows):
        print("+" + "---+" * columns)
        print("|" + "|".join(f" {board[row][col]} " for col in range(columns)) + "|")
    print("+" + "---+" * columns)


def is_valid_column_input(col_str, columns):
    if len(col_str) != 1:
        return False
    if not ('A' <= col_str <= chr(ord('A') + columns - 1)):
        return False
    return True


def find_drop_row(board, col):
    """
    Returns the row index where the checker falls in the given column.
    Returns None if the column is full.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            return row
    return None


def place_checker(board, col, checker):
    row = find_drop_row(board, col)
    if row is not None:
        board[row][col] = checker
        return True
    return False


def check_line_win(line, checker):
    count = 0
    for cell in line:
        if cell == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    return False


def check_win(board, checker):
    rows = len(board)
    columns = len(board[0])

    # Check horizontal
    for r in range(rows):
        if check_line_win(board[r], checker):
            return True

    # Check vertical
    for c in range(columns):
        column_line = [board[r][c] for r in range(rows)]
        if check_line_win(column_line, checker):
            return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(columns - WIN_LENGTH + 1):
            diag = [board[r + i][c + i] for i in range(WIN_LENGTH)]
            if all(cell == checker for cell in diag):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(columns - WIN_LENGTH + 1):
            diag = [board[r - i][c + i] for i in range(WIN_LENGTH)]
            if all(cell == checker for cell in diag):
                return True

    return False


def check_draw(board):
    return all(cell != " " for row in board for cell in row)


def main():
    # Validate constants
    if not (2 <= NUMBER_OF_PLAYERS <= 5):
        print(f"Error: NUMBER_OF_PLAYERS must be between 2 and 5.")
        return
    if not (ROWS >= WIN_LENGTH and COLUMNS >= WIN_LENGTH):
        print(f"Error: Board must be at least {WIN_LENGTH}x{WIN_LENGTH} for a valid game.")
        return
    if COLUMNS > MAX_COLUMNS:
        print(f"Error: Columns exceeded max allowed {MAX_COLUMNS}.")
        return

    board = create_board(ROWS, COLUMNS)
    players = PLAYERS_SYMBOLS[:NUMBER_OF_PLAYERS]

    current_player_idx = random.randint(0, NUMBER_OF_PLAYERS - 1)

    print_board(board)

    while True:
        player = players[current_player_idx]
        prompt = f"Player {player}, please enter a column: "

        # Input loop for a valid column input or a skipped turn when column full
        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_column_input(user_input, COLUMNS):
                prompt = f"Invalid input. Player {player}, please enter a valid column letter (A-{chr(ord('A') + COLUMNS - 1)}): "
                continue
            col = ord(user_input) - ord('A')
            # Try to place checker
            if place_checker(board, col, player):
                break
            else:
                # Column full -> turn lost
                # Inform player and break to next player
                print(f"Column {user_input} is full. Player {player} loses this turn.")
                break

        print_board(board)

        # Check if checker was placed (didn't lose turn)
        placed = board[find_drop_row(board, col)+1][col] == player if find_drop_row(board, col) is not None else False
        # Instead of above complicated check, simpler: check if place_checker succeeded above break. We've already broken if success.

        # If checker placed (meaning turn was not lost), check win and draw condition
        # Actually, must check win only if checker placed.
        # We can detect if checker was placed by checking if board contains player's checker increased by 1 compared to previous
        # But that is complicated. Since we try place_checker and break only if successful, here is what we can do:
        # So if the last place_checker succeeded, check win. Otherwise, just continue.

        # Slightly changed approach: If place_checker failed, turn lost, so no checker placed. We broke out.
        # So, place_checker succeeded if we are here after breaking from while True input loop.

        # So to manage this properly, restructure input logic:

    # The above code will skip ending game check if turn was lost,
    # Need to rewrite game loop carefully:

def improved_main():
    if not (2 <= NUMBER_OF_PLAYERS <= 5):
        print(f"Error: NUMBER_OF_PLAYERS must be between 2 and 5.")
        return
    if not (ROWS >= WIN_LENGTH and COLUMNS >= WIN_LENGTH):
        print(f"Error: Board must be at least {WIN_LENGTH}x{WIN_LENGTH} for a valid game.")
        return
    if COLUMNS > MAX_COLUMNS:
        print(f"Error: Columns exceeded max allowed {MAX_COLUMNS}.")
        return

    board = create_board(ROWS, COLUMNS)
    players = PLAYERS_SYMBOLS[:NUMBER_OF_PLAYERS]

    current_player_idx = random.randint(0, NUMBER_OF_PLAYERS - 1)

    print_board(board)

    while True:
        player = players[current_player_idx]
        prompt = f"Player {player}, please enter a column: "
        # Input loop for valid input
        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_column_input(user_input, COLUMNS):
                prompt = f"Invalid input. Player {player}, please enter a valid column letter (A-{chr(ord('A') + COLUMNS - 1)}): "
                continue
            col = ord(user_input) - ord('A')
            drop_row = find_drop_row(board, col)
            if drop_row is None:
                # Column full: player loses the turn, no input retry
                print(f"Column {user_input} is full. Player {player} loses this turn.")
                break
            # Place checker and continue
            board[drop_row][col] = player
            break

        print_board(board)

        # Check for win only if checker placed in this turn (drop_row != None)
        if drop_row is not None:
            if check_win(board, player):
                print(f"Player {player} won!")
                return
            if check_draw(board):
                print("The game is a draw!")
                return

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUMBER_OF_PLAYERS


if __name__ == "__main__":
    improved_main()
