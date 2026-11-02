import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A to G
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(row) + '|')
        print('+' + '---+' * COLS)

def choose_first_player():
    return random.randint(0, len(PLAYERS) - 1)

def is_valid_input(column):
    if len(column) != 1:
        return False
    if column not in [chr(65 + i) for i in range(COLS)]:
        return False
    return True

def get_column_index(column):
    return ord(column) - 65

def place_checker(board, column, player):
    for row in reversed(board):
        if row[get_column_index(column)] == ' ':
            row[get_column_index(column)] = player
            return True
    return False

def check_win(board, player):
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
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = initialize_board()
    first_player_index = choose_first_player()
    current_player_index = first_player_index
    game_over = False

    while not game_over:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        column = input(f"Player {current_player}, please enter a column: ").strip().upper()

        while not is_valid_input(column) or not place_checker(board, column, current_player):
            print("Invalid input or column is full. Please try again.")
            column = input(f"Player {current_player}, please enter a column: ").strip().upper()

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
