import os
import random

# Constants for board size and players
ROWS = 6       # Number of rows (6)
COLS = 7       # Number of columns (7), max 26 supported
NUM_PLAYERS = 2  # Number of players (2)
WIN_COUNT = 4    # Number of checkers in a row needed to win

# Allowed checkers for up to 5 players (order matters)
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Create the board initialized with whitespace characters."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Print the Connect 4 board.
    Columns are labeled A..G (or more), rows aren't labeled.
    """
    cols = len(board[0])
    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(cols))
    print(header)
    # Print board rows with the format shown
    for row in range(len(board)):
        print('+' + '---+' * cols)
        # Print cell content separated by vertical bars
        row_str = '| ' + ' | '.join(board[row][col] for col in range(cols)) + ' |'
        print(row_str)
    print('+' + '---+' * cols)

def get_player_input(player_checker, cols, board):
    """
    Request player input for a column letter.
    Validate input until a valid column letter and not full column.
    If the column is full, player loses the turn.
    Returns:
        col_index (int) or None if column full (lose turn)
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Check input length and validity
        if len(user_input) != 1 or not ('A' <= user_input <= chr(ord('A') + cols - 1)):
            print(f"Invalid input. Enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        col = ord(user_input) - ord('A')
        # Check if column is full
        if board[0][col] != ' ':
            # Column full, player loses turn
            print(f"Column {user_input} is full. Turn lost.")
            return None
        return col

def place_checker(board, col, checker):
    """
    Place the checker in given column, at the lowest available row.
    Returns the row index where checker was placed.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return None  # Should not reach here if column not full

def check_win(board, row, col, checker):
    """
    Check if placing checker at board[row][col] produces a win.
    Win = 4 in a row horizontally, vertically, or diagonally
    """
    def count_direction(r_step, c_step):
        # Count continuous checkers of the same kind in one direction
        r, c = row + r_step, col + c_step
        count = 0
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += r_step
            c += c_step
        return count

    # Directions to check: horizontal, vertical, two diagonals
    directions = [
        ((0, 1), (0, -1)),    # Horizontal (right and left)
        ((1, 0), (-1, 0)),    # Vertical (down and up)
        ((1, 1), (-1, -1)),   # Diagonal down-right and up-left
        ((1, -1), (-1, 1))    # Diagonal down-left and up-right
    ]

    for dir1, dir2 in directions:
        count = 1  # Count current checker
        count += count_direction(*dir1)
        count += count_direction(*dir2)
        if count >= WIN_COUNT:
            return True
    return False

def check_draw(board):
    """
    Check if board is full (draw)
    """
    # If any cell in top row is empty, game continues
    return all(cell != ' ' for cell in board[0])

def main():
    # Setup board and players
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_index]

        col = get_player_input(current_checker, COLS, board)

        if col is not None:
            # Place checker on board
            row = place_checker(board, col, current_checker)

            # Check if this move wins the game
            if check_win(board, row, col, current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                break

            # Check draw
            if check_draw(board):
                clear_screen()
                print_board(board)
                print("The game is a draw!")
                break
        # If col is None, player lost turn (column full), no placement done

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == '__main__':
    main()
