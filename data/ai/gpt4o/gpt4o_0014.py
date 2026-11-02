import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Create board
def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

# Print board
def print_board(board):
    os.system('clear')
    column_labels = ' '.join([chr(65+i) for i in range(len(board[0]))])
    print(f"  {column_labels}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Validate user input for column choice
def get_valid_column_input(board):
    columns = len(board[0])
    while True:
        try:
            user_input = input("Please enter a column (A to {}): ".format(chr(65 + columns - 1)))
            col_index = ord(user_input.upper()) - 65
            if 0 <= col_index < columns:
                return col_index
            else:
                print("Invalid column! Please try again.")
        except (ValueError, TypeError):
            print("Invalid input! Please try again.")

# Place checker in the column
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

# Check for win
def check_for_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] == checker:
                return True
    
    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] == checker:
                return True
    
    # Check diagonal (bottom-left to top-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] == checker:
                return True

    return False

# Check for draw
def check_for_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game loop
def play_game(num_players):
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:num_players]
    random.shuffle(players)
    current_player_index = 0

    while True:
        print_board(board)
        print(f"Player {players[current_player_index]}'s turn.")
        
        column = get_valid_column_input(board)
        if board[0][column] != ' ':
            print("Column full! You lose your turn.")
            current_player_index = (current_player_index + 1) % num_players
            continue

        place_checker(board, column, players[current_player_index])

        if check_for_win(board, players[current_player_index]):
            print_board(board)
            print(f"Player {players[current_player_index]} won!")
            break

        if check_for_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % num_players

# Set number of players and start the game with specified dimensions and players
num_players = 2
play_game(num_players)
