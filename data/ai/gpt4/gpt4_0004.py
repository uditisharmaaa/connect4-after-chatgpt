# Importing necessary libraries
import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # Max columns for future adjustments
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Supports up to 5 players

def initialize_board(rows, cols):
    """
    Create an empty board 
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Print the Connect 4 board
    """
    os.system('clear')  # Clear the terminal
    column_labels = "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {column_labels}")
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def is_valid_column(column, board):
    """
    Check if a column input is valid
    """
    if not column.isalpha() or len(column) != 1:
        return False
    col_index = ord(column.upper()) - 65
    if col_index < 0 or col_index >= len(board[0]) or board[0][col_index] != " ":
        return False
    return True

def get_next_open_row(board, col_index):
    """
    Get the next open row in a specific column
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == " ":
            return row
    return None

def drop_checker(board, col_index, checker):
    """
    Drop a checker into the chosen column
    """
    row_index = get_next_open_row(board, col_index)
    if row_index is not None:
        board[row_index][col_index] = checker

def check_for_win(board, checker):
    """
    Check if the player with 'checker' has won the game
    """
    rows, cols = len(board), len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Vertical check
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Diagonal (\) check
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Diagonal (/) check
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    """
    Check if the board is completely filled (draw)
    """
    return all(board[0][col] != " " for col in range(len(board[0])))

def get_player_input(player_checker, board):
    """
    Get valid input for the player's move
    """
    while True:
        column = input(f"Player {player_checker}, please enter a column: ").upper()
        if is_valid_column(column, board):
            return ord(column) - 65  # Convert column letter to index
        print("Invalid input. Please enter a valid column.")

def main():
    # Initialize the game
    board = initialize_board(ROWS, COLUMNS)
    checkers = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)  # Randomly select the first player
    game_over = False

    # Print initial board
    print_board(board)

    while not game_over:
        # Get current player's checker
        player_checker = checkers[current_player]

        # Get player input
        col_index = get_player_input(player_checker, board)

        # Drop the player's checker
        drop_checker(board, col_index, player_checker)

        # Print the updated board
        print_board(board)

        # Check for a win or draw
        if check_for_win(board, player_checker):
            print(f"Player {player_checker} won!")
            game_over = True
        elif check_for_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to the next player
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
