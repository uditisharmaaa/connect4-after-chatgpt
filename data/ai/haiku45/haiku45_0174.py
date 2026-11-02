import os
import random

# Constants for game configuration
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def initialize_board(rows, columns):
    """
    Create and return a two-dimensional board with all elements initialized to whitespace.
    """
    board = []
    for i in range(rows):
        row = []
        for j in range(columns):
            row.append(" ")
        board.append(row)
    return board

def print_board(board, columns):
    """
    Print the current state of the board.
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for i in range(columns):
        print(chr(65 + i), end="   ")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * columns + "+")
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
    print("+---" * columns + "+")

def get_column_input(columns):
    """
    Get valid column input from the player.
    Return the column index (0-based).
    """
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col_index < 0 or col_index >= columns:
            print("Invalid column. Please enter a letter between A and " + chr(65 + columns - 1) + ".")
            continue
        
        return col_index

def place_checker(board, column, checker, rows, columns):
    """
    Place a checker in the specified column.
    Return True if successful, False if column is full.
    """
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    
    # Column is full
    return False

def check_horizontal_win(board, rows, columns, checker):
    """
    Check if the specified checker has won horizontally.
    """
    for row in range(rows):
        for col in range(columns - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row][col + i] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    return False

def check_vertical_win(board, rows, columns, checker):
    """
    Check if the specified checker has won vertically.
    """
    for col in range(columns):
        for row in range(rows - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    return False

def check_diagonal_win(board, rows, columns, checker):
    """
    Check if the specified checker has won diagonally.
    """
    # Check diagonal going down-right
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(columns - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col + i] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check diagonal going down-left
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, columns):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col - i] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    return False

def check_win(board, rows, columns, checker):
    """
    Check if the specified checker has won (horizontally, vertically, or diagonally).
    """
    if check_horizontal_win(board, rows, columns, checker):
        return True
    if check_vertical_win(board, rows, columns, checker):
        return True
    if check_diagonal_win(board, rows, columns, checker):
        return True
    return False

def is_board_full(board, rows, columns):
    """
    Check if the board is completely full.
    """
    for row in range(rows):
        for col in range(columns):
            if board[row][col] == " ":
                return False
    return True

def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLUMNS)
    
    # Game loop
    game_over = False
    
    while not game_over:
        current_player = CHECKERS[current_player_index]
        
        print("Player " + current_player + ", ", end="")
        
        # Get valid column input
        column = get_column_input(COLUMNS)
        
        # Try to place checker
        if not place_checker(board, column, current_player, ROWS, COLUMNS):
            print("Column is full. You lose your turn.")
            print_board(board, COLUMNS)
        else:
            # Print board after move
            print_board(board, COLUMNS)
            
            # Check for win
            if check_win(board, ROWS, COLUMNS, current_player):
                print("Player " + current_player + " won!")
                game_over = True
            # Check for draw
            elif is_board_full(board, ROWS, COLUMNS):
                print("It's a draw!")
                game_over = True
        
        # Move to next player if game is not over
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """
    Start the game.
    """
    play_game()

if __name__ == "__main__":
    main()
