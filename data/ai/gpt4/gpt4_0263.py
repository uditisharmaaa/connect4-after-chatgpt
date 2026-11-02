import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]  # Checkers for up to 5 players
EMPTY_CELL = " "

# Functions
def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[EMPTY_CELL for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    column_headers = "   ".join(chr(65 + i) for i in range(COLUMNS))  # A, B, C, ...
    print("  " + column_headers)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    if not column.isalpha() or len(column) != 1:
        return False
    index = ord(column.upper()) - 65  # Convert column letter to index
    return 0 <= index < COLUMNS and board[0][index] == EMPTY_CELL

def get_column_index(column):
    return ord(column.upper()) - 65

def drop_checker(board, column_index, checker):
    for row in reversed(board):  # Start from the bottom row
        if row[column_index] == EMPTY_CELL:
            row[column_index] = checker
            return True
    return False

def has_winner(board, checker):
    # Check horizontal, vertical, and diagonal patterns for a win
    for row in range(ROWS):
        for col in range(COLUMNS):
            if col + 3 < COLUMNS and all(board[row][col + i] == checker for i in range(4)):
                return True
            if row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4)):
                return True
            if row + 3 < ROWS and col + 3 < COLUMNS and all(board[row + i][col + i] == checker for i in range(4)):
                return True
            if row + 3 < ROWS and col - 3 >= 0 and all(board[row + i][col - i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != EMPTY_CELL for row in board for cell in row)

# Main
def connect4():
    clear_screen()
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Set to 2 for this assignment (can modify for more players)
    players = PLAYERS[:num_players]
    
    current_player_index = random.randint(0, num_players - 1)  # Randomly select first player
    winner = None

    print_board(board)

    while not winner and not is_draw(board):
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")

        column = input().strip()
        while not is_valid_column(column, board):
            print(f"Invalid input. Player {current_player}, please enter a valid column:")
            column = input().strip()
        
        column_index = get_column_index(column)
        drop_checker(board, column_index, current_player)
        clear_screen()
        print_board(board)
        
        if has_winner(board, current_player):
            winner = current_player
        else:
            current_player_index = (current_player_index + 1) % num_players
    
    if winner:
        print(f"Player {winner} won!")
    else:
        print("The game is a draw!")

# Start the game
if __name__ == "__main__":
    connect4()
