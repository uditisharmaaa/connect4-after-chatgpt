import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
ACTIVE_CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]

# Column labels (A, B, C, ...)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]

# --- Board Initialization and Display ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.
    """
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('clear' if os.name == 'posix' else 'cls')

def print_board(board):
    """
    Prints the Connect 4 board with column labels.
    """
    clear_screen()

    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS))

    # Print top border
    print('+' + '---+'.join(['-' * 3 for _ in range(NUM_COLS)]) + '+')

    # Print rows
    for r in range(len(board)):
        row_str = '|'
        for c in range(len(board[0])):
            row_str += f' {board[r][c]} |'
        print(row_str)
        # Print row separator
        print('+' + '---+'.join(['-' * 3 for _ in range(NUM_COLS)]) + '+')

# --- Game Logic ---

def get_player_input(player_checker, current_board):
    """
    Prompts the current player for a column choice and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            prompt = f"Player {player_checker}, please enter a column: "
            col_char = input(prompt).upper()

            if len(col_char) != 1 or col_char not in COLUMN_LABELS:
                print("Invalid input. Please enter a single letter corresponding to a column (e.g., A, B, C).")
                continue

            col_index = COLUMN_LABELS.index(col_char)

            if is_column_full(current_board, col_index):
                print(f"Column {col_char} is full. Please choose another column.")
                # This doesn't lose the turn, it just asks for new input
                continue

            return col_index
        except ValueError:
            print("Invalid input. Please enter a letter.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")

def is_column_full(board, col_index):
    """
    Checks if a given column is completely filled with checkers.
    """
    return board[0][col_index] != ' '

def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns the (row, col) position where the checker was placed.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == ' ':
            board[r][col_index] = player_checker
            return (r, col_index)
    return None # Should not happen if is_column_full is checked beforehand

def check_win(board, last_placed_row, last_placed_col, player_checker):
    """
    Checks if the last placed checker resulted in a win (horizontal, vertical, or diagonal).
    """
    # Check horizontal
    if check_direction(board, last_placed_row, last_placed_col, player_checker, 0, 1): return True
    if check_direction(board, last_placed_row, last_placed_col, player_checker, 0, -1): return True

    # Check vertical
    if check_direction(board, last_placed_row, last_placed_col, player_checker, 1, 0): return True

    # Check diagonal (top-left to bottom-right)
    if check_direction(board, last_placed_row, last_placed_col, player_checker, 1, 1): return True
    if check_direction(board, last_placed_row, last_placed_col, player_checker, -1, -1): return True

    # Check anti-diagonal (top-right to bottom-left)
    if check_direction(board, last_placed_row, last_placed_col, player_checker, 1, -1): return True
    if check_direction(board, last_placed_row, last_placed_col, player_checker, -1, 1): return True

    return False

def check_direction(board, start_row, start_col, player_checker, dr, dc):
    """
    Counts consecutive checkers in a given direction from a starting point.
    Returns True if WIN_CONDITION checkers are found.
    """
    count = 0
    # Check forwards in the direction
    r, c = start_row, start_col
    while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player_checker:
        count += 1
        r += dr
        c += dc

    # Check backwards in the opposite direction (excluding the starting checker again)
    # The starting point was already included in the first loop
    r, c = start_row - dr, start_col - dc
    while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player_checker:
        count += 1
        r -= dr
        c -= dc
    
    return count >= WIN_CONDITION

def check_draw(board):
    """
    Checks if the board is completely filled, resulting in a draw.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found, it's a draw

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = ACTIVE_CHECKERS[current_player_index]

    game_over = False
    
    # Game loop
    while not game_over:
        print_board(board)
        
        col_index = get_player_input(current_checker, board)
        
        last_placed_pos = drop_checker(board, col_index, current_checker)
        
        # Check for a win
        if check_win(board, last_placed_pos[0], last_placed_pos[1], current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for a draw
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_checker = ACTIVE_CHECKERS[current_player_index]

if __name__ == "__main__":
    main()
