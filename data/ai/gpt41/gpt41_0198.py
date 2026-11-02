import random
import os
import sys

# -------------------------
# CONSTANTS
# -------------------------

NUM_ROWS = 6
NUM_COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # You may set this to 2–5 for testing, but must be 2 in submission

COLUMNS = [chr(i) for i in range(ord('A'), ord('A') + NUM_COLS)]


# -------------------------
# BOARD FUNCTIONS
# -------------------------

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    os.system('clear')  # use 'cls' on Windows if needed
    # Print column headers
    print("  " + "   ".join(COLUMNS))
    print("+" + "---+" * NUM_COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * NUM_COLS)

def is_column_full(board, col_index):
    return board[0][col_index] != " "

def drop_checker(board, col_index, checker):
    for row in range(NUM_ROWS-1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    return None  # Column is full

def is_valid_column_input(col_input):
    return (len(col_input) == 1 and 
            col_input.isalpha() and 
            col_input.upper() in COLUMNS)

def is_board_full(board):
    for col in range(NUM_COLS):
        if not is_column_full(board, col):
            return False
    return True

# -------------------------
# WIN CHECK FUNCTIONS
# -------------------------

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    for _ in range(4):
        if 0 <= row < NUM_ROWS and 0 <= col < NUM_COLS:
            if board[row][col] == checker:
                count += 1
            else:
                break
        else:
            break
        row += delta_row
        col += delta_col
    return count == 4

def check_for_win(board, checker):
    # Check all cells to see if there's 4 in a row starting there
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == checker:
                # Check right
                if check_direction(board, row, col, 0, 1, checker):
                    return True
                # Check down
                if check_direction(board, row, col, 1, 0, checker):
                    return True
                # Check diagonal down-right
                if check_direction(board, row, col, 1, 1, checker):
                    return True
                # Check diagonal down-left
                if check_direction(board, row, col, 1, -1, checker):
                    return True
    return False

# -------------------------
# MAIN GAME FUNCTION
# -------------------------

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    checkers = PLAYERS[:NUM_PLAYERS]

    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print("Player {} starts!".format(checkers[current_player]))

    while True:
        player_checker = checkers[current_player]
        print("Player {}, please enter a column:".format(player_checker))
        
        while True:
            col_input = input().strip().upper()
            if not is_valid_column_input(col_input):
                print("Invalid input. Please enter a column letter (A-{}):".format(COLUMNS[-1]))
                continue
            col_index = COLUMNS.index(col_input)
            if is_column_full(board, col_index):
                print("Column is full! You lose your turn.")
                col_index = None
                break
            break

        if col_index is not None:
            position = drop_checker(board, col_index, player_checker)
            print_board(board)
            if check_for_win(board, player_checker):
                print("Player {} won!".format(player_checker))
                break
            if is_board_full(board):
                print("The game is a draw!")
                break
        else:
            print_board(board)

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
