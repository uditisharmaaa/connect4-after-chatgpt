import os
import random
import string

# ----------------------------
# Constants (change as needed)
ROWS = 6    # number of rows
COLUMNS = 7 # number of columns (max 26)
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
WIN_COUNT = 4
# ----------------------------

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column labels
    col_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def get_valid_input(prompt, valid_cols):
    while True:
        choice = input(prompt).strip().upper()
        if len(choice) != 1 or choice not in valid_cols:
            print(f"Invalid input. Please enter one of {', '.join(valid_cols)}.")
            continue
        return choice

def drop_checker(board, col_index, checker):
    # Place checker in lowest available row in the column
    for row_index in reversed(range(len(board))):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return row_index  # Return the row where checker fell
    return None  # Column is full

def check_win(board, row, col, checker):
    # Check in all directions for a win (horiz, vert, diag1, diag2)
    directions = [ (0,1), (1,0), (1,1), (1,-1) ]
    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    valid_cols = [string.ascii_uppercase[i] for i in range(COLUMNS)]
    # Choose random first player
    current_player = random.randint(0, NUM_PLAYERS-1)
    clear_screen()
    print_board(board)
    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")
        col_choice = get_valid_input("> ", valid_cols)
        col_index = valid_cols.index(col_choice)
        # Check for full column
        if board[0][col_index] != " ":
            print(f"Column {col_choice} is full. You lose your turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        # Drop checker
        row_index = drop_checker(board, col_index, checker)
        clear_screen()
        print_board(board)
        # Check for win condition
        if check_win(board, row_index, col_index, checker):
            print(f"Player {checker} won!")
            break
        # Check draw
        if board_full(board):
            print("It's a draw!")
            break
        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
