import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Function to create an empty board
def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Function to check if the input column is valid
def is_valid_input(column):
    return column in "ABCDEFG"[:COLS]

# Function to find the next open row in a specific column
def get_next_open_row(board, column):
    for r in range(ROWS-1, -1, -1):
        if board[r][column] == ' ':
            return r
    return -1

# Function to place a checker on the board
def drop_piece(board, row, column, piece):
    board[row][column] = piece

# Function to check for a win
def check_winner(board, piece):
    # Check horizontal locations for win
    for c in range(COLS - 3):
        for r in range(ROWS):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # Check positively sloped diagonals
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Main function to run the game
def main():
    board = initialize_board()
    players = PLAYER_SYMBOLS[:2]  # Using only 2 players for submission
    turn = random.randint(0, 1)  # Randomly select the first player

    print_board(board)

    while True:
        current_player = players[turn]
        column = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()

        if is_valid_input(column):
            col_index = ord(column) - 65
            row_index = get_next_open_row(board, col_index)

            if row_index != -1:
                drop_piece(board, row_index, col_index, current_player)
                print_board(board)

                if check_winner(board, current_player):
                    print(f"Player {current_player} won!")
                    break

                if check_draw(board):
                    print("It's a draw!")
                    break

                turn = (turn + 1) % len(players)  # Switch turns
            else:
                print("Column is full! Try another column.")
        else:
            print("Invalid input! Please enter a valid column letter.")

if __name__ == "__main__":
    main()
