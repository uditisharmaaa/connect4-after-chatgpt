import os
import random

# Constants for the game
ROWS = 6              # Number of rows on the board
COLUMNS = 7           # Number of columns on the board (max 26)
PLAYERS = 2           # Number of players (2-5)
WIN_LENGTH = 4        # Number of checkers in a row needed to win

# Checkers for players in order
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """
    Clears the terminal screen using 'clear' command.
    """
    os.system('clear')

def create_board(rows, columns):
    """
    Creates a game board (list of lists) initialized with spaces.
    :param rows: Number of rows
    :param columns: Number of columns
    :return: 2D list representing the board
    """
    return [[" " for _ in range(columns)] for __ in range(rows)]

def print_board(board):
    """
    Prints the board to the terminal with column labels.
    The top row shows column letters (A-G etc).
    """
    clear_screen()
    # Print column labels
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    # Print each row with separators
    line_sep = "+" + "---+" * len(board[0])
    for row in range(len(board)):
        print(line_sep)
        print("| " + " | ".join(board[row]) + " |")
    print(line_sep)

def is_valid_column(column_letter, columns):
    """
    Validates if the input is a single uppercase letter corresponding
    to a column on the board.
    :param column_letter: User input character
    :param columns: Number of columns
    :return: True if valid, else False
    """
    if len(column_letter) != 1:
        return False
    if not column_letter.isalpha():
        return False
    col_index = ord(column_letter) - ord('A')
    return 0 <= col_index < columns

def get_lowest_empty_row(board, col_index):
    """
    Finds the lowest empty row in given column where a checker can be placed.
    Returns row index or -1 if column is full.
    :param board: The game board
    :param col_index: Column index
    :return: Row index or -1
    """
    for row in reversed(range(len(board))):
        if board[row][col_index] == " ":
            return row
    return -1

def place_checker(board, col_index, checker):
    """
    Places the player's checker in the lowest available position in the column.
    Returns True if the checker was placed, False if column is full.
    :param board: The game board
    :param col_index: Column index
    :param checker: Player's checker symbol
    :return: True if placed, else False
    """
    row = get_lowest_empty_row(board, col_index)
    if row == -1:
        return False
    board[row][col_index] = checker
    return True

def check_win(board, checker):
    """
    Check if the player with given checker has a connect-4 on the board.
    Checks horizontally, vertically and both diagonal directions.
    :param board: The game board
    :param checker: Player's checker symbol
    :return: True if player won, else False
    """
    rows = len(board)
    cols = len(board[0])
    
    # Horizontal check
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + offset] == checker for offset in range(WIN_LENGTH)):
                return True
    
    # Vertical check
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + offset][col] == checker for offset in range(WIN_LENGTH)):
                return True
    
    # Diagonal check (\ direction)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + offset][col + offset] == checker for offset in range(WIN_LENGTH)):
                return True
    
    # Diagonal check (/ direction)
    for row in range(WIN_LENGTH - 1, rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row - offset][col + offset] == checker for offset in range(WIN_LENGTH)):
                return True
    
    return False

def check_draw(board):
    """
    Check if the board is full (draw).
    :param board: The game board
    :return: True if full, else False
    """
    return all(cell != " " for row in board for cell in row)

def get_player_input(player_checker, columns):
    """
    Prompts the player to enter a column letter, validates the input.
    Repeats until a valid input is given.
    :param player_checker: Current player's checker symbol
    :param columns: Number of columns on board
    :return: Column index (int)
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(user_input, columns):
            print(f"Invalid input! Enter a letter between A and {chr(ord('A')+columns-1)}.")
            continue
        col_index = ord(user_input) - ord('A')
        return col_index

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    
    # Randomly select starting player
    current_player_index = random.randint(0, PLAYERS - 1)
    current_player_checker = players[current_player_index]
    
    print_board(board)
    
    while True:
        # Prompt current player for input and validate
        col_index = get_player_input(current_player_checker, COLUMNS)
        
        placed = place_checker(board, col_index, current_player_checker)
        if not placed:
            # Column full, player loses the turn
            print(f"Column {chr(col_index + ord('A'))} is full. Player {current_player_checker} loses the turn.")
            # Switch to next player
        else:
            print_board(board)
            # Check if current player won
            if check_win(board, current_player_checker):
                print(f"Player {current_player_checker} won!")
                break
            # Check for draw
            if check_draw(board):
                print("The game is a draw!")
                break
            # Switch to next player only if turn was successful
            current_player_index = (current_player_index + 1) % PLAYERS
            current_player_checker = players[current_player_index]
            continue
        
        # If turn lost due to full column, move to next player and print board unchanged
        print_board(board)
        current_player_index = (current_player_index + 1) % PLAYERS
        current_player_checker = players[current_player_index]

if __name__ == "__main__":
    main()
