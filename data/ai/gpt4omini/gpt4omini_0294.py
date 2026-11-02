import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear screen
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def choose_first_player():
    return random.randint(0, len(PLAYERS) - 1)

def is_valid_input(column):
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(ord('A') + COLS - 1)

def place_checker(board, column, player):
    col_index = ord(column) - ord('A')
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = player
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

    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = choose_first_player()
    current_player = PLAYERS[current_player_index]
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        column = input().upper()

        if not is_valid_input(column):
            print("Invalid input. Please enter a letter from A to " + chr(ord('A') + COLS - 1))
            continue

        if not place_checker(board, column, current_player):
            print("Column is full. Please choose another column.")
            continue

        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)
        current_player = PLAYERS[current_player_index]

if __name__ == "__main__":
    main()
