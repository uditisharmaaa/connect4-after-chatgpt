import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the board with empty spaces.
    Returns a 2D list representing the game board.
    """
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board


def print_board(board, cols):
    """
    Print the game board in a formatted manner.
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        letter = chr(ord('A') + col)
        print(f" {letter}  ", end="")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * cols + "+")


def is_valid_column(col_letter, cols):
    """
    Check if the column input is valid.
    Returns the column index if valid, -1 otherwise.
    """
    if len(col_letter) != 1:
        return -1
    
    if not col_letter.isupper():
        return -1
    
    col_index = ord(col_letter) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return -1
    
    return col_index


def is_column_full(board, col_index, rows):
    """
    Check if a column is completely full.
    Returns True if full, False otherwise.
    """
    return board[0][col_index] != " "


def place_checker(board, col_index, checker, rows):
    """
    Place a checker in the specified column.
    Returns True if placement was successful, False otherwise.
    """
    if is_column_full(board, col_index, rows):
        return False
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False


def check_horizontal_win(board, rows, cols, checker):
    """
    Check if the specified checker has won horizontally.
    Returns True if there's a winning horizontal sequence, False otherwise.
    """
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, rows, cols, checker):
    """
    Check if the specified checker has won vertically.
    Returns True if there's a winning vertical sequence, False otherwise.
    """
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, rows, cols, checker):
    """
    Check if the specified checker has won diagonally.
    Returns True if there's a winning diagonal sequence, False otherwise.
    """
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


def check_win(board, rows, cols, checker):
    """
    Check if the specified checker has won the game.
    Returns True if the checker has won, False otherwise.
    """
    if check_horizontal_win(board, rows, cols, checker):
        return True
    if check_vertical_win(board, rows, cols, checker):
        return True
    if check_diagonal_win(board, rows, cols, checker):
        return True
    return False


def is_board_full(board, rows, cols):
    """
    Check if the board is completely full.
    Returns True if full, False otherwise.
    """
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def get_player_input(cols):
    """
    Get and validate player input for column choice.
    Returns the valid column index.
    """
    while True:
        col_letter = input("Please enter a column: ").strip()
        
        col_index = is_valid_column(col_letter, cols)
        
        if col_index == -1:
            print("Invalid input. Please enter a valid column letter (A-" + 
                  chr(ord('A') + cols - 1) + ").")
            continue
        
        return col_index


def play_game(board, rows, cols, num_players):
    """
    Main game loop. Manages turns, checker placement, and win checking.
    """
    # Randomly select first player
    current_player = random.randint(0, num_players - 1)
    
    # Print initial board
    print_board(board, cols)
    
    game_over = False
    
    while not game_over:
        checker = CHECKERS[current_player]
        player_label = chr(ord('X') + current_player) if current_player < 3 else CHECKERS[current_player]
        
        print(f"Player {checker}, please enter a column:")
        col_index = get_player_input(cols)
        
        # Try to place the checker
        if not place_checker(board, col_index, checker, rows):
            print("Column is full. Please choose another column.")
            continue
        
        # Print updated board
        print_board(board, cols)
        
        # Check for win
        if check_win(board, rows, cols, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board, rows, cols):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % num_players


def main():
    """
    Main function to initialize and start the game.
    """
    board = initialize_board(ROWS, COLS)
    play_game(board, ROWS, COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
