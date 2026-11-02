import os
import random
import string

# ======== CONSTANTS ==========
ROWS = 6                              # Number of rows in the board
COLUMNS = 7                           # Number of columns in the board (max 26)
NUM_PLAYERS = 2                       # Number of players (2-5)
PLAYER_MARKS = ['X', 'O', 'V', 'H', 'M']  # Player symbols, in order
EMPTY_CELL = ' '                      # Character to represent an empty cell

# ========== FUNCTIONS ==========

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Creates and returns a 2D game board initialized with empty cells."""
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Displays the current state of the board"""
    col_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print('  ' + '   '.join(col_labels))
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def get_valid_columns(board):
    """Returns a list of column indices that are not full"""
    valid_cols = []
    for c in range(len(board[0])):
        if board[0][c] == EMPTY_CELL:
            valid_cols.append(c)
    return valid_cols

def input_column(board, player):
    """Prompts the current player for input and validates the response."""
    valid_cols = get_valid_columns(board)
    col_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    valid_labels = [col_labels[c] for c in valid_cols]
    while True:
        inp = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in col_labels:
            print("Invalid input. Please enter a valid column letter (e.g., A-G).")
            continue
        c = col_labels.index(inp)
        if c not in valid_cols:
            print("That column is full. Please choose another or lose your turn.")
            return None   # Lose turn if full
        return c

def place_checker(board, col, mark):
    """Places the player's checker in the lowest available row of given column."""
    for row in reversed(board):
        if row[col] == EMPTY_CELL:
            row[col] = mark
            return board.index(row), col
    # Column is full -- shouldn't reach here due to validation
    return None, None

def check_winner(board, row_idx, col_idx, mark):
    """Checks for 4 in a row - horizontally, vertically, or diagonally, for the last played checker."""
    def count_in_direction(dr, dc):
        count = 0
        r, c = row_idx, col_idx
        while True:
            r += dr
            c += dc
            if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == mark:
                count += 1
            else:
                break
        return count

    # Check all directions: horizontal, vertical, diagonal, anti-diagonal
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        cnt = 1
        cnt += count_in_direction(dr, dc)
        cnt += count_in_direction(-dr, -dc)
        if cnt >= 4:
            return True
    return False

def check_draw(board):
    """Checks if the board is full (i.e., a draw)."""
    return all(cell != EMPTY_CELL for row in board for cell in row)

def get_next_player(curr_idx, total_players):
    """Returns the next player's index."""
    return (curr_idx + 1) % total_players

# ========== MAIN GAME LOOP ==========

def main():
    clear_screen()
    # Set up game
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_MARKS[:NUM_PLAYERS]
    player_names = players

    # Pick starting player at random
    curr_player_idx = random.randint(0, NUM_PLAYERS - 1)
    curr_mark = players[curr_player_idx]

    # Show initial empty board
    print_board(board)

    winner = None
    while True:
        # Player's turn
        print(f"Player {curr_mark}'s turn.")
        col = input_column(board, curr_mark)
        if col is None:
            print("Turn skipped: column full!")
            curr_player_idx = get_next_player(curr_player_idx, NUM_PLAYERS)
            curr_mark = players[curr_player_idx]
            continue
        row, _ = place_checker(board, col, curr_mark)
        clear_screen()
        print_board(board)

        # Check for winner
        if check_winner(board, row, col, curr_mark):
            print(f"Player {curr_mark} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Switch to next player
        curr_player_idx = get_next_player(curr_player_idx, NUM_PLAYERS)
        curr_mark = players[curr_player_idx]

if __name__ == '__main__':
    main()
