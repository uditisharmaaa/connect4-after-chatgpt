import os
import random
import string

# ----- CONSTANTS -----
ROWS = 6                   # Number of rows for default board
COLUMNS = 7                # Number of columns for default board
MAX_COLUMNS = 26           # Max columns limited by English alphabet
PLAYERS = 2                # Number of players (2 - 5 supported)

CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYER_CHECKERS = CHECKERS[:PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLUMNS])

# ----- FUNCTIONS -----

def clear_screen():
    """Clears the terminal."""
    os.system('clear')

def create_board(rows, cols):
    """Creates and returns an initial board with all spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board with column labels and lines."""
    clear_screen()
    # Print Column Headers
    print("  " + '   '.join(COLUMN_LABELS))
    print("+" + "---+"*COLUMNS)
    # Print Board Rows
    for row in board:
        print("| " + ' | '.join(row) + " |")
        print("+" + "---+"*COLUMNS)

def is_column_valid(column_input, board):
    """Checks if user input is a valid column and if not full."""
    if len(column_input) != 1 or column_input not in COLUMN_LABELS:
        return False, "Not a valid column label."
    col_index = COLUMN_LABELS.index(column_input)
    if board[0][col_index] != ' ':
        return False, "Column is full."
    return True, ""

def get_player_input(player_checker, board):
    """Prompts player for input and validates it."""
    while True:
        choice = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        valid, error_message = is_column_valid(choice, board)
        if not valid:
            print(error_message)
            continue
        return COLUMN_LABELS.index(choice)

def drop_checker(board, player_checker, col):
    """Drops the player's checker in the lowest available position in a column."""
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player_checker
            return row, col
    return None, None  # Should not reach here if validation is correct

def check_winner(board, player_checker):
    """Checks if the player has four in a row somewhere on the board."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player_checker for i in range(4)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_checker for i in range(4)):
                return True
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_checker for i in range(4)):
                return True
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_checker for i in range(4)):
                return True
    return False

def is_draw(board):
    """Checks if the board is full, leading to a draw."""
    return all(cell != ' ' for cell in board[0])

def switch_player(current_index, num_players):
    """Returns the next player's index."""
    return (current_index + 1) % num_players

def main():
    # Initialization
    board = create_board(ROWS, COLUMNS)
    player_indices = list(range(PLAYERS))
    current_player = random.choice(player_indices)

    print_board(board)
    print(f"Player {PLAYER_CHECKERS[current_player]} starts!")
    input("Press Enter to begin...")

    # Game Loop
    moves_played = 0
    while True:
        print_board(board)
        player_checker = PLAYER_CHECKERS[current_player]

        # Get and process player input
        col = get_player_input(player_checker, board)
        row, col = drop_checker(board, player_checker, col)
        moves_played += 1

        # Check for a winner
        if check_winner(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Next player
        current_player = switch_player(current_player, PLAYERS)

if __name__ == '__main__':
    main()
