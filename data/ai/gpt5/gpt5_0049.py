import os
import random

# Constants (you can change these for testing; submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4  # Always 4 in a row to win

# Safety checks for constants
if COLS > 26:
    COLS = 26
if NUM_PLAYERS < 2:
    NUM_PLAYERS = 2
if NUM_PLAYERS > 5:
    NUM_PLAYERS = 5

# Global board (list of lists)
board = []


def clear_screen():
    # Clear the terminal (Linux/macOS)
    os.system('clear')


def create_board(rows, cols):
    b = []
    for _ in range(rows):
        b.append([" "] * cols)
    return b


def print_board(b):
    # Print column labels A, B, C, ...
    labels = []
    for i in range(len(b[0])):
        labels.append(chr(ord('A') + i))
    print("  " + "   ".join(labels))
    # Print rows
    horizontal = "+" + "+".join(["---"] * len(b[0])) + "+"
    for r in range(len(b)):
        print(horizontal)
        row_cells = []
        for c in range(len(b[0])):
            row_cells.append(b[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(horizontal)


def is_valid_column_letter(letter):
    if len(letter) != 1:
        return False
    if not letter.isalpha():
        return False
    letter = letter.upper()
    col_index = ord(letter) - ord('A')
    if col_index < 0 or col_index >= COLS:
        return False
    return True


def get_column_index(letter):
    return ord(letter.upper()) - ord('A')


def find_row_for_column(b, col):
    # Return the lowest available row index for this column, or -1 if column is full
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            return r
    return -1


def check_winner(b, symbol):
    # Check horizontal, vertical, and diagonals for WIN_LENGTH in a row for the given symbol
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - WIN_LENGTH + 1):
            ok = True
            for k in range(WIN_LENGTH):
                if b[r][c + k] != symbol:
                    ok = False
                    break
            if ok:
                return True

    # Vertical
    for c in range(COLS):
        for r in range(ROWS - WIN_LENGTH + 1):
            ok = True
            for k in range(WIN_LENGTH):
                if b[r + k][c] != symbol:
                    ok = False
                    break
            if ok:
                return True

    # Diagonal down-right
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(COLS - WIN_LENGTH + 1):
            ok = True
            for k in range(WIN_LENGTH):
                if b[r + k][c + k] != symbol:
                    ok = False
                    break
            if ok:
                return True

    # Diagonal up-right
    for r in range(WIN_LENGTH - 1, ROWS):
        for c in range(COLS - WIN_LENGTH + 1):
            ok = True
            for k in range(WIN_LENGTH):
                if b[r - k][c + k] != symbol:
                    ok = False
                    break
            if ok:
                return True

    return False


def is_draw(b):
    # Game is a draw if no empty spaces remain
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] == " ":
                return False
    return True


def main():
    global board
    board = create_board(ROWS, COLS)

    # Determine players' symbols
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly choose a starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_symbol = players[current_player_index]
        # Prompt for input and validate (only invalid inputs are re-asked; full column loses turn)
        while True:
            user_input = input(f"Player {current_symbol}, please enter a column: ").strip()
            if len(user_input) == 0:
                print("Invalid input. Please enter a column letter.")
                continue
            # Accept both lower and uppercase, but require letter to be valid column
            if not is_valid_column_letter(user_input[0]):
                print("Invalid input. Please enter a valid column letter within the board.")
                continue
            col = get_column_index(user_input[0])
            break

        # Try to place the checker
        row = find_row_for_column(board, col)
        if row == -1:
            # Column full -> turn is invalid and lost
            clear_screen()
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {current_symbol} loses the turn.")
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        else:
            # Place the checker
            board[row][col] = current_symbol

        # After placing, print updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_winner(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
