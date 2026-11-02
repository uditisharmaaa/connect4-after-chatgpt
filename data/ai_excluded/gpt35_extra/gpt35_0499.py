import os
import random
import string

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers
    headers = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(headers))
    # Print rows
    for row in board:
        print("+" + "---+" * cols)
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * cols)

def choose_starting_player(num_players):
    return random.randint(0, num_players - 1)

def input_valid_column(input_str, cols):
    if len(input_str) != 1:
        return False
    letter = input_str.upper()
    if letter not in string.ascii_uppercase[:cols]:
        return False
    return True

def column_index(letter):
    return string.ascii_uppercase.index(letter.upper())

def place_checker(board, col, checker):
    """
    Attempts to place checker in the column.
    Returns True if successful, False if column full.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c+i] == checker for i in range(WIN_COUNT)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r+i][c] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal \ check
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal / check
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = choose_starting_player(NUM_PLAYERS)

    # Show empty board with chosen player to start
    print_board(board)

    while True:
        checker = players[current_player]
        print(f"Player {checker}, please enter a column:")

        while True:
            user_input = input().strip().upper()
            if not input_valid_column(user_input, COLS):
                print(f"Invalid input. Please enter a letter between A and {string.ascii_uppercase[COLS-1]}:")
                continue

            col = column_index(user_input)
            # Try to place checker
            if not place_checker(board, col, checker):
                # Column full -> turn lost
                print(f"Column {user_input} is full. Turn lost.")
                break
            else:
                # Successful placement, break for next phase
                break

        print_board(board)

        # If checker was placed successfully, check win and draw
        if board[row][col] == checker:  # means place_checker succeeded
            if check_winner(board, checker):
                print(f"Player {checker} won!")
                return
            if board_full(board):
                print("The game is a draw!")
                return

        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
