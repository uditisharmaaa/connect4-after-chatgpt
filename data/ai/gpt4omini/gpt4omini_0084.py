import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clears the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column labels A, B, C, ...
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_next_free_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1  # Column is full

def check_winner(board, player):
    # Check horizontal, vertical, and diagonal (both directions)
    for row in range(ROWS):
        for col in range(COLUMNS):
            if col + 3 < COLUMNS and all(board[row][col + i] == player for i in range(4)):  # Horizontal
                return True
            if row + 3 < ROWS and all(board[row + i][col] == player for i in range(4)):  # Vertical
                return True
            if row + 3 < ROWS and col + 3 < COLUMNS and all(board[row + i][col + i] == player for i in range(4)):  # Diagonal \
                return True
            if row - 3 >= 0 and col + 3 < COLUMNS and all(board[row - i][col + i] == player for i in range(4)):  # Diagonal /
                return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def get_valid_input(player):
    while True:
        col = input(f"Player {player}, please enter a column (A-{chr(65 + COLUMNS - 1)}): ").upper()
        if col in [chr(65 + i) for i in range(COLUMNS)]:
            return ord(col) - 65  # Convert letter to index
        print("Invalid input. Try again.")

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    print_board(board)

    while True:
        player = PLAYERS[current_player_index]
        col = get_valid_input(player)
        row = get_next_free_row(board, col)
        if row != -1:
            board[row][col] = player
            print_board(board)

            if check_winner(board, player):
                print(f"Player {player} won!")
                break

            if check_draw(board):
                print("The game is a draw!")
                break

            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print(f"Column {chr(65 + col)} is full, try again.")

if __name__ == "__main__":
    main()
