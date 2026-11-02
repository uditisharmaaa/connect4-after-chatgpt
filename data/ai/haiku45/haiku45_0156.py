import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the game board to the console.
    
    Args:
        board: The current game board
    """
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * cols + "+")


def get_column_input(cols, board):
    """
    Get and validate column input from the player.
    
    Args:
        cols: Number of columns in the board
        board: The current game board
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input().strip().upper()
        
        # Validate input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter (A-{}).".format(
                chr(65 + cols - 1)))
            continue
        
        # Validate input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter (A-{}).".format(
                chr(65 + cols - 1)))
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Validate column is within board bounds
        if col < 0 or col >= cols:
            print("Invalid input. Please enter a letter (A-{}).".format(
                chr(65 + cols - 1)))
            continue
        
        # Validate column is not full
        if board[0][col] != ' ':
            print("That column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The current game board
        col: The column index where the checker should be placed
        checker: The checker symbol to place
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest available row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    
    return -1


def check_horizontal_win(board, row, col, checker):
    """
    Check if there's a horizontal win starting from the given position.
    
    Args:
        board: The current game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for
    
    Returns:
        True if there's a win, False otherwise
    """
    cols = len(board[0])
    count = 1
    
    # Check left
    for c in range(col - 1, -1, -1):
        if board[row][c] == checker:
            count += 1
        else:
            break
    
    # Check right
    for c in range(col + 1, cols):
        if board[row][c] == checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH


def check_vertical_win(board, row, col, checker):
    """
    Check if there's a vertical win starting from the given position.
    
    Args:
        board: The current game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    count = 1
    
    # Check down
    for r in range(row + 1, rows):
        if board[r][col] == checker:
            count += 1
        else:
            break
    
    # Check up
    for r in range(row - 1, -1, -1):
        if board[r][col] == checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH


def check_diagonal_win_down_right(board, row, col, checker):
    """
    Check if there's a diagonal win (down-right direction) from the given position.
    
    Args:
        board: The current game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    count = 1
    
    # Check up-left diagonal
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        if board[r][c] == checker:
            count += 1
            r -= 1
            c -= 1
        else:
            break
    
    # Check down-right diagonal
    r, c = row + 1, col + 1
    while r < rows and c < cols:
        if board[r][c] == checker:
            count += 1
            r += 1
            c += 1
        else:
            break
    
    return count >= WIN_LENGTH


def check_diagonal_win_down_left(board, row, col, checker):
    """
    Check if there's a diagonal win (down-left direction) from the given position.
    
    Args:
        board: The current game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    count = 1
    
    # Check up-right diagonal
    r, c = row - 1, col + 1
    while r >= 0 and c < cols:
        if board[r][c] == checker:
            count += 1
            r -= 1
            c += 1
        else:
            break
    
    # Check down-left diagonal
    r, c = row + 1, col - 1
    while r < rows and c >= 0:
        if board[r][c] == checker:
            count += 1
            r += 1
            c -= 1
        else:
            break
    
    return count >= WIN_LENGTH


def check_win(board, row, col, checker):
    """
    Check if the last move resulted in a win.
    
    Args:
        board: The current game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for
    
    Returns:
        True if there's a win, False otherwise
    """
    return (check_horizontal_win(board, row, col, checker) or
            check_vertical_win(board, row, col, checker) or
            check_diagonal_win_down_right(board, row, col, checker) or
            check_diagonal_win_down_left(board, row, col, checker))


def check_draw(board):
    """
    Check if the board is full (draw condition).
    
    Args:
        board: The current game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for cell in board[0]:
        if cell == ' ':
            return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get player's checker
        checker = CHECKERS[current_player]
        
        # Get input from player
        print(f"Player {checker}, please enter a column:")
        col = get_column_input(COLS, board)
        
        # Place the checker
        row = place_checker(board, col, checker)
        
        # Print the updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        # Move to next player
        else:
            current_player = (current_player + 1) % NUM_PLAYERS


def main():
    """
    Entry point for the Connect 4 game.
    """
    play_game()


if __name__ == "__main__":
    main()
