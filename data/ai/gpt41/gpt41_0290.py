import os
import random
import string

# ------------------- CONSTANTS -------------------
ROWS = 6                # Number of rows (default 6)
COLUMNS = 7             # Number of columns (default 7, max 26)
PLAYERS = 2             # Number of players (between 2 and 5)

# The checkers for up to 5 players
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# ---------------------------------------------

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')  # Use 'cls' on Windows if testing there

def create_board(rows, cols):
    """Creates an empty board with given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board in the specified format."""
    rows = len(board)
    cols = len(board[0])

    col_labels = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(col_labels)
    print('+' + '---+' * cols)

    for row in board:
        print('|', end='')
        for cell in row:
            print(f" {cell} |", end='')
        print()
        print('+' + '---+' * cols)

def get_valid_columns(board):
    """Returns a list of column indices that can accept another checker."""
    cols = len(board[0])
    valid_cols = []
    for col in range(cols):
        if board[0][col] == " ":
            valid_cols.append(col)
    return valid_cols

def input_column(player_checker, valid_cols):
    """Prompts user to input a valid column letter, validates the input."""
    cols = len(valid_cols)
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip()
        if len(col_input) != 1 or not col_input.isupper():
            print("Invalid input! Please enter a single uppercase letter.")
            continue
        col_idx = ord(col_input) - ord('A')
        if not (0 <= col_idx < COLUMNS):
            print(f"Invalid column! Please choose between A and {string.ascii_uppercase[COLUMNS-1]}.")
            continue
        if board[0][col_idx] != " ":
            print("That column is full! You'll lose your turn.")
            return None   # Return None, and turn will be lost
        return col_idx

def drop_checker(board, col, checker):
    """Drops a checker in the specified column, simulating gravity."""
    rows = len(board)
    for row in reversed(range(rows)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Should never get here if input validation is correct
    return None

def check_win(board, checker):
    """Checks if the given checker has won (4 in a row)."""
    rows = len(board)
    cols = len(board[0])

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            # Check right
            if c + 3 < cols and all(board[r][c+i] == checker for i in range(4)):
                return True
            # Check down
            if r + 3 < rows and all(board[r+i][c] == checker for i in range(4)):
                return True
            # Check diagonal down-right
            if r + 3 < rows and c + 3 < cols and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            # Check diagonal down-left
            if r + 3 < rows and c - 3 >= 0 and all(board[r+i][c-i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    """Checks if the board is full."""
    return all(cell != " " for cell in board[0])

def next_player(current, num_players):
    """Returns the index of the next player."""
    return (current + 1) % num_players

# ------------------- MAIN GAME LOOP -------------------

def play_game():
    # Board and player setup
    board = create_board(ROWS, COLUMNS)
    num_players = PLAYERS
    player_checkers = CHECKERS[:num_players]

    # Randomize starting player
    current_player = random.randint(0, num_players - 1)

    clear_screen()
    print_board(board)
    print(f"Player {player_checkers[current_player]} starts!\n")

    while True:
        valid_cols = get_valid_columns(board)
        # If no valid columns -> draw
        if not valid_cols:
            print("The board is full! It's a draw.")
            break

        # Show the current board
        print_board(board)

        # Prompt input
        col_idx = input_column(player_checkers[current_player], valid_cols)
        if col_idx is None:
            # Column full, lose turn!
            print(f"Player {player_checkers[current_player]} loses this turn!")
        else:
            # Drop checker
            drop_checker(board, col_idx, player_checkers[current_player])
            clear_screen()
            # Check win condition
            if check_win(board, player_checkers[current_player]):
                print_board(board)
                print(f"Player {player_checkers[current_player]} won!")
                break
            # Check draw after move
            if check_draw(board):
                print_board(board)
                print("The board is full! It's a draw.")
                break
        # Next player's turn
        current_player = next_player(current_player, num_players)

if __name__ == "__main__":
    play_game()
