import os
import random
import string

# ----------- CONSTANTS ------------- #
NUM_ROWS = 6
NUM_COLS = 7   # Max 26 columns supported
NUM_PLAYERS = 2  # Changeable between 2 and 5 as needed
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_CONDITION = 4
EMPTY_CELL = ' '

# ----------- BOARD CREATION ------------- #
def create_board(rows, cols):
    """Creates a 2D board with all cells initialized to EMPTY_CELL."""
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

# ----------- BOARD PRINTING ------------- #
def print_board(board):
    """Prints the Connect 4 board with appropriate formatting and column labels."""
    os.system('clear')

    columns_label = "  " + "   ".join(string.ascii_uppercase[:len(board[0])])
    print(columns_label)
    print("+" + "---+" * len(board[0]))

    for row in board:
        row_str = "| " + " | ".join(row) + " |"
        print(row_str)
        print("+" + "---+" * len(board[0]))

# ----------- MOVE VALIDATION & UPDATE ------------- #
def is_valid_column(input_str, board):
    """Checks if the user's input is a valid column letter on the current board."""
    if not (len(input_str) == 1 and input_str in string.ascii_uppercase):
        return False
    col_index = ord(input_str) - ord('A')
    if 0 <= col_index < len(board[0]):
        # Check if column is not full
        return board[0][col_index] == EMPTY_CELL
    return False

def is_column_full(col_index, board):
    """Returns True if the top cell in the column is taken."""
    return board[0][col_index] != EMPTY_CELL

def place_checker(board, col_index, checker):
    """Places the checker in the specified column at the lowest available row."""
    for row in reversed(board):
        if row[col_index] == EMPTY_CELL:
            row[col_index] = checker
            return board.index(row), col_index  # return row, col of placed checker
    return None, None  # Can't happen if checked beforehand

# ----------- WIN CHECKING ------------- #
def check_for_win(board, row, col, checker):
    """Checks if placing the checker at (row,col) results in a win."""
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_CONDITION:
            return True
    return False

def is_draw(board):
    """Returns True if the board is full (draw)."""
    return all(cell != EMPTY_CELL for cell in board[0])

# ----------- MAIN GAME LOOP ------------- #
def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    player_symbols = CHECKERS[:NUM_PLAYERS]
    # Random player starts
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print(f"Player {player_symbols[current_player]} starts!")

    while True:
        print_board(board)
        player_char = player_symbols[current_player]
        while True:
            col_input = input(f"Player {player_char}, please enter a column: ").strip().upper()
            if not (len(col_input) == 1 and col_input.isalpha()):
                print("Invalid input. Please enter a letter (A-{}).".format(chr(ord('A')+NUM_COLS-1)))
                continue
            col_index = ord(col_input) - ord('A')
            if 0 <= col_index < NUM_COLS:
                if is_column_full(col_index, board):
                    print("Column full! You lose your turn.")
                    break  # Lose the turn
                else:
                    row_index, _ = place_checker(board, col_index, player_char)
                    break
            else:
                print("Invalid column. Try again.")

        # If the column is not full and checker is placed
        if not is_column_full(col_index, board):
            # Check for win
            if check_for_win(board, row_index, col_index, player_char):
                print_board(board)
                print(f"Player {player_char} won!")
                return
            # Check for draw
            if is_draw(board):
                print_board(board)
                print("Game is a draw!")
                return

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
