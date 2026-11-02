import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labeling
NUM_PLAYERS = 2  # Between 2 and 5
WIN_CONDITION = 4  # Number of checkers in a row to win

CHECKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]


# --- Board Functions ---
def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    Each cell is initialized with a whitespace.
    """
    board = []
    for _ in range(rows):
        board.append([' '] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    Includes column labels and a grid structure.
    """
    os.system('clear')  # Clear screen for fresh board print

    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS[:len(board[0])]))

    # Print board rows
    for r_idx, row in enumerate(board):
        print('+' + '---+' * len(row))
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+' + '---+' * len(board[0]))


# --- Game Logic Functions ---
def get_column_input(player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-based index of the chosen column.
    """
    while True:
        try:
            user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()

            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B).")
                continue

            col_label_index = COLUMN_LABELS.index(user_input)
            if col_label_index >= NUM_COLS:
                print(f"Invalid column. Please choose a column from A to {COLUMN_LABELS[NUM_COLS - 1]}.")
                continue

            return col_label_index
        except ValueError:
            print(f"Invalid column. Please choose a column from A to {COLUMN_LABELS[NUM_COLS - 1]}.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")


def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if the checker was successfully placed, False if the column is full.
    """
    for r_idx in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r_idx][col_index] == ' ':
            board[r_idx][col_index] = player_checker
            return True, r_idx, col_index  # Return success and placement coordinates
    return False, -1, -1  # Column is full


def check_win(board, r, c, player_checker, win_len):
    """
    Checks if the last placed checker at (r, c) results in a win.
    Checks horizontal, vertical, and both diagonal directions.
    """
    # Helper function to count consecutive checkers in a direction
    def count_consecutive(delta_r, delta_c):
        count = 0
        # Check forward direction
        curr_r, curr_c = r, c
        while 0 <= curr_r < NUM_ROWS and 0 <= curr_c < NUM_COLS and board[curr_r][curr_c] == player_checker:
            count += 1
            curr_r += delta_r
            curr_c += delta_c
        
        # Check backward direction (excluding the starting checker again)
        curr_r, curr_c = r - delta_r, c - delta_c
        while 0 <= curr_r < NUM_ROWS and 0 <= curr_c < NUM_COLS and board[curr_r][curr_c] == player_checker:
            count += 1
            curr_r -= delta_r
            curr_c -= delta_c
        
        return count

    # Check horizontal
    if count_consecutive(0, 1) >= win_len:
        return True
    # Check vertical
    if count_consecutive(1, 0) >= win_len: # Only need to check downwards from placement
        return True
    # Check diagonal (top-left to bottom-right)
    if count_consecutive(1, 1) >= win_len:
        return True
    # Check anti-diagonal (top-right to bottom-left)
    if count_consecutive(1, -1) >= win_len:
        return True

    return False


def check_draw(board):
    """
    Checks if the board is completely filled (draw).
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found, it's a draw


# --- Main Game Function ---
def play_game():
    """
    Main function to run the Connect 4 game.
    """
    current_board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly choose first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winning_player = None

    print_board(current_board)
    print(f"Player {players[current_player_idx]} goes first!")

    while not game_over:
        player_checker = players[current_player_idx]
        
        col_index = get_column_input(player_checker)

        placed, row_placed, col_placed = drop_checker(current_board, col_index, player_checker)

        if not placed:
            print(f"Column {COLUMN_LABELS[col_index]} is full. Please choose another column.")
            # Player does not lose turn for a full column
            continue
        
        print_board(current_board)

        # Check for win
        if check_win(current_board, row_placed, col_placed, player_checker, WIN_CONDITION):
            winning_player = player_checker
            game_over = True
            break
        
        # Check for draw
        if check_draw(current_board):
            game_over = True
            break

        # Switch to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    # Game End
    print_board(current_board) # Final board state

    if winning_player:
        print(f"Player {winning_player} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_game()
