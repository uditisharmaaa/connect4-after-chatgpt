import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Support up to 5 players
NUM_PLAYERS = 2  # Set this to the number of players (between 2 and 5)

# Create the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clears the screen
    print("\n  " + "   ".join(chr(i) for i in range(65, 65 + COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

# Check for valid input
def is_valid_input(input_str):
    if len(input_str) != 1:
        return False
    if input_str not in [chr(i) for i in range(65, 65 + COLUMNS)]:
        return False
    return True

# Find lowest empty row in the column
def find_lowest_empty_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

# Place the checker in the board
def place_checker(board, col, checker):
    row = find_lowest_empty_row(board, col)
    if row != -1:
        board[row][col] = checker
        return True
    return False

# Check for a win in the board
def check_for_win(board, checker):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (check_line(board, row, col, 1, 0, checker) or  # Horizontal
                check_line(board, row, col, 0, 1, checker) or  # Vertical
                check_line(board, row, col, 1, 1, checker) or  # Diagonal /
                check_line(board, row, col, 1, -1, checker)):  # Diagonal \
                return True
    return False

# Helper function to check a line for a win
def check_line(board, row, col, delta_row, delta_col, checker):
    count = 0
    for _ in range(4):
        if 0 <= row < ROWS and 0 <= col < COLUMNS and board[row][col] == checker:
            count += 1
            row += delta_row
            col += delta_col
        else:
            break
    return count == 4

# Check for a draw
def check_for_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Randomly select the first player
def select_first_player():
    return random.randint(0, NUM_PLAYERS - 1)

# Main function to execute the game
def main():
    board = create_board()
    current_player_idx = select_first_player()
    player_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]

    while True:
        print_board(board)
        current_player_checker = player_checkers[current_player_idx]
        print(f"Player {current_player_checker}, please enter a column:")

        valid_move = False
        while not valid_move:
            user_input = input().strip().upper()
            if is_valid_input(user_input):
                col = ord(user_input) - 65
                if place_checker(board, col, current_player_checker):
                    valid_move = True
                else:
                    print("Column is full, try another one.")
            else:
                print("Invalid input, please enter a valid column letter.")

        if check_for_win(board, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            break

        if check_for_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
