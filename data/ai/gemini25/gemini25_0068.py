import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board,
              initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))

    # Print board content
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_content = []
        for c in range(len(board[0])):
            row_content.append(f"| {board[r][c]} ")
        print("".join(row_content) + "|")
    print("+---" * len(board[0]) + "+")

def is_valid_column_input(col_str, num_cols):
    """
    Checks if the given column input string is valid.

    Args:
        col_str (str): The column input string from the player.
        num_cols (int): The total number of columns on the board.

    Returns:
        tuple: (bool, int) - True if valid, False otherwise.
               If valid, the integer index of the column.
    """
    if not isinstance(col_str, str) or len(col_str) != 1:
        return False, -1
    
    col_char = col_str.upper()
    
    if not 'A' <= col_char <= chr(ord('A') + num_cols - 1):
        return False, -1
    
    col_index = ord(col_char) - ord('A')
    return True, col_index

def get_player_move(player_checker, board):
    """
    Prompts the current player for a column choice and validates it.

    Args:
        player_checker (str): The checker symbol for the current player.
        board (list): The current game board.

    Returns:
        int: The valid column index chosen by the player.
    """
    num_cols = len(board[0])
    num_rows = len(board)
    
    while True:
        try:
            col_input = input(f"Player {player_checker}, please enter a column: ").strip()
            is_valid, col_index = is_valid_column_input(col_input, num_cols)

            if not is_valid:
                print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + num_cols - 1)}.")
                continue

            # Check if the column is full
            if board[0][col_index] != " ":
                print("That column is full. Please choose another column.")
                continue
            
            return col_index
        except EOFError:
            print("\nGame interrupted. Exiting.")
            sys.exit()

def drop_checker(board, col_index, player_checker):
    """
    Places the player's checker into the lowest available spot in a column.

    Args:
        board (list): The current game board.
        col_index (int): The column index where the checker is to be dropped.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column was full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True
    return False # Column is full (should have been caught by get_player_move)

def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The current game board.
        player_checker (str): The checker symbol for the current player.
        win_condition (int): The number of checkers in a row needed to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal wins
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical wins
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal (top-left to bottom-right) wins
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal (bottom-left to top-right) wins
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The current game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
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
        player_checker = PLAYER_CHECKERS[current_player_index]
        
        print_board(board)
        
        col_index = get_player_move(player_checker, board)
        
        drop_successful = drop_checker(board, col_index, player_checker)
        
        # This condition should ideally not be False if get_player_move is robust,
        # but included for defensive programming.
        if not drop_successful:
            print("Error: Could not drop checker. This should not happen.")
            continue 

        # Check for win
        if check_win(board, player_checker, WIN_CONDITION):
            print_board(board)
            print(f"Player {player_checker} won!")
            game_over = True
        
        # Check for draw if no win
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        
        # Switch to the next player
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
