import os
import random

# Constants for the board dimensions and number of players
NUM_COLUMNS = 7
NUM_ROWS = 6
NUM_PLAYERS = 2  # Change this to between 2 and 5 for more players

# Constants for checkers for each player
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def create_board(rows, columns):
    """Creates the initial game board."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the game board."""
    os.system('clear')
    header = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(row) + "+")

def check_valid_input(column_input, columns, board):
    """Checks if the user input is valid."""
    if len(column_input) != 1 or not column_input.isalpha():
        return False
    column_index = ord(column_input.upper()) - 65
    if column_index < 0 or column_index >= columns or board[0][column_index] != " ":
        return False
    return True

def place_checker(board, column, checker):
    """Places the checker in the correct position on the board."""
    column_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            break

def check_win(board, checker):
    """Checks if current player won the game."""
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True
    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    # Check diagonal /
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Check diagonal \
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def play_game():
    """Main game function to play Connect 4."""
    board = create_board(NUM_ROWS, NUM_COLUMNS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        print_board(board)
        player_checker = CHECKERS[current_player]
        column_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        while not check_valid_input(column_input, NUM_COLUMNS, board):
            column_input = input(f"Invalid input. Player {player_checker}, please enter a valid column: ").strip().upper()

        place_checker(board, column_input, player_checker)

        if check_win(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

play_game()
