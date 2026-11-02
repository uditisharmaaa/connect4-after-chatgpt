import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the board in the required format.
    
    Args:
        board: 2D list representing the board
    """
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)} ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Print top border
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()


def is_valid_column(column_input, cols):
    """
    Check if the column input is valid.
    
    Args:
        column_input: String input from user
        cols: Number of columns in the board
    
    Returns:
        Column index if valid, -1 if invalid
    """
    if len(column_input) != 1:
        return -1
    
    if not column_input.isalpha():
        return -1
    
    column_input = column_input.upper()
    col_index = ord(column_input) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return -1
    
    return col_index


def is_column_full(board, col):
    """
    Check if a column is completely full.
    
    Args:
        board: 2D list representing the board
        col: Column index
    
    Returns:
        True if column is full, False otherwise
    """
    return board[0][col] != " "


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: 2D list representing the board
        col: Column index
        checker: The checker symbol to place
    
    Returns:
        True if successful, False if column is full
    """
    rows = len(board)
    
    # Find the lowest empty space in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_horizontal_win(board, checker):
    """
    Check if there's a horizontal win.
    
    Args:
        board: 2D list representing the board
        checker: The checker symbol to check
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_vertical_win(board, checker):
    """
    Check if there's a vertical win.
    
    Args:
        board: 2D list representing the board
        checker: The checker symbol to check
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_diagonal_win(board, checker):
    """
    Check if there's a diagonal win (both directions).
    
    Args:
        board: 2D list representing the board
        checker: The checker symbol to check
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check diagonals going down-right
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonals going down-left
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, checker):
    """
    Check if the current player has won.
    
    Args:
        board: 2D list representing the board
        checker: The checker symbol to check
    
    Returns:
        True if there's a win, False otherwise
    """
    return (check_horizontal_win(board, checker) or
            check_vertical_win(board, checker) or
            check_diagonal_win(board, checker))


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: 2D list representing the board
    
    Returns:
        True if board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_player_input(player_checker, cols):
    """
    Get and validate column input from the player.
    
    Args:
        player_checker: The checker symbol of current player
        cols: Number of columns in the board
    
    Returns:
        Valid column index
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ")
        col_index = is_valid_column(user_input, cols)
        
        if col_index == -1:
            print("Invalid input. Please enter a valid column letter (A-{}).".format(
                chr(ord('A') + cols - 1)))
            continue
        
        return col_index


def play_game():
    """
    Main game loop for Connect 4.
    """
    board = initialize_board(ROWS, COLS)
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    print(f"Player {players[current_player_index]} starts first!")
    input("Press Enter to continue...")
    
    game_over = False
    
    while not game_over:
        print_board(board)
        current_checker = players[current_player_index]
        
        # Get valid column input from player
        col = get_player_input(current_checker, COLS)
        
        # Check if column is full
        if is_column_full(board, col):
            print(f"Column {chr(ord('A') + col)} is full. Turn lost.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            input("Press Enter to continue...")
            continue
        
        # Place checker
        place_checker(board, col, current_checker)
        
        # Check for win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
