import os
import random

# Game configuration constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(width, height):
    """
    Initialize the game board with empty spaces.
    
    Args:
        width: Number of columns
        height: Number of rows
    
    Returns:
        A 2D list representing the board
    """
    board = [[" " for _ in range(width)] for _ in range(height)]
    return board


def print_board(board):
    """
    Print the current state of the board.
    
    Args:
        board: 2D list representing the game board
    """
    os.system('clear')
    
    width = len(board[0])
    height = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(width):
        print(f"{chr(65 + col):^3} ", end="")
    print()
    
    # Print top border
    print("+" + "+".join(["---"] * width) + "+")
    
    # Print each row
    for row in range(height):
        print("|", end="")
        for col in range(width):
            print(f" {board[row][col]} |", end="")
        print()
        print("+" + "+".join(["---"] * width) + "+")


def is_valid_column(column_letter, width):
    """
    Check if the entered column letter is valid.
    
    Args:
        column_letter: String representing the column (e.g., 'A')
        width: Number of columns on the board
    
    Returns:
        True if valid, False otherwise
    """
    if len(column_letter) != 1:
        return False
    if not column_letter.isalpha():
        return False
    if column_letter.upper() < 'A' or column_letter.upper() >= chr(65 + width):
        return False
    return True


def get_column_index(column_letter):
    """
    Convert column letter to index.
    
    Args:
        column_letter: String representing the column (e.g., 'A')
    
    Returns:
        Integer index (0-based)
    """
    return ord(column_letter.upper()) - ord('A')


def can_place_checker(board, col_index):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: 2D list representing the game board
        col_index: 0-based column index
    
    Returns:
        True if the column has space, False otherwise
    """
    return board[0][col_index] == " "


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: 2D list representing the game board
        col_index: 0-based column index
        checker: Character representing the player's checker
    
    Returns:
        Row index where the checker was placed, or -1 if placement failed
    """
    height = len(board)
    
    # Find the lowest empty space in the column
    for row in range(height - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    
    return -1


def check_win(board, row, col, checker):
    """
    Check if the last placed checker at (row, col) results in a win.
    
    Args:
        board: 2D list representing the game board
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        checker: Character representing the player's checker
    
    Returns:
        True if there's a winning condition, False otherwise
    """
    height = len(board)
    width = len(board[0])
    
    # Check horizontal
    count = 1
    # Check left
    j = col - 1
    while j >= 0 and board[row][j] == checker:
        count += 1
        j -= 1
    # Check right
    j = col + 1
    while j < width and board[row][j] == checker:
        count += 1
        j += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    i = row - 1
    while i >= 0 and board[i][col] == checker:
        count += 1
        i -= 1
    # Check down
    i = row + 1
    while i < height and board[i][col] == checker:
        count += 1
        i += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0 and board[i][j] == checker:
        count += 1
        i -= 1
        j -= 1
    # Check down-right
    i, j = row + 1, col + 1
    while i < height and j < width and board[i][j] == checker:
        count += 1
        i += 1
        j += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    i, j = row - 1, col + 1
    while i >= 0 and j < width and board[i][j] == checker:
        count += 1
        i -= 1
        j += 1
    # Check down-left
    i, j = row + 1, col - 1
    while i < height and j >= 0 and board[i][j] == checker:
        count += 1
        i += 1
        j -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: 2D list representing the game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_player_move(current_player, checker, board_width):
    """
    Get valid input from the current player.
    
    Args:
        current_player: Player number (1-based)
        checker: Character representing the player's checker
        board_width: Number of columns on the board
    
    Returns:
        0-based column index where the checker should be placed
    """
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip()
        
        if not is_valid_column(user_input, board_width):
            print(f"Invalid input! Please enter a letter between A and {chr(65 + board_width - 1)}.")
            continue
        
        col_index = get_column_index(user_input)
        
        if not can_place_checker(board, col_index):
            print(f"Column {user_input} is full! Please choose another column.")
            continue
        
        return col_index


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(BOARD_WIDTH, BOARD_HEIGHT)
    
    # Determine player order
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)
    current_player_index = 0
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    winner = None
    
    while not game_over:
        current_player = players[current_player_index]
        checker = CHECKERS[current_player]
        
        # Get player move
        col_index = get_player_move(current_player + 1, checker, BOARD_WIDTH)
        
        # Place checker
        row_index = place_checker(board, col_index, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, checker):
            print(f"Player {checker} won!")
            game_over = True
            winner = current_player
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        # Switch to next player
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """
    Entry point for the Connect 4 game.
    """
    play_game()


if __name__ == "__main__":
    main()
