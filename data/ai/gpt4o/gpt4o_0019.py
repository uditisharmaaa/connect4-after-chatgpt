import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # Choose symbols according to number of players

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    column_labels = ' '.join([chr(65 + i) for i in range(len(board[0]))])
    print(f"  {column_labels}")
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(row))

def get_column_input(columns):
    while True:
        column = input("Please enter a column: ").upper()
        if len(column) == 1 and 'A' <= column < chr(65 + columns):
            return ord(column) - 65
        print("Invalid input. Please enter a valid column (e.g., A, B, C, ...).")

def is_valid_move(board, col):
    return board[0][col] == ' '

def place_checker(board, col, player_symbol):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player_symbol
            break

def check_win(board, player_symbol):
    def four_in_a_row(sequence):
        return any(sequence[i:i+4] == [player_symbol]*4 for i in range(len(sequence) - 3))

    # Check horizontal and vertical
    for row in board:
        if four_in_a_row(row):
            return True
    for col in range(len(board[0])):
        if four_in_a_row([board[row][col] for row in range(len(board))]):
            return True

    # Check diagonal
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row+i][col+i] == player_symbol for i in range(4)):
                return True
            if all(board[row+3-i][col+i] == player_symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print("Starting Connect 4!")
    print_board(board)

    while True:
        print(f"Player {PLAYERS[current_player_idx]},", end=" ")
        col = get_column_input(COLUMNS)

        if not is_valid_move(board, col):
            print("Column is full. You've lost your turn.")
        else:
            place_checker(board, col, PLAYERS[current_player_idx])
            print_board(board)

            if check_win(board, PLAYERS[current_player_idx]):
                print(f"Player {PLAYERS[current_player_idx]} won!")
                break

            if check_draw(board):
                print("The game is a draw!")
                break

            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

play_game()
