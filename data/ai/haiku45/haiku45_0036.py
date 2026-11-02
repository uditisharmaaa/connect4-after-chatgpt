import os
import random

# Global constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the board with all empty spaces.
    
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
    Print the board in a formatted way with column labels and borders.
    
    Args:
        board: The 2D list representing the board
    """
    rows = len(board)
    cols = len(board[0])
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print each row
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


def get_valid_column(board, num_players, current_player):
    """
    Get a valid column input from the current player.
    
    Args:
        board: The 2D list representing the board
        num_players: Total number of players
        current_player: Index of the current player (0-based)
    
    Returns:
        The column index (0-based) where the checker should be placed
    """
    cols = len(board[0])
    
    while True:
        player_checker = CHECKERS[current_player]
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("That column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col, current_player):
    """
    Place a checker in the specified column.
    
    Args:
        board: The 2D list representing the board
        col: The column index (0-based)
        current_player: Index of the current player (0-based)
    
    Returns:
        True if placement was successful, False otherwise
    """
    rows = len(board)
    checker = CHECKERS[current_player]
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_horizontal_win(board, rows, cols, win_length):
    """
    Check if there is a horizontal win on the board.
    
    Args:
        board: The 2D list representing the board
        rows: Number of rows
        cols: Number of columns
        win_length: Number of checkers in a row needed to win
    
    Returns:
        The checker that won, or None if no win
    """
    for row in range(rows):
        for col in range(cols - win_length + 1):
            checker = board[row][col]
            if checker != " ":
                # Check if all next win_length-1 checkers are the same
                if all(board[row][col + i] == checker for i in range(win_length)):
                    return checker
    
    return None


def check_vertical_win(board, rows, cols, win_length):
    """
    Check if there is a vertical win on the board.
    
    Args:
        board: The 2D list representing the board
        rows: Number of rows
        cols: Number of columns
        win_length: Number of checkers in a row needed to win
    
    Returns:
        The checker that won, or None if no win
    """
    for col in range(cols):
        for row in range(rows - win_length + 1):
            checker = board[row][col]
            if checker != " ":
                # Check if all next win_length-1 checkers are the same
                if all(board[row + i][col] == checker for i in range(win_length)):
                    return checker
    
    return None


def check_diagonal_win(board, rows, cols, win_length):
    """
    Check if there is a diagonal win on the board.
    
    Args:
        board: The 2D list representing the board
        rows: Number of rows
        cols: Number of columns
        win_length: Number of checkers in a row needed to win
    
    Returns:
        The checker that won, or None if no win
    """
    # Check diagonals going down-right
    for row in range(rows - win_length + 1):
        for col in range(cols - win_length + 1):
            checker = board[row][col]
            if checker != " ":
                if all(board[row + i][col + i] == checker for i in range(win_length)):
                    return checker
    
    # Check diagonals going down-left
    for row in range(rows - win_length + 1):
        for col in range(win_length - 1, cols):
            checker = board[row][col]
            if checker != " ":
                if all(board[row + i][col - i] == checker for i in range(win_length)):
                    return checker
    
    return None


def check_win(board, win_length):
    """
    Check if there is a win on the board.
    
    Args:
        board: The 2D list representing the board
        win_length: Number of checkers in a row needed to win
    
    Returns:
        The checker that won, or None if no win
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    winner = check_horizontal_win(board, rows, cols, win_length)
    if winner:
        return winner
    
    # Check vertical
    winner = check_vertical_win(board, rows, cols, win_length)
    if winner:
        return winner
    
    # Check diagonal
    winner = check_diagonal_win(board, rows, cols, win_length)
    if winner:
        return winner
    
    return None


def check_draw(board):
    """
    Check if the board is full (draw condition).
    
    Args:
        board: The 2D list representing the board
    
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
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Clear screen and print initial board
    os.system('clear')
    print_board(board)
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Game loop
    while True:
        # Get valid column from current player
        col = get_valid_column(board, NUM_PLAYERS, current_player)
        
        # Place the checker
        place_checker(board, col, current_player)
        
        # Clear screen and print updated board
        os.system('clear')
        print_board(board)
        
        # Check for win
        winner = check_win(board, WIN_LENGTH)
        if winner:
            winner_index = CHECKERS.index(winner)
            print(f"Player {winner} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


def main():
    """
    Entry point for the program.
    """
    play_game()


if __name__ == "__main__":
    main()
