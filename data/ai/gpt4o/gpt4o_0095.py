import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" "] * COLUMNS for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    header = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(header)
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_move(column, board):
    return 0 <= column < COLUMNS and board[0][column] == " "

def make_move(player_symbol, column, board):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player_symbol
            return True
    return False

def check_winner(board):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            symbol = board[row][col]
            if symbol != " " and all(board[row][col + i] == symbol for i in range(4)):
                return symbol

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            symbol = board[row][col]
            if symbol != " " and all(board[row + i][col] == symbol for i in range(4)):
                return symbol

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            symbol = board[row][col]
            if symbol != " " and all(board[row + i][col + i] == symbol for i in range(4)):
                return symbol

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            symbol = board[row][col]
            if symbol != " " and all(board[row - i][col + i] == symbol for i in range(4)):
                return symbol

    return None

def is_full(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def get_player_input(current_player):
    while True:
        try:
            column_input = input(f"Player {PLAYER_SYMBOLS[current_player]}, please enter a column: ")
            column = ord(column_input.upper()) - ord('A')
            return column
        except (IndexError, ValueError):
            print("Invalid input. Please enter a valid column letter.")

def main():
    board = create_board()
    print_board(board)
    num_players = 2  # Set number of players to 2 for submission
    current_player = random.randint(0, num_players - 1)

    while True:
        move_column = get_player_input(current_player)
        if is_valid_move(move_column, board):
            make_move(PLAYER_SYMBOLS[current_player], move_column, board)
            print_board(board)
            winner = check_winner(board)
            if winner:
                print(f"Player {winner} won!")
                break
            elif is_full(board):
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % num_players
        else:
            print("Column is full or invalid, try another column.")

if __name__ == "__main__":
    main()
