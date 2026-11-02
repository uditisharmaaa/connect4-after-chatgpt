import os
import random

# Constants for board dimensions and gameplay
ROWS = 6        # Number of rows on the board
COLUMNS = 7     # Number of columns on the board (max 26)
PLAYERS = 2     # Number of players (between 2 and 5)

# Checkers assigned to players in order
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """
    Create an empty game board as a list of lists filled with spaces.
    Board dimension: rows x columns
    """
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """
    Print the current board to the terminal.
    Columns are labeled A, B, C, ... with '+' and '-' borders as shown in example.
    """
    clear_screen()
    columns = len(board[0])
    rows = len(board)
    
    # Print column headers (A, B, C, ...)
    header = "  "
    for col in range(columns):
        header += "  " + chr(ord('A') + col) + " "
    print(header)
    
    # Print the board rows with borders
    horizontal_border = "+" + "---+" * columns
    for row in range(rows):
        print(horizontal_border)
        row_str = "|"
        for col in range(columns):
            row_str += " " + board[row][col] + " |"
        print(row_str)
    print(horizontal_border)

def is_valid_input(user_input, board, current_player):
    """
    Check if the user input is a single uppercase letter within board columns.
    Also checks if the chosen column is not completely full.
    """
    if len(user_input) != 1:
        return False
    if not ('A' <= user_input <= chr(ord('A') + len(board[0]) - 1)):
        return False
    col = ord(user_input) - ord('A')
    # If the top row in that column is occupied, column is full
    if board[0][col] != " ":
        return False
    return True

def place_checker(board, col, checker):
    """
    Place the checker in the lowest available spot in column col.
    Returns True if placed successfully, False if column full.
    """
    rows = len(board)
    # start checking from bottom row upwards
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    # Column is full
    return False

def check_winner(board, checker):
    """
    Check if the player with 'checker' has 4 in a row in any direction.
    Returns True if winner found, else False.
    """
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for row in range(rows):
        for col in range(cols - 3):
            if board[row][col] == checker and \
               board[row][col+1] == checker and \
               board[row][col+2] == checker and \
               board[row][col+3] == checker:
                return True

    # Vertical check
    for col in range(cols):
        for row in range(rows - 3):
            if board[row][col] == checker and \
               board[row+1][col] == checker and \
               board[row+2][col] == checker and \
               board[row+3][col] == checker:
                return True

    # Diagonal check (down-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if board[row][col] == checker and \
               board[row+1][col+1] == checker and \
               board[row+2][col+2] == checker and \
               board[row+3][col+3] == checker:
                return True

    # Diagonal check (down-left)
    for row in range(rows - 3):
        for col in range(3, cols):
            if board[row][col] == checker and \
               board[row+1][col-1] == checker and \
               board[row+2][col-2] == checker and \
               board[row+3][col-3] == checker:
                return True

    return False

def check_draw(board):
    """
    Check if the board is full with no empty spaces left.
    If full return True, else False.
    """
    # If any cell in top row is empty, the game is not a draw yet
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    return True

def main():
    # Initialize the board
    board = create_board(ROWS, COLUMNS)

    # Prepare players and their checkers (subset of first PLAYERS checkers)
    players_checkers = CHECKERS[:PLAYERS]

    # Randomly select the first player (index)
    current_player_index = random.randint(0, PLAYERS - 1)

    # Print initial board
    print_board(board)

    while True:
        current_checker = players_checkers[current_player_index]
        # Prompt player input until valid or column full
        while True:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()

            # Validate user input format and column availability
            if not is_valid_input(user_input, board, current_checker):
                # If column is full, player loses turn (break input loop)
                if len(user_input) == 1 and 'A' <= user_input <= chr(ord('A') + COLUMNS - 1):
                    col_index = ord(user_input) - ord('A')
                    # Check if column is full
                    if board[0][col_index] != " ":
                        # Column full - turn lost
                        break
                print("Invalid input. Please enter a valid column letter that is not full.")
                continue
            else:
                break

        # If user_input invalid due to column full and break-out, no move made
        if is_valid_input(user_input, board, current_checker):
            col_to_place = ord(user_input) - ord('A')
            placed = place_checker(board, col_to_place, current_checker)
            # If could not place because column full, lose turn (no move)
            if not placed:
                # lose turn automatically, do nothing
                pass

        # Print updated board
        print_board(board)

        # Check if current player won
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check if draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
