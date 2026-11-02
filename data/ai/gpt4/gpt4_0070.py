import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def initialize_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    clear_screen()
    header = "  " + "   ".join(chr(65 + i) for i in range(cols))
    print(header)
    print("+---" * cols + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * cols + "+")

def is_valid_column(column, cols):
    return len(column) == 1 and column.isalpha() and 'A' <= column <= chr(65 + cols - 1)

def find_row_for_column(board, col_index):
    for row_index in range(ROWS - 1, -1, -1):
        if board[row_index][col_index] == " ":
            return row_index
    return -1

def check_winner(board, token):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == token for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == token for i in range(4)):
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == token for i in range(4)):
                return True

    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == token for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(all(cell != " " for cell in row) for row in board)

def main():
    # Initialize game variables
    board = initialize_board(ROWS, COLS)
    num_players = 2  # Default to 2 players
    players = PLAYER_TOKENS[:num_players]
    current_player = random.choice(players)

    # Game loop
    while True:
        print_board(board, COLS)
        print(f"Player {current_player}, it's your turn!")
        
        # Process input
        while True:
            column = input("Please enter a column: ").strip().upper()
            if not is_valid_column(column, COLS):
                print("Invalid column. Try again.")
                continue

            col_index = ord(column) - 65
            row_index = find_row_for_column(board, col_index)

            if row_index == -1:
                print("Column is full. Try again.")
            else:
                break

        # Place the checker
        board[row_index][col_index] = current_player

        # Check for a win
        if check_winner(board, current_player):
            print_board(board, COLS)
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if is_draw(board):
            print_board(board, COLS)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % num_players]

if __name__ == "__main__":
    main()
