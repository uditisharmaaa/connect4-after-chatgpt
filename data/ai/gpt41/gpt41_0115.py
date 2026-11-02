import os
import random
import string

# ==== CONSTANTS ====
BOARD_ROWS = 6
BOARD_COLS = 7  # up to 26
NUM_PLAYERS = 2  # between 2 and 5

CHECKERS = ['X', 'O', 'V', 'H', 'M']  # up to 5 players
PLAYER_TOKENS = CHECKERS[:NUM_PLAYERS]
COL_LABELS = [chr(ord('A') + i) for i in range(BOARD_COLS)]

# ==== BOARD FUNCTIONS ====


def create_board(rows, cols):
    """Creates and returns the game board as a list of lists."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Clears the screen and prints the current state of the board."""
    os.system('clear')
    # Print column labels
    label_line = "  " + "   ".join(COL_LABELS[:len(board[0])])
    print(label_line)
    # Print separator
    sep = '+' + '---+' * len(board[0])
    for row in board:
        print(sep)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(sep)


def is_valid_column(col_input, board):
    """Validates the column input."""
    if len(col_input) != 1 or col_input not in COL_LABELS[:len(board[0])]:
        return False
    col = COL_LABELS.index(col_input)
    # Column is valid if it's not full
    return board[0][col] == ' '


def place_checker(board, col_input, token):
    """Places a checker in the chosen column. Returns the row index, or None if column full."""
    col = COL_LABELS.index(col_input)
    # Start from the bottom of the column
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = token
            return row, col
    return None  # Column is full


def valid_inputs(board):
    """Returns list of valid column inputs for current board"""
    return [label for label in COL_LABELS[:len(board[0])] if board[0][COL_LABELS.index(label)] == ' ']


def is_board_full(board):
    """Checks if the board is full."""
    return all(cell != ' ' for cell in board[0])


# ==== WIN CHECKING ====

def check_winner(board, token, win_count=4):
    """Checks whether the given token has won the game."""
    rows = len(board)
    cols = len(board[0])

    # Check horizontally
    for row in range(rows):
        count = 0
        for col in range(cols):
            count = count + 1 if board[row][col] == token else 0
            if count >= win_count:
                return True

    # Check vertically
    for col in range(cols):
        count = 0
        for row in range(rows):
            count = count + 1 if board[row][col] == token else 0
            if count >= win_count:
                return True

    # Check diagonals (top left to bottom right)
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == token:
                # Down-right diagonal
                if row + win_count <= rows and col + win_count <= cols:
                    if all(board[row + d][col + d] == token for d in range(win_count)):
                        return True
                # Down-left diagonal
                if row + win_count <= rows and col - win_count + 1 >= 0:
                    if all(board[row + d][col - d] == token for d in range(win_count)):
                        return True
    return False

# ==== MAIN GAME LOOP ====


def main():
    # Initialize the board
    board = create_board(BOARD_ROWS, BOARD_COLS)

    # Randomly choose first player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {PLAYER_TOKENS[current_player]} will start!")

    while True:
        token = PLAYER_TOKENS[current_player]
        valid_cols = valid_inputs(board)
        if not valid_cols:
            # No valid columns left = draw
            print("It's a draw! No more moves possible.")
            break

        while True:
            print_board(board)
            inp = input(f"Player {token}, please enter a column: ").strip().upper()
            if not is_valid_column(inp, board):
                if len(inp) != 1 or inp not in COL_LABELS[:len(board[0])]:
                    print(f"Invalid input. Please enter a valid column: {', '.join(valid_cols)}")
                elif board[0][COL_LABELS.index(inp)] != ' ':
                    print(f"Column is full! You lose your turn.")
                    break  # Lose turn
            else:
                move = place_checker(board, inp, token)
                if move is not None:
                    # Correct placement
                    if check_winner(board, token):
                        print_board(board)
                        print(f"Player {token} won!")
                        return
                    elif is_board_full(board):
                        print_board(board)
                        print("It's a draw! No player has won.")
                        return
                    # Next player's turn
                    current_player = (current_player + 1) % NUM_PLAYERS
                break  # Move made or turn lost

        # If turn was invalid due to full column, skip to next player
        if len(inp) == 1 and inp in COL_LABELS[:len(board[0])] and board[0][COL_LABELS.index(inp)] != ' ':
            current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == '__main__':
    main()
