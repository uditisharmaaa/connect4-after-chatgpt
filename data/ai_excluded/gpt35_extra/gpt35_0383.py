import os
import random
import string

# Constants for the game setup
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
NUM_PLAYERS = 2  # must be between MIN_PLAYERS and MAX_PLAYERS
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers (A-G)
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    line = "+" + "---+" * cols
    for row in board:
        print(line)
        # Print each row with vertical bars
        print("| " + " | ".join(row) + " |")
    print(line)


def get_valid_column_input(board, player_checker):
    cols = len(board[0])
    valid_letters = string.ascii_uppercase[:cols]
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            # Invalid length
            continue
        if inp not in valid_letters:
            # Not a valid column letter
            continue
        col = valid_letters.index(inp)
        # Check if column is full, if yes player loses turn
        if board[0][col] != " ":
            # The top cell is occupied; column full
            return None  # Special value meaning turn lost
        return col


def place_checker(board, col, checker):
    # Place checker in the lowest free row in the chosen column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col  # Return position where placed
    # Should not reach here if called properly (check done before)
    return None, None


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal checks
    # \ diagonal
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # / diagonal
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False


def board_full(board):
    # If any top row cell is empty, board is not full
    return all(cell != " " for cell in board[0])


def main():
    # Setup
    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randrange(NUM_PLAYERS)
    print_board(board)
    # Start game loop
    while True:
        player_checker = players[current_player_index]
        col = get_valid_column_input(board, player_checker)
        if col is None:
            # Player loses turn, do not place checker, print board and move on
            print_board(board)
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        # Place checker in board
        row_placed, col_placed = place_checker(board, col, player_checker)
        print_board(board)
        # Check win
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        # Check draw
        if board_full(board):
            print("The game is a draw.")
            break
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
