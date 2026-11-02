import os
import random

# Constants for players
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 4  # You can set this between 2 and 5

ROWS = 6
COLUMNS = 7
COLUMN_LABELS = "ABCDEFG"

def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print(" " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (2 * COLUMNS + 1))

def drop_piece(board, column, piece):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = piece
            return True
    return False

def is_valid_move(board, column):
    return board[0][column] == ' '

def get_column_choice():
    choice = input("Choose a column (A-G): ").upper()
    if choice in COLUMN_LABELS:
        return COLUMN_LABELS.index(choice)
    return None

def check_win(board, piece):
    # Horizontal Check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == piece for i in range(4)):
                return True
    # Vertical Check
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == piece for i in range(4)):
                return True
    # Positive Diagonal Check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True
    # Negative Diagonal Check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == piece for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def play_game():
    board = initialize_board()
    player_turn = random.randint(0, NUM_PLAYERS - 1)
    game_running = True

    while game_running:
        print_board(board)
        print(f"Player {PLAYERS[player_turn]}'s turn")

        column = None
        while column is None or not is_valid_move(board, column):
            column = get_column_choice()
            if column is not None and not is_valid_move(board, column):
                print("Column is full. Choose another.")

        drop_piece(board, column, PLAYERS[player_turn])

        if check_win(board, PLAYERS[player_turn]):
            print_board(board)
            print(f"Player {PLAYERS[player_turn]} wins!")
            game_running = False
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_running = False

        player_turn = (player_turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
