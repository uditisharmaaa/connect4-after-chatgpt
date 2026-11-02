import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows=ROWS, cols=COLS):
    # Board is list of lists: board[row][col]
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column letters A-G (or up to max 26)
    col_headers = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(col_headers))
    line = "+" + "---+" * cols
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)

def input_column(player_checker, board):
    cols = len(board[0])
    col_letters = [chr(ord('A') + i) for i in range(cols)]
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()

        # Validate input length and characters
        if len(col_input) != 1 or col_input not in col_letters:
            # Invalid input, prompt again
            continue
        
        col_index = ord(col_input) - ord('A')

        # Check if column is full: if top row is not empty in that column, column full
        if board[0][col_index] != " ":
            # Column full, player loses the turn
            return None
        return col_index

def place_checker(board, col, checker):
    # Place checker in lowest empty space of the column
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col  # Return position placed
    # If we got here, column is full (should not happen due to input checking)
    return None

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Diagonal checks (top-left to bottom-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal checks (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def check_draw(board):
    # If any cell in top row is empty, then not full
    if any(cell == " " for cell in board[0]):
        return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        col = input_column(player_checker, board)
        if col is None:
            # Column full, player loses turn, move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        place_checker(board, col, player_checker)
        print_board(board)

        # Check win
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check draw
        if check_draw(board):
            print("Game is a draw!")
            break

        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
