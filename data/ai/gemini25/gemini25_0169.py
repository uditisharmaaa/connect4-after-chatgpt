import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board filled with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def get_column_letter(col_index):
    """
    Converts a column index (0-based) to an uppercase letter (A-Z).
    """
    if col_index < 0 or col_index >= 26:
        return "" # Should not happen with valid NUM_COLS
    return chr(ord('A') + col_index)

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    """
    os.system('clear') # Clear the screen before printing

    # Print column headers (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f" {get_column_letter(col_index)} ", end="")
    print()

    # Print board content
    for row in board:
        print("+", end="")
        for _ in row:
            print("---+", end="")
        print()
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in board[0]:
        print("---+", end="")
    print()

def get_column_from_input(user_input, num_cols):
    """
    Converts a user's column letter input to a 0-based column index.
    Returns -1 if the input is invalid.
    """
    if len(user_input) != 1 or not user_input.isalpha():
        return -1
    
    col_char = user_input.upper()
    col_index = ord(col_char) - ord('A')
    
    if 0 <= col_index < num_cols:
        return col_index
    else:
        return -1

def is_valid_move(board, col_index):
    """
    Checks if a column is a valid place to drop a checker (not full).
    """
    return board[0][col_index] == " " # Check the top-most row

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.
    Returns the row where the checker landed, or -1 if the column was full.
    """
    for row_index in range(len(board) - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return row_index
    return -1 # Column is full

# --- Win Condition Checks ---

def check_horizontal_win(board, row, col, checker, win_count):
    """
    Checks for a horizontal win.
    """
    count = 0
    # Check to the right
    for c in range(col, len(board[0])):
        if board[row][c] == checker:
            count += 1
        else:
            break
    # Check to the left (starting from col - 1 to avoid double counting the original checker)
    for c in range(col - 1, -1, -1):
        if board[row][c] == checker:
            count += 1
        else:
            break
    return count >= win_count

def check_vertical_win(board, row, col, checker, win_count):
    """
    Checks for a vertical win.
    """
    count = 0
    # Check downwards
    for r in range(row, len(board)):
        if board[r][col] == checker:
            count += 1
        else:
            break
    return count >= win_count

def check_diagonal_win(board, row, col, checker, win_count):
    """
    Checks for diagonal wins (both directions).
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check positive slope diagonal (bottom-left to top-right)
    count1 = 0
    # Start from current position and move up-right
    for i in range(win_count):
        r, c = row - i, col + i
        if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
            count1 += 1
        else:
            break
    # Move down-left from current position
    for i in range(1, win_count): # Start from 1 to avoid double counting
        r, c = row + i, col - i
        if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
            count1 += 1
        else:
            break
    if count1 >= win_count:
        return True

    # Check negative slope diagonal (top-left to bottom-right)
    count2 = 0
    # Start from current position and move up-left
    for i in range(win_count):
        r, c = row - i, col - i
        if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
            count2 += 1
        else:
            break
    # Move down-right from current position
    for i in range(1, win_count): # Start from 1 to avoid double counting
        r, c = row + i, col + i
        if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
            count2 += 1
        else:
            break
    return count2 >= win_count

def check_win(board, last_row, last_col, checker, win_condition):
    """
    Checks if the last placed checker resulted in a win.
    """
    # Check all possible win directions
    return (check_horizontal_win(board, last_row, last_col, checker, win_condition) or
            check_vertical_win(board, last_row, last_col, checker, win_condition) or
            check_diagonal_win(board, last_row, last_col, checker, win_condition))

def check_draw(board):
    """
    Checks if the board is completely full (a draw).
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False # Found an empty space, not a draw yet
    return True # No empty spaces found, it's a draw

# --- Main Game Logic ---

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Select checkers for the game
    game_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = game_checkers[current_player_index]

    game_over = False
    winning_player_checker = None

    while not game_over:
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        # Get and validate player input
        valid_input = False
        col_index = -1
        while not valid_input:
            user_input = input().strip()
            col_index = get_column_from_input(user_input, NUM_COLS)

            if col_index == -1:
                print("Invalid column. Please enter a letter from A to", get_column_letter(NUM_COLS - 1))
            elif not is_valid_move(board, col_index):
                print("Column is full. Please choose another column.")
            else:
                valid_input = True
        
        # Drop the checker
        last_row = drop_checker(board, col_index, current_checker)
        last_col = col_index # Store the column for win check

        # Check for win
        if check_win(board, last_row, last_col, current_checker, WIN_CONDITION):
            print_board(board)
            winning_player_checker = current_checker
            game_over = True
        elif check_draw(board):
            print_board(board)
            game_over = True
            print("It's a draw!")
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_checker = game_checkers[current_player_index]

    if winning_player_checker:
        print(f"Player {winning_player_checker} won!")

if __name__ == "__main__":
    main()
