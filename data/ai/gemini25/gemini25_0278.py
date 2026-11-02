import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']


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
        list: A 2D list representing the game board, initialized with spaces.
    """
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print('  ' + '   '.join(col_labels))

    # Print the board
    for r_idx, row in enumerate(board):
        print('+---+---' * (len(row) - 1) + '+---+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---+---' * (len(board[0]) - 1) + '+---+')


def get_column_index(column_char, num_cols):
    """
    Converts a column character (e.g., 'A', 'B') to its integer index.

    Args:
        column_char (str): The character representing the chosen column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-based index of the column, or None if invalid.
    """
    if not isinstance(column_char, str) or len(column_char) != 1:
        return None
    
    col_index = ord(column_char.upper()) - ord('A')
    if 0 <= col_index < num_cols:
        return col_index
    return None


def is_valid_move(board, col_index):
    """
    Checks if a move to the given column is valid.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the chosen column.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    if col_index is None:
        return False
    
    # Check if the column is within board boundaries
    if not (0 <= col_index < len(board[0])):
        return False
    
    # Check if the top row of the column is empty
    return board[0][col_index] == ' '


def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        checker (str): The checker symbol for the current player.

    Returns:
        tuple: (row_index, col_index) where the checker was placed, or None if the column was full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col_index] == ' ':
            board[r][col_index] = checker
            return (r, col_index)
    return None  # Column is full (should be caught by is_valid_move, but as a safeguard)


def check_win(board, checker):
    """
    Checks if the current player (with 'checker') has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    seq_len = WIN_SEQUENCE_LENGTH

    # Check horizontal win
    for r in range(num_rows):
        for c in range(num_cols - seq_len + 1):
            if all(board[r][c + i] == checker for i in range(seq_len)):
                return True

    # Check vertical win
    for r in range(num_rows - seq_len + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == checker for i in range(seq_len)):
                return True

    # Check diagonal (top-left to bottom-right) win
    for r in range(num_rows - seq_len + 1):
        for c in range(num_cols - seq_len + 1):
            if all(board[r + i][c + i] == checker for i in range(seq_len)):
                return True

    # Check diagonal (bottom-left to top-right) win
    for r in range(seq_len - 1, num_rows):
        for c in range(num_cols - seq_len + 1):
            if all(board[r - i][c + i] == checker for i in range(seq_len)):
                return True

    return False


def check_draw(board):
    """
    Checks if the game is a draw (board is full).

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_checker = players[current_player_index]
        print_board(board)
        
        print(f"Player {current_checker}, please enter a column:")
        
        while True:
            user_input = input().strip().upper()
            
            if not user_input:
                print("Invalid input. Please enter a column letter (e.g., A, B).")
                continue

            col_index = get_column_index(user_input, NUM_COLS)

            if col_index is None:
                print("Invalid column. Please enter a letter within the board range (A-" + chr(ord('A') + NUM_COLS - 1) + ").")
            elif not is_valid_move(board, col_index):
                print("Column is full. Please choose another column.")
            else:
                break # Valid input and move
        
        # Place the checker
        drop_checker(board, col_index, current_checker)
        
        # Check for win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
