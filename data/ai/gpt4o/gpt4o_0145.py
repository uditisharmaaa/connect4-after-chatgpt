import os
import random

# Constants for the board dimensions and number of players
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board with empty spaces
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board with column labels and a clear screen
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Validate the input by checking for valid characters and empty column space
def valid_input(column_choice, board):
    if column_choice.isalpha() and ord(column_choice) - 65 < COLS:
        column = ord(column_choice) - 65
        return board[0][column] == " "
    return False

# Drop the checker into the lowest available space in the chosen column
def place_checker(board, column_choice, checker):
    column = ord(column_choice) - 65
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

# Check for a winning move horizontally, vertically, or diagonally
def check_winner(board, checker):
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
            if all(board[row + 3 - i][col + i] == checker for i in range(4)):
                return True
    return False

# Check to see if the board is completely filled
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player_index]
        column_choice = input(f"Player {current_checker}, please enter a column: ").upper()

        if valid_input(column_choice, board):
            place_checker(board, column_choice, current_checker)
            print_board(board)

            if check_winner(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            elif check_draw(board):
                print("The game is a draw!")
                break

            current_player_index = (current_player_index + 1) % PLAYERS
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    main()
