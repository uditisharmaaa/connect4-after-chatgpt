import os
import random
import string

# ====== Constants (Change these for other settings if needed) =======
NUM_ROWS = 6           # Number of rows
NUM_COLS = 7           # Number of columns (Max: 26)
NUM_PLAYERS = 2        # Number of players (2-5)
CONNECT_N = 4          # Number of checkers in a row needed to win

PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']  # Available checkers for up to 5 players
COLUMN_LABELS = list(string.ascii_uppercase[:NUM_COLS])

# ========== Board Functions ==========

def create_board(rows, cols):
    """Creates and returns a new board."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def print_board(board):
    """Prints the board with column labels."""
    clear_screen()
    # Print column headers
    print('  ' + '   '.join(COLUMN_LABELS))
    # Print top border
    print('+' + '---+' * NUM_COLS)
    # Print rows
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * NUM_COLS)

# ========== Gameplay Functions ==========

def get_valid_column_input(board, current_player):
    """Prompts the current player until a valid column is entered."""
    while True:
        user_input = input(f"Player {PLAYER_MARKERS[current_player]}, please enter a column: ").strip().upper()

        if len(user_input) != 1 or user_input not in COLUMN_LABELS:
            print("Invalid input! Please enter a single column letter (A-G).")
            continue

        col_index = COLUMN_LABELS.index(user_input)
        # Check if the column is full
        if board[0][col_index] != ' ':
            print("Column is full! You lose your turn.")
            return None
        return col_index

def place_checker(board, col, marker):
    """Places a checker in the given column for the player."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = marker
            return board.index(row), col  # Return the position where checker landed
    # Should not reach here (column fullness checked before calling)
    return None, None

def board_full(board):
    """Checks if the board is full."""
    for col in range(NUM_COLS):
        if board[0][col] == ' ':
            return False
    return True

def check_for_win(board, row, col, marker):
    """Checks horizontally, vertically, and diagonally for a win starting from (row, col)."""
    # Directions: (dr, dc)
    directions = [
        (0, 1),    # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1),   # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == marker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == marker:
            count += 1
            r -= dr
            c -= dc
        if count >= CONNECT_N:
            return True
    return False

# ========== Main Game ==========

def main():
    # Setup
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_MARKERS[:NUM_PLAYERS]

    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {players[current_player]} goes first!")

    move_count = 0
    while True:
        col = get_valid_column_input(board, current_player)
        if col is None:  # Player lost their turn due to full column
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Place checker and print board
        row_placed, col_placed = place_checker(board, col, players[current_player])
        print_board(board)

        move_count += 1

        # Check for win
        if check_for_win(board, row_placed, col_placed, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
