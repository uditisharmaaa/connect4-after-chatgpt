import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 checkers for 5 players

# Create the board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    # Print column headers
    headers = "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(f"  {headers}")
    print("+---" * COLUMNS + "+")
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Check for win conditions
def check_win(board, rows, columns, player_checker):
    # Check horizontal win
    for row in range(rows):
        for col in range(columns - 3):
            if all(board[row][col + i] == player_checker for i in range(4)):
                return True

    # Check vertical win
    for row in range(rows - 3):
        for col in range(columns):
            if all(board[row + i][col] == player_checker for i in range(4)):
                return True

    # Check diagonal win (bottom-left to top-right)
    for row in range(3, rows):
        for col in range(columns - 3):
            if all(board[row - i][col + i] == player_checker for i in range(4)):
                return True

    # Check diagonal win (top-left to bottom-right)
    for row in range(rows - 3):
        for col in range(columns - 3):
            if all(board[row + i][col + i] == player_checker for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Get valid column input from the player
def get_valid_column(board):
    while True:
        column = input("Please enter a column: ").strip().upper()
        if len(column) == 1 and column in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:COLUMNS]:
            col_index = ord(column) - 65
            if board[0][col_index] == " ":
                return col_index
            else:
                print("Column is full. Choose a different column.")
        else:
            print("Invalid input. Enter a valid column letter.")

# Place checker in the selected column
def place_checker(board, col_index, player_checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_checker
            break

# Main game logic
def connect_4():
    board = create_board(ROWS, COLUMNS)
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player = random.choice(players)

    print_board(board)
    print(f"Player {current_player} goes first!")

    while True:
        print(f"Player {current_player}'s turn.")
        col_index = get_valid_column(board)
        place_checker(board, col_index, current_player)

        print_board(board)

        if check_win(board, ROWS, COLUMNS, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    connect_4()
