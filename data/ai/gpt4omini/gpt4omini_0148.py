import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the screen (for Linux/Unix)
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_empty_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return None

def is_winner(board, player):
    # Check horizontal, vertical and diagonal (/) and diagonal (\) for a win
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Diagonal (/) check
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    # Diagonal (\) check
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = initialize_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        col_input = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").strip().upper()

        if col_input not in [chr(65 + i) for i in range(COLS)]:
            print("Invalid column. Please enter a valid column (A-G).")
            continue

        col = ord(col_input) - 65
        empty_row = get_empty_row(board, col)

        if empty_row is None:
            print("Column is full. Try another column.")
            continue

        board[empty_row][col] = current_player
        print_board(board)

        if is_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
