import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
# Ensure enough checkers for the number of players
if NUM_PLAYERS > len(PLAYER_CHECKERS):
    raise ValueError(f"Not enough unique checkers defined for {NUM_PLAYERS} players.")

# --- Board Initialization and Display ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board with column labels.
    Clears the screen before printing.
    """
    os.system('clear')  # Clear the terminal screen

    # Print column labels (A, B, C, ...)
    col_labels = string.ascii_uppercase[:len(board[0])]
    print("  " + "   ".join(col_labels))

    # Print top border
    print("+" + "---+-" * len(board[0]) + "++" if len(board[0]) == 1 else "+" + "---+-" * len(board[0]))

    # Print rows with checkers
    for r in range(len(board)):
        row_str = "|"
        for c in range(len(board[r])):
            row_str += f" {board[r][c]} |"
        print(row_str)
        # Print row separator (only if not the last row)
        if r < len(board) - 1:
            print("+" + "---+-" * len(board[0]) + "++" if len(board[0]) == 1 else "+" + "---+-" * len(board[0]))
    
    # Print bottom border
    print("+" + "---+-" * len(board[0]) + "++" if len(board[0]) == 1 else "+" + "---+-" * len(board[0]))


# --- Game Logic ---

def get_player_input(player_checker, board_cols):
    """
    Prompts the current player for a column input and validates it.
    Keeps asking until a valid input is received.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or col_char not in string.ascii_uppercase[:board_cols]:
                print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
                continue

            col_index = ord(col_char) - ord('A')
            return col_index
        except ValueError:
            print("Invalid input. Please enter a single uppercase letter.")

def place_checker(board, col_index, player_checker):
    """
    Places the player's checker in the lowest available space in the specified column.
    Returns True if successful, False if the column is full.
    """
    if not (0 <= col_index < len(board[0])):
        return False, -1, -1 # Invalid column index

    # Check from the bottom up
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True, r, col_index  # Return success and position
    return False, -1, -1  # Column is full

def check_win(board, r, c, player_checker, win_condition):
    """
    Checks if the last placed checker at (r, c) results in a win.
    Checks horizontally, vertically, and diagonally.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # 1. Check Horizontal
    count = 0
    for col in range(num_cols):
        if board[r][col] == player_checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # 2. Check Vertical
    count = 0
    for row in range(num_rows):
        if board[row][c] == player_checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # 3. Check Diagonals (top-left to bottom-right)
    # Start from the current position and go up-left as far as possible
    start_r_tlbr = r - min(r, c)
    start_c_tlbr = c - min(r, c)
    count = 0
    while start_r_tlbr < num_rows and start_c_tlbr < num_cols:
        if board[start_r_tlbr][start_c_tlbr] == player_checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0
        start_r_tlbr += 1
        start_c_tlbr += 1

    # 4. Check Diagonals (top-right to bottom-left)
    # Start from the current position and go up-right as far as possible
    start_r_trbl = r - min(r, num_cols - 1 - c)
    start_c_trbl = c + min(r, num_cols - 1 - c)
    count = 0
    while start_r_trbl < num_rows and start_c_trbl >= 0:
        if board[start_r_trbl][start_c_trbl] == player_checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0
        start_r_trbl += 1
        start_c_trbl -= 1

    return False

def check_draw(board):
    """
    Checks if the board is completely full (no more empty spaces).
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces, it's a draw

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    print_board(board)

    while not game_over:
        current_player_checker = players[current_player_index]
        
        col_index = get_player_input(current_player_checker, NUM_COLS)
        
        placed, row_placed, col_placed = place_checker(board, col_index, current_player_checker)

        if not placed:
            print("Column is full. Please choose another column.")
            # Player does not lose turn if column is full or invalid input,
            # but for this assignment, the prompt says "the turn is invalid and the player loses the turn."
            # So, we don't change the player index if placement failed.
            # If the intended behavior is to retry without losing turn, remove the continue below.
            continue
        
        print_board(board)

        if check_win(board, row_placed, col_placed, current_player_checker, WIN_CONDITION):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        
        # Switch to the next player
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
