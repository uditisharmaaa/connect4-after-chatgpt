import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = 'ABCDEFG'
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:5]  # Adjust number of players here

def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # For Linux/Mac; use 'cls' on Windows
    # Print column labels
    print(' ' + ' '.join(COLUMN_LABELS))
    # Print rows
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (2 * COLUMNS + 1))

def make_move(board, player, column):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return True
    return False

def validate_input(input_str):
    return input_str in COLUMN_LABELS

def check_winner(board, player):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col:col + 4] == [player] * 4:
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Diagonal check (bottom left to top right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Diagonal check (top left to bottom right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def connect_4_game():
    board = initialize_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        print(f"Player {current_player}'s turn. Choose a column (A-G):")

        valid_move = False
        while not valid_move:
            user_input = input().upper()
            if validate_input(user_input):
                column = COLUMN_LABELS.index(user_input)
                valid_move = make_move(board, current_player, column)
                if not valid_move:
                    print("Column is full. Choose another column.")
            else:
                print("Invalid input. Choose a column (A-G):")

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    connect_4_game()
