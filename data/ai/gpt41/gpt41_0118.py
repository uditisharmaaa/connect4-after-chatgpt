import os
import random
import string

# ----- Constants -----
ROWS = 6              # Number of rows
COLUMNS = 7           # Number of columns (max 26)
NUM_PLAYERS = 2       # Number of players (2 to 5)
MAX_PLAYERS = 5
WIN_LENGTH = 4

CHECKERS = ["X", "O", "V", "H", "M"]  # Max 5, in order

# ----- Functions -----

def clear_screen():
    os.system('clear')  # On linux/unix

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column headers
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    # Print separator
    print("+" + "---+" * cols)
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_columns(board):
    return [c for c in range(len(board[0])) if board[0][c] == " "]

def column_letter_to_index(letter, cols):
    letter = letter.upper()
    if letter in string.ascii_uppercase[:cols]:
        return string.ascii_uppercase.index(letter)
    return -1

def drop_checker(board, col, checker):
    # Place checker in lowest available position in the column
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col  # return the position
    return None, None  # Should not get here if caller checks first

def check_direction(board, row, col, dr, dc, checker):
    count = 0
    r, c = row, col
    while (0 <= r < len(board)) and (0 <= c < len(board[0])) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, row, col, checker):
    # Check all directions from the last placed checker
    directions = [ (0,1), (1,0), (1,1), (1,-1) ]  # H, V, Diag \, Diag /
    for dr, dc in directions:
        count = 1  # Include the current checker

        # Check forward
        count += check_in_direction(board, row, col, dr, dc, checker)
        # Check backward
        count += check_in_direction(board, row, col, -dr, -dc, checker)

        if count >= WIN_LENGTH:
            return True
    return False

def check_in_direction(board, row, col, dr, dc, checker):
    count = 0
    r, c = row + dr, col + dc
    while (0 <= r < len(board)) and (0 <= c < len(board[0])) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def board_full(board):
    return all(cell != " " for cell in board[0])

def input_column(prompt, board):
    cols = len(board[0])
    valid_letters = string.ascii_uppercase[:cols]
    valid_cols = get_valid_columns(board)
    while True:
        col_input = input(prompt).strip().upper()
        if len(col_input) != 1 or col_input not in valid_letters:
            print("Invalid column. Please enter one of the column letters (A-{}).".format(valid_letters[-1]))
            continue
        col = column_letter_to_index(col_input, cols)
        if col not in valid_cols:
            print("Column {} is full or invalid. Please try another column.".format(col_input))
            continue
        return col

# ----- Main Program -----

def main():
    # Setup players
    if NUM_PLAYERS < 2 or NUM_PLAYERS > MAX_PLAYERS:
        print(f"Number of players must be between 2 and {MAX_PLAYERS}.")
        return
    players = CHECKERS[:NUM_PLAYERS]

    # Initialize board
    board = create_board(ROWS, COLUMNS)

    # Randomly select starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Initial board display
    clear_screen()
    print_board(board)

    while True:
        player_checker = players[current_player]
        print(f"Player {player_checker}, please enter a column:")
        col = input_column(">", board)

        # Place checker
        row, col_index = drop_checker(board, col, player_checker)
        clear_screen()
        print_board(board)

        # Check win
        if check_win(board, row, col_index, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
