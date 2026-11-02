import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5

# Number of players for this submission (2 players)
NUM_PLAYERS = 2

# Checkers for players in order
CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    board = []
    for _ in range(rows):
        board.append([" "] * columns)
    return board


def print_board(board):
    clear_screen()
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(headers))
    # Print the board rows with borders
    for row in board:
        print("+" + "---+" * len(row))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * len(board[0]))


def get_player_input(player_checker, board):
    columns = len(board[0])
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ")
        if len(col_input) != 1:
            # Invalid input length
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        if not col_input.isalpha() or not col_input.isupper():
            # Not a valid uppercase letter
            print("Invalid input. Please enter an uppercase letter for a column.")
            continue
        col_index = ord(col_input) - ord('A')
        if col_index < 0 or col_index >= columns:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + columns - 1)}.")
            continue
        # Check if column is full
        if board[0][col_index] != " ":
            # Column full - player loses turn (as per assignment)
            print(f"Column {col_input} is full. You lose your turn.")
            return None
        return col_index


def place_checker(board, col, checker):
    rows = len(board)
    # Place checker at the lowest empty space in the column
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col  # Return position where placed


def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])
    needed = 4

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == needed:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == needed:
                    return True
            else:
                count = 0

    # Diagonal (left-top to right-bottom)
    for r in range(rows - needed + 1):
        for c in range(cols - needed + 1):
            win = True
            for i in range(needed):
                if board[r + i][c + i] != checker:
                    win = False
                    break
            if win:
                return True

    # Diagonal (right-top to left-bottom)
    for r in range(rows - needed + 1):
        for c in range(needed - 1, cols):
            win = True
            for i in range(needed):
                if board[r + i][c - i] != checker:
                    win = False
                    break
            if win:
                return True

    return False


def check_draw(board):
    # If top row has no empty spaces, board is full
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True


def main():
    # Initialize board
    board = create_board(ROWS, COLUMNS)

    # Set players according to number of players
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        col_index = get_player_input(current_checker, board)
        if col_index is None:
            # Lost turn due to full column, move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        place_checker(board, col_index, current_checker)
        print_board(board)

        # Check win
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
