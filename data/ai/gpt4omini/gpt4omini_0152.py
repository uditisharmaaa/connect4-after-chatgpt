import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" + "---+" * (COLS - 1) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * (COLS - 1) + "---+")

def get_valid_input(player):
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1):
            return ord(column) - 65
        print("Invalid input! Please enter a valid column (A-G).")

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in board:
        for c in range(COLS - 3):
            if all(cell == checker for cell in row[c:c + 4]):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    random_player_index = random.randint(0, len(PLAYERS) - 1)
    current_player_index = random_player_index

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]

        while True:
            col = get_valid_input(current_player)
            if place_checker(board, col, current_player):
                break
            print("Column is full! Please choose another column.")

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            return

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            return

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
