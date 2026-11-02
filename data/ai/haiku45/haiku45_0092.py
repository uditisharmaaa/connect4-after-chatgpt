import random
import os

# Global constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the game board to the console.
    
    Args:
        board: The game board to print
    """
    os.system('clear')
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)} ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * cols + "+")


def is_valid_column(column_input, cols):
    """
    Validate if the column input is valid.
    
    Args:
        column_input: The user's column input
        cols: Number of columns in the board
    
    Returns:
        True if valid, False otherwise
    """
    if len(column_input) != 1:
        return False
    
    col_index = ord(column_input.upper()) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return False
    
    return True


def get_column_input(current_player, cols):
    """
    Get and validate column input from the player.
    
    Args:
        current_player: The current player's checker
        cols: Number of columns in the board
    
    Returns:
        The valid column index (0-based)
    """
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip()
        
        if not is_valid_column(user_input, cols):
            print("Invalid input. Please enter a single letter from A to " + 
                  chr(65 + cols - 1) + ".")
            continue
        
        col_index = ord(user_input.upper()) - ord('A')
        return col_index


def can_place_checker(board, col):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The game board
        col: The column index
    
    Returns:
        True if the column is not full, False otherwise
    """
    return board[0][col] == " "


def place_checker(board, col, player_checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board
        col: The column index
        player_checker: The player's checker symbol
    
    Returns:
        The row where the checker was placed, or -1 if column is full
    """
    rows = len(board)
    
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return row
    
    return -1


def check_horizontal_win(board, row, col, player_checker):
    """
    Check if there's a horizontal win at the given position.
    
    Args:
        board: The game board
        row: The row index
        col: The column index
        player_checker: The player's checker symbol
    
    Returns:
        True if there's a win, False otherwise
    """
    cols = len(board[0])
    count = 0
    
    # Check left to right
    for c in range(cols):
        if board[row][c] == player_checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    return False


def check_vertical_win(board, row, col, player_checker):
    """
    Check if there's a vertical win at the given position.
    
    Args:
        board: The game board
        row: The row index
        col: The column index
        player_checker: The player's checker symbol
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    count = 0
    
    # Check top to bottom
    for r in range(rows):
        if board[r][col] == player_checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    return False


def check_diagonal_win(board, row, col, player_checker):
    """
    Check if there's a diagonal win at the given position.
    
    Args:
        board: The game board
        row: The row index
        col: The column index
        player_checker: The player's checker symbol
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check diagonal from top-left to bottom-right
    count = 0
    for offset in range(-WIN_LENGTH + 1, WIN_LENGTH):
        r = row + offset
        c = col + offset
        if 0 <= r < rows and 0 <= c < cols and board[r][c] == player_checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal from top-right to bottom-left
    count = 0
    for offset in range(-WIN_LENGTH + 1, WIN_LENGTH):
        r = row + offset
        c = col - offset
        if 0 <= r < rows and 0 <= c < cols and board[r][c] == player_checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    return False


def check_win(board, row, col, player_checker):
    """
    Check if the current player has won.
    
    Args:
        board: The game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        player_checker: The player's checker symbol
    
    Returns:
        True if the player has won, False otherwise
    """
    return (check_horizontal_win(board, row, col, player_checker) or
            check_vertical_win(board, row, col, player_checker) or
            check_diagonal_win(board, row, col, player_checker))


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    board = initialize_board(ROWS, COLUMNS)
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_player = checkers[current_player_index]
        
        # Get valid column input from player
        while True:
            col = get_column_input(current_player, COLUMNS)
            
            if not can_place_checker(board, col):
                print("That column is full. Please choose another column.")
                continue
            
            break
        
        # Place the checker
        row = place_checker(board, col, current_player)
        
        # Print the updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """
    Entry point of the program.
    """
    play_game()


if __name__ == "__main__":
    main()
