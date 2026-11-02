import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, columns):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the game board to the console.
    
    Args:
        board: The game board to print
    """
    columns = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for i in range(columns):
        print(chr(ord('A') + i), end="   ")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(columns):
        print("---+", end="")
    print()
    
    # Print board rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        
        # Print row border
        print("+", end="")
        for _ in range(columns):
            print("---+", end="")
        print()


def clear_screen():
    """Clear the console screen."""
    os.system('clear')


def get_player_input(player_checker, columns):
    """
    Get valid column input from the current player.
    
    Args:
        player_checker: The checker symbol of the current player
        columns: Number of columns in the board
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Validate input length
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Validate input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        column_index = ord(user_input) - ord('A')
        
        # Validate column is within board range
        if column_index < 0 or column_index >= columns:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + columns - 1)}.")
            continue
        
        return column_index


def place_checker(board, column, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board
        column: The column index where the checker should be placed
        checker: The checker symbol to place
    
    Returns:
        True if the checker was placed successfully, False if the column is full
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False


def check_win(board, row, column, checker):
    """
    Check if the current move results in a win.
    
    Args:
        board: The game board
        row: The row where the checker was placed
        column: The column where the checker was placed
        checker: The checker symbol that was placed
    
    Returns:
        True if the player won, False otherwise
    """
    rows = len(board)
    columns = len(board[0])
    
    # Directions: horizontal, vertical, diagonal (top-left to bottom-right), diagonal (top-right to bottom-left)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dx, dy in directions:
        count = 1
        
        # Check in the positive direction
        x, y = row + dx, column + dy
        while 0 <= x < rows and 0 <= y < columns and board[x][y] == checker:
            count += 1
            x += dx
            y += dy
        
        # Check in the negative direction
        x, y = row - dx, column - dy
        while 0 <= x < rows and 0 <= y < columns and board[x][y] == checker:
            count += 1
            x -= dx
            y -= dy
        
        # Check if we have 4 or more in a row
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    
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


def get_next_player(current_player_index, num_players):
    """
    Get the index of the next player.
    
    Args:
        current_player_index: The index of the current player
        num_players: The total number of players
    
    Returns:
        The index of the next player
    """
    return (current_player_index + 1) % num_players


def main():
    """Main game loop."""
    clear_screen()
    
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Create list of players
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        current_player = players[current_player_index]
        
        # Get valid input from the player
        valid_move = False
        while not valid_move:
            column = get_player_input(current_player, COLUMNS)
            valid_move = place_checker(board, column, current_player)
        
        # Clear screen and print updated board
        clear_screen()
        print_board(board)
        
        # Find the row where the checker was placed
        for row in range(ROWS):
            if board[row][column] == current_player:
                placed_row = row
                break
        
        # Check for win
        if check_win(board, placed_row, column, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = get_next_player(current_player_index, NUM_PLAYERS)


if __name__ == "__main__":
    main()
