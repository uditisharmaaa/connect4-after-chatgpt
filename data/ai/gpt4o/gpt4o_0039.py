import os
import random

# Constants for dimensions and players
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board with whitespaces
def create_board(rows, columns):
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board

# Display the board
def display_board(board):
    os.system('clear')
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Get the column index from a letter
def get_column_index(column, num_columns):
    index = ord(column) - ord('A')
    if index < 0 or index >= num_columns:
        raise ValueError("Invalid column")
    return index

# Place the checker in the board
def place_checker(board, column, checker):
    column_index = get_column_index(column, len(board[0]))
    for row_index in range(len(board) - 1, -1, -1):
        if board[row_index][column_index] == " ":
            board[row_index][column_index] = checker
            return row_index, column_index
    raise ValueError("Column is full")

# Check for a win condition in the board
def check_win(board, last_row, last_col, checker):
    # Check directions: horizontal, vertical, diagonal1, diagonal2
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 0
        for step in range(-3, 4):
            r = last_row + step * dr
            c = last_col + step * dc
            if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    return False

# Check if the board is a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(len(board[0])))

# The main game loop
def connect4():
    board = create_board(ROWS, COLUMNS)
    display_board(board)
    
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    while True:
        print(f"Player {current_player}, please enter a column:")
        while True:
            try:
                column_choice = input().strip()
                row, col = place_checker(board, column_choice, current_player)
                break
            except ValueError as e:
                print(e, "Try again.")

        display_board(board)
        
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break
        else:
            current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

# Start the game
connect4()
