import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Adjust for more players as needed

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clearing the console
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C...
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def get_valid_input(player):
    while True:
        col = input(f"Player {player}, please enter a column: ").upper()
        if len(col) != 1 or col < 'A' or col >= chr(65 + COLS):
            print("Invalid input. Please enter a column from A to " + chr(65 + COLS - 1) + ".")
        else:
            return ord(col) - 65  # Convert from char to column index

def drop_checker(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return True
    return False

def check_winner(board, player):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    # Check diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True

    # Check diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = initialize_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    game_over = False

    while not game_over:
        print_board(board)
        current_player = PLAYERS[current_player_index]

        col = get_valid_input(current_player)
        if drop_checker(board, col, current_player):
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("The game is a draw!")
                game_over = True
            else:
                current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print(f"Column {chr(65 + col)} is full. Please choose another column.")

if __name__ == "__main__":
    main()
