import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # Tokens for players
NUM_PLAYERS = 2  # Change this from 2 to 5 depending on the number of players

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  A B C D E F G")
    for row in board:
        print("|" + "|".join(row) + "|")
    print("+" + "-+" * COLUMNS)

def is_valid_column(column, board):
    if 0 <= column < COLUMNS and board[0][column] == ' ':
        return True
    return False

def get_valid_move(board):
    while True:
        column_letter = input("Enter the column (A-G): ").strip().upper()
        if column_letter in "ABCDEFG":
            column = ord(column_letter) - ord('A')
            if is_valid_column(column, board):
                return column
        print("Invalid input. Try again.")

def make_move(board, column, token):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = token
            break

def is_winner(board, token):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == token for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == token for i in range(4)):
                return True

    # Check diagonal /
    for col in range(COLUMNS - 3):
        for row in range(3, ROWS):
            if all(board[row - i][col + i] == token for i in range(4)):
                return True

    # Check diagonal \
    for col in range(COLUMNS - 3):
        for row in range(ROWS - 3):
            if all(board[row + i][col + i] == token for i in range(4)):
                return True

    return False

def is_board_full(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def play_game():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {PLAYER_TOKENS[current_player]}'s turn")
        column = get_valid_move(board)
        make_move(board, column, PLAYER_TOKENS[current_player])
        print_board(board)

        if is_winner(board, PLAYER_TOKENS[current_player]):
            print(f"Player {PLAYER_TOKENS[current_player]} wins!")
            break
        elif is_board_full(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
