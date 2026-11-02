import os
import random

# Constants for the board and players
NUM_ROWS = 6
NUM_COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
BOARD_COLUMN_LABELS = [chr(i) for i in range(ord('A'), ord('A') + MAX_COLUMNS)]

# Initialize the board and players
def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board, rows, columns):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(BOARD_COLUMN_LABELS[:columns]))
    print("+---" * columns + "+")
    for row in range(rows):
        print("| " + " | ".join(board[row]) + " |")
        print("+---" * columns + "+")

def valid_input(column_input, columns):
    return column_input in BOARD_COLUMN_LABELS[:columns]

def place_checker(board, column, player_symbol):
    for row in reversed(range(NUM_ROWS)):
        if board[row][column] == ' ':
            board[row][column] = player_symbol
            return True
    return False

def check_win(board, rows, columns, player_symbol):
    # Check horizontal win
    for row in range(rows):
        for col in range(columns - 3):
            if all(board[row][col + i] == player_symbol for i in range(4)):
                return True

    # Check vertical win
    for col in range(columns):
        for row in range(rows - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True

    # Check diagonal win (\ direction)
    for row in range(rows - 3):
        for col in range(columns - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True

    # Check diagonal win (/ direction)
    for row in range(3, rows):
        for col in range(columns - 3):
            if all(board[row - i][col + i] == player_symbol for i in range(4)):
                return True

    return False

def check_draw(board, rows, columns):
    return all(board[0][col] != ' ' for col in range(columns))

def main():
    board = initialize_board(NUM_ROWS, NUM_COLUMNS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board, NUM_ROWS, NUM_COLUMNS)
        print(f"Player {players[current_player_index]}, please enter a column:")

        column_input = input().strip().upper()
        while not valid_input(column_input, NUM_COLUMNS):
            print("Invalid input. Please enter a valid column:")
            column_input = input().strip().upper()
        
        column_index = BOARD_COLUMN_LABELS.index(column_input)

        if place_checker(board, column_index, players[current_player_index]):
            if check_win(board, NUM_ROWS, NUM_COLUMNS, players[current_player_index]):
                print_board(board, NUM_ROWS, NUM_COLUMNS)
                print(f"Player {players[current_player_index]} won!")
                break
            elif check_draw(board, NUM_ROWS, NUM_COLUMNS):
                print_board(board, NUM_ROWS, NUM_COLUMNS)
                print("The game is a draw!")
                break

            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print("Column full. Turn lost.")

if __name__ == "__main__":
    main()
