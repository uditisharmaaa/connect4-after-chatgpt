import os
import random

# Constants for the game
ROWS = 6           # Number of rows in the board
COLS = 7           # Number of columns in the board
MAX_PLAYERS = 2    # Number of players (between 2 and 5)
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers symbols for players
WIN_CONDITION = 4  # Number of checkers in a row needed to win

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates and returns a board initialized with spaces.
    
    Args:
        rows (int): Number of rows.
        cols (int): Number of columns.
    
    Returns:
        list: 2D list representing the board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the board to the terminal in the required format.
    
    Args:
        board (list): 2D list representing the board.
    """
    clear_screen()
    # Print column headers, letters from A upwards
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(header)
    # Print each row separated by lines
    line = "+" + "---+" * len(board[0])
    for row in range(len(board)):
        print(line)
        print("| " + " | ".join(board[row]) + " |")
    print(line)

def get_valid_column_input(current_player, board):
    """
    Prompts the player to enter a valid column letter.
    
    Args:
        current_player (str): The checker symbol of the current player.
        board (list): Current board state.
    
    Returns:
        int: The column index to place the checker, or None if column full.
    """
    valid_columns = [chr(ord('A') + i) for i in range(len(board[0]))]
    while True:
        choice = input(f"Player {current_player}, please enter a column: ").strip().upper()
        # Validate input is a single letter in valid columns
        if len(choice) != 1 or choice not in valid_columns:
            print(f"Invalid input. Please enter a letter from {valid_columns[0]} to {valid_columns[-1]}.")
            continue
        col = ord(choice) - ord('A')
        # Check if the column is full (top cell is occupied)
        if board[0][col] != " ":
            # Invalid turn, loses the turn
            print(f"Column {choice} is full. You lose your turn.")
            return None
        return col

def place_checker(board, col, checker):
    """
    Places the checker in the specified column at the lowest available row.
    
    Args:
        board (list): Current board.
        col (int): Column index to place the checker.
        checker (str): Player's checker symbol.
    
    Returns:
        tuple: (row, col) position where checker was placed.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return (row, col)
    # Should not reach here if called properly (col has space)
    return None

def check_win(board, row, col, checker):
    """
    Checks if placing the checker at (row, col) caused a win.
    
    Args:
        board (list): Current board.
        row (int): Row index where last checker was placed.
        col (int): Column index where last checker was placed.
        checker (str): Checker symbol of current player.
    
    Returns:
        bool: True if player wins, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # Count the checker itself
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_CONDITION:
            return True
    return False

def board_full(board):
    """
    Checks if the board is completely filled.
    
    Args:
        board (list): Current board.
    
    Returns:
        bool: True if full, False otherwise.
    """
    return all(cell != " " for cell in board[0])

def main():
    # Initialize board and players
    board = create_board(ROWS, COLS)
    players = CHECKERS[:MAX_PLAYERS]
    
    # Randomly choose starting player index
    current_player_idx = random.randint(0, MAX_PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]

        col = get_valid_column_input(current_checker, board)
        if col is None:
            # Player loses turn (column full)
            # Move to next player
            current_player_idx = (current_player_idx + 1) % MAX_PLAYERS
            print_board(board)
            continue

        # Place checker
        row_col = place_checker(board, col, current_checker)
        print_board(board)

        # Check if current player won
        if check_win(board, row_col[0], row_col[1], current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % MAX_PLAYERS

if __name__ == "__main__":
    main()
