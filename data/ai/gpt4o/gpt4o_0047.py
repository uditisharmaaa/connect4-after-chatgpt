import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_input(column):
    return len(column) == 1 and 'A' <= column <= chr(ord('A') + COLUMNS - 1)

def place_checker(board, column, symbol):
    col_index = ord(column) - ord('A')
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = symbol
            return True
    return False

def check_winner(board, symbol):
    def check_direction(start_row, start_col, delta_row, delta_col):
        count = 0
        for step in range(4):
            r = start_row + step * delta_row
            c = start_col + step * delta_col
            if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == symbol:
                count += 1
            else:
                break
        return count == 4

    for r in range(ROWS):
        for c in range(COLUMNS):
            if (
                check_direction(r, c, 0, 1) or  # Horizontal
                check_direction(r, c, 1, 0) or  # Vertical
                check_direction(r, c, 1, 1) or  # Diagonal /
                check_direction(r, c, 1, -1)   # Diagonal \
            ):
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def connect4_game():
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    print_board(board)
    
    while True:
        current_symbol = player_symbols[current_player_index]
        print(f"Player {current_symbol}, please enter a column:")
        
        column = input().upper()
        while not is_valid_input(column):
            print("Invalid input. Please enter a valid column letter:")
            column = input().upper()

        if place_checker(board, column, current_symbol):
            print_board(board)

            if check_winner(board, current_symbol):
                print(f"Player {current_symbol} won!")
                break
            elif is_draw(board):
                print("The game is a draw!")
                break

            current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print("Column is full. You lose your turn.")

if __name__ == "__main__":
    connect4_game()
