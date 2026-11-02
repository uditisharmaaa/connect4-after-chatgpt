import os
import random
import string

# ----- Constants -----
ROWS = 6          # Number of rows in the board
COLUMNS = 7       # Number of columns in the board (max 26)
NUM_PLAYERS = 2   # Number of players (between 2 and 5)
WIN_CONDITION = 4 # Number of checkers in a row needed to win

CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Player tokens in order

# ----- Functions -----

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Initializes the game board as a list of lists filled with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Displays the current game board with column labels."""
    cols = len(board[0])
    header_labels = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header_labels)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_player_input(player_num, player_checker, board):
    """Prompts the current player for a column choice and validates the input."""
    cols = len(board[0])
    valid_labels = list(string.ascii_uppercase[:cols])
    while True:
        move = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(move) != 1 or move not in valid_labels:
            print("Invalid input! Please enter a valid column letter.")
            continue
        col = valid_labels.index(move)
        if board[0][col] != ' ':
            print("Column is full! Turn is lost.")
            return None  # Turn is forfeited if column full
        return col

def place_checker(board, col, checker):
    """Places the checker in the lowest available row in the chosen column."""
    for row_idx in reversed(range(len(board))):
        if board[row_idx][col] == ' ':
            board[row_idx][col] = checker
            return row_idx, col
    # Should not reach here since we check for column full in input
    return None, None

def check_win(board, row, col, checker):
    """Checks if the given checker has a winning line starting from (row, col)."""
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_CONDITION:
            return True
    return False

def is_draw(board):
    """Checks if the board is full, resulting in a draw."""
    return all(cell != ' ' for cell in board[0])

def main():
    # Initialize
    board = create_board(ROWS, COLUMNS)
    player_checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)
    print(f"Randomly selected Player {player_checkers[current_player]} to start.")

    while True:
        player_checker = player_checkers[current_player]
        col = get_player_input(current_player, player_checker, board)

        clear_screen()
        if col is not None:
            row, col_placed = place_checker(board, col, player_checker)
            print_board(board)

            # Check for win
            if check_win(board, row, col_placed, player_checker):
                print(f"Player {player_checker} won!")
                break

            # Check for draw
            if is_draw(board):
                print("It's a draw!")
                break

        else:
            print_board(board)

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
