import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+---+" + "---+" * (COLS - 1))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLS - 1))
        
def get_valid_column(player):
    while True:
        column_input = input(f"Player {player}, please enter a column: ").upper()
        if len(column_input) == 1 and 'A' <= column_input <= chr(64 + COLS):
            column_index = ord(column_input) - 65
            if board[0][column_index] == " ":
                return column_index
            else:
                print("This column is already full. Please choose another column.")
        else:
            print("Invalid input. Please enter a letter from A to " + chr(64 + COLS) + ".")

def drop_checker(board, column, player):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player
            return True
    return False

def check_win(board, player):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + i] == player for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game logic
board = create_board()
current_player_index = random.randint(0, len(PLAYERS) - 1)

print_board(board)
while True:
    current_player = PLAYERS[current_player_index]
    column = get_valid_column(current_player)
    drop_checker(board, column, current_player)
    print_board(board)

    if check_win(board, current_player):
        print(f"Player {current_player} won!")
        break
    if check_draw(board):
        print("It's a draw!")
        break
    
    current_player_index = (current_player_index + 1) % len(PLAYERS)
