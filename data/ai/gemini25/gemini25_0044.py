import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers. Max 5 players as per assignment (X, O, V, H, M)
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column headers (A, B, C...)
    col_labels = [chr(ord('A') + i) for i in range(num_cols)]
    print("  " + "   ".join(col_labels))

    # Print board rows
    for r in range(len(board)):
        print("+---" * num_cols + "+")
        row_content = []
        for c in range(num_cols):
            row_content.append(f"| {board[r][c]} ")
        print("".join(row_content) + "|")
    print("+---" * num_cols + "+")

def get_column_index(column_char, num_cols):
    """
    Converts a column character (e.g., 'A', 'B') to a 0-based index.

    Args:
        column_char (str): The uppercase character representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-based column index, or None if invalid.
    """
    if not isinstance(column_char, str) or len(column_char) != 1:
        return None
    
    col_index = ord(column_char.upper()) - ord('A')
    if 0 <= col_index < num_cols:
        return col_index
    return None

def is_valid_input(user_input, num_cols):
    """
    Validates the player's column input.

    Args:
        user_input (str): The input string from the player.
        num_cols (int): The total number of columns on the board.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    if len(user_input) != 1:
        return False
    
    col_char = user_input.upper()
    col_index = get_column_index(col_char, num_cols)
    
    return col_index is not None

def drop_checker(board, col_index, player_checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from the bottom row
        if board[r][col_index] == ' ':
            board[r][col_index] = player_checker
            return True
    return False  # Column is full

def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the player to check.
        win_condition (int): The number of checkers in a row needed to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to check a line
    def check_line(r, c, dr, dc):
        count = 0
        for i in range(win_condition):
            nr, nc = r + i * dr, c + i * dc
            if 0 <= nr < num_rows and 0 <= nc < num_cols and board[nr][nc] == player_checker:
                count += 1
            else:
                break
        return count == win_condition

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if check_line(r, c, 0, 1):
                return True

    # Check vertical
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols):
            if check_line(r, c, 1, 0):
                return True

    # Check positive diagonal (bottom-left to top-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if check_line(r, c, 1, 1):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(win_condition - 1, num_cols):
            if check_line(r, c, 1, -1):
                return True
                
    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == ' ':
                return False
    return True

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_checker = CHECKERS[current_player_index]
        print_board(board)
        
        print(f"Player {current_checker}, please enter a column:")
        
        valid_turn = False
        while not valid_turn:
            user_input = input().strip()
            
            if not is_valid_input(user_input, NUM_COLS):
                print("Invalid input. Please enter a single letter (e.g., A, B) within the board range.")
                continue
            
            col_index = get_column_index(user_input, NUM_COLS)
            
            if drop_checker(board, col_index, current_checker):
                valid_turn = True
            else:
                print(f"Column {user_input.upper()} is full. Please choose another column.")
        
        # After a successful drop, check game status
        if check_win(board, current_checker, WIN_CONDITION):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
