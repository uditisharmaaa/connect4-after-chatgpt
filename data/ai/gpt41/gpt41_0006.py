import os
import random
import string

# Constants
ROWS = 6                # Number of rows (can change up to max 26 columns)
COLUMNS = 7             # Number of columns (can change up to max 26 columns)
NUM_PLAYERS = 2         # Number of players (can be from 2 to 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Player pieces
WIN_CONDITION = 4       # Number of checkers in a row needed to win

def clear_screen():
    # Clear the console screen
    os.system('clear')

def create_board(rows, columns):
    # Create board: list of lists filled with " "
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    # Print the board as described
    cols = len(board[0])
    # Print column headers
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(letters))
    print("+" + "---+"*cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+"*cols)

def get_valid_columns(board):
    # Returns list of indices of columns that aren't full
    columns = []
    for col in range(len(board[0])):
        if board[0][col] == " ":
            columns.append(col)
    return columns

def col_letter_to_index(letter):
    # Convert letter (e.g. 'A') to column index
    letter = letter.upper()
    if letter in string.ascii_uppercase:
        return string.ascii_uppercase.index(letter)
    else:
        return -1

def is_board_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def drop_checker(board, col, checker):
    # Place checker in the lowest available spot in specified column
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True
    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True
    # Check diagonals (top-left to bottom-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True
    # Check diagonals (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True
    return False

def get_player_input(player_checker, board):
    valid_columns = get_valid_columns(board)
    cols = len(board[0])
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    while True:
        choice = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(choice) != 1 or choice not in letters:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col_index = col_letter_to_index(choice)
        if col_index < 0 or col_index >= cols:
            print("Invalid input. Please enter a valid column letter within the board.")
            continue
        if board[0][col_index] != " ":
            print(f"Column {choice} is full. You lose your turn!")
            return None  # Indicate losing turn
        return col_index

def main():
    # Setup
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]  # Only as many checkers as players
    current_player = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    winner_found = False
    while True:
        player_checker = players[current_player]
        col_index = get_player_input(player_checker, board)
        clear_screen()
        if col_index is not None:
            if drop_checker(board, col_index, player_checker):
                print_board(board)
                if check_win(board, player_checker):
                    print(f"Player {player_checker} won!")
                    break
                if is_board_full(board):
                    print("It's a draw!")
                    break
            else:
                print_board(board)
                print(f"Column {string.ascii_uppercase[col_index]} is full. You lose your turn!")
        else:
            print_board(board)
        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
