import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # Set to number of players for the game

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_input(input_char):
    return input_char.isalpha() and input_char.upper() in [chr(65 + i) for i in range(COLUMNS)]

def drop_checker(board, column, player_symbol):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player_symbol
            return True
    return False

def check_for_win(board, player_symbol):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == player_symbol for i in range(4)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == player_symbol for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == player_symbol for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == player_symbol for i in range(4)):
                return True
    return False

def check_for_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board(ROWS, COLUMNS)
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.choice(player_symbols)
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        column_input = input().strip()
        
        if not is_valid_input(column_input):
            print("Invalid input, please enter a letter corresponding to a column.")
            continue
        
        column = ord(column_input.upper()) - 65  # Convert letter to index

        if not drop_checker(board, column, current_player):
            print(f"Column {column_input} is full, turn is lost.")
        else:
            print_board(board)

            if check_for_win(board, current_player):
                print(f"Player {current_player} won!")
                break

            if check_for_draw(board):
                print("The game is a draw!")
                break

            # Alternate player
            current_player = player_symbols[(player_symbols.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
