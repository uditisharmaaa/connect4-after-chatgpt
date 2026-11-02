import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
WIN_CONDITION = 4
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

def create_board(rows, columns):
    """Creates a 2D list representing the Connect 4 board."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the terminal
    column_labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:len(board[0])]
    print("  "+"   ".join(column_labels))
    print("+" + "---+"*len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+"*len(board[0]))

def is_valid_column(column, columns, board):
    """Checks if a given column input is valid (in bounds and not full)."""
    return column.isalpha() and 0 <= ord(column.upper()) - ord('A') < columns and \
           board[0][ord(column.upper()) - ord('A')] == ' '

def get_lowest_empty_row(column, board):
    """Finds the lowest empty row in a column."""
    column_index = ord(column.upper()) - ord('A')
    for row in range(len(board)-1, -1, -1):
        if board[row][column_index] == " ":
            return row
    return -1

def drop_checker(column, player_token, board):
    """Places the current player's checker in the selected column."""
    row = get_lowest_empty_row(column, board)
    col = ord(column.upper()) - ord('A')
    if row != -1:
        board[row][col] = player_token
        return True
    return False

def check_win(board, token):
    """Checks if the current player has won."""
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r][c+i] == token for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_CONDITION + 1):
            if all(board[r+i][c] == token for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (down-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r+i][c+i] == token for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (up-right)
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r-i][c+i] == token for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """Checks if the board is full, resulting in a draw."""
    return all(cell != " " for row in board for cell in row)

def connect_four():
    """Main game loop for Connect 4."""
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_TOKENS[:2]  # Configure for 2 players
    current_player = random.randint(0, len(players) - 1)

    print_board(board)
    print(f"Player {players[current_player]} starts!")

    while True:
        print_board(board)
        column = input(f"Player {players[current_player]}, please enter a column: ").strip().upper()

        if not is_valid_column(column, COLUMNS, board):
            print("Invalid input! Please choose a valid column.")
            continue

        if not drop_checker(column, players[current_player], board):
            print("Column is full! Please choose another column.")
            continue

        # Check for win
        if check_win(board, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % len(players)

if __name__ == "__main__":
    connect_four()
