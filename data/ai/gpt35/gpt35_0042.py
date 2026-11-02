import os
import random

# Constants
ROWS = 6               # Number of rows on the board
COLS = 7               # Number of columns on the board
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_CONDITION = 4      # Number of checkers in a row needed to win

# Players' checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Create a game board filled with spaces.
    :param rows: Number of rows
    :param cols: Number of columns
    :return: 2D list representing the board
    """
    return [[" " for _ in range(cols)] for __ in range(rows)]

def print_board(board):
    """
    Print the game board to the terminal with column labels.
    :param board: 2D list representing the board
    """
    cols = len(board[0])
    rows = len(board)
    # Print column labels (A, B, C, ...)
    labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(labels))
    line = "+" + "---+" * cols
    for r in range(rows):
        print(line)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def is_valid_column(col_letter, board):
    """
    Check if the provided column letter is valid and not full.
    :param col_letter: uppercase letter representing the column
    :param board: 2D list representing the board
    :return: True if column is valid and has space, False otherwise
    """
    cols = len(board[0])
    if len(col_letter) != 1 or not ('A' <= col_letter <= chr(ord('A') + cols - 1)):
        return False
    col_index = ord(col_letter) - ord('A')
    # Check if top cell in column is empty (if not empty, column full)
    return board[0][col_index] == " "

def place_checker(board, col_letter, checker):
    """
    Place the checker in the chosen column, it falls to the lowest empty cell.
    :param board: 2D list representing the board
    :param col_letter: uppercase letter representing the column
    :param checker: the player's checker character
    :return: True if placed successfully, False if column full
    """
    col = ord(col_letter) - ord('A')
    rows = len(board)
    # Start from bottom row upwards and find first empty cell
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    # Column full
    return False

def check_win(board, checker):
    """
    Check if the player with 'checker' has 4 in a row horizontally, vertically or diagonally.
    :param board: 2D list representing the board
    :param checker: checker character to find a win for
    :return: True if win found, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_CONDITION:
                    return True
            else:
                count = 0
    
    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_CONDITION:
                    return True
            else:
                count = 0
    
    # Diagonal check (bottom-left to top-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            # Check 4 diagonal cells
            if all(board[r+i][c+i] == checker for i in range(WIN_CONDITION)):
                return True

    # Diagonal check (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Check if the board is full and it's a draw.
    :param board: 2D list representing the board
    :return: True if board full, False otherwise
    """
    # If any cell in top row is empty, not full
    return all(cell != " " for cell in board[0])

def get_valid_input(board, player_checker):
    """
    Ask the player for input until a valid column is entered.
    :param board: 2D list representing the board
    :param player_checker: current player's checker character
    :return: uppercase column letter or None if column full (lose turn)
    """
    cols = len(board[0])
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(user_input, board):
            print(f"Invalid input. Please enter a column letter between A and {chr(ord('A') + cols - 1)} that is not full.")
            continue
        # Check if we can place a checker in this column
        # If column full, the turn is lost (return None)
        col_index = ord(user_input) - ord('A')
        if board[0][col_index] != " ":
            # Column full => lose turn
            print(f"Column {user_input} is full, you lose your turn.")
            return None
        return user_input

def main():
    # Settings for assignment submission:
    num_players = 2        # Between 2 and 5, fixed to 2 for submission
    rows = ROWS            # Fixed to 6
    cols = COLS            # Fixed to 7

    # Initialize board
    board = create_board(rows, cols)
    
    # Select players' checkers for the game in order
    players = CHECKERS[:num_players]
    
    # Randomly select the starting player index
    current_player_idx = random.randint(0, num_players -1)

    clear_screen()
    print_board(board)

    # Game loop
    while True:
        player_checker = players[current_player_idx]

        # Get player's valid move
        col_choice = get_valid_input(board, player_checker)

        placed = False
        if col_choice is not None:
            # Try placing the checker (should always succeed here)
            placed = place_checker(board, col_choice, player_checker)

        # If player lost turn (could not place) - move on
        if not placed and col_choice is not None:
            # Should never occur because we check for full columns before placement,
            # but if somehow placed is False here, treat as lose turn.
            pass

        clear_screen()
        print_board(board)

        # If checker placed, check win condition
        if placed:
            if check_win(board, player_checker):
                print(f"Player {player_checker} won!")
                break
            # Check for draw
            if check_draw(board):
                print("The game is a draw!")
                break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players


if __name__ == "__main__":
    main()
