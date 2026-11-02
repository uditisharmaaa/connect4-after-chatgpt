import os
import random

# Global constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2
BLANK = " "

def clear_screen():
    os.system('clear')  # Use 'cls' for Windows, 'clear' for Linux/Unix.

def create_board():
    return [[BLANK for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column):
    return column.isalpha() and column.upper() in [chr(65 + i) for i in range(COLUMNS)]

def is_column_full(board, column):
    column_index = ord(column.upper()) - 65
    return all(board[row][column_index] != BLANK for row in range(ROWS))

def drop_checker(board, column, checker):
    column_index = ord(column.upper()) - 65
    for row in range(ROWS - 1, -1, -1):
        if board[row][column_index] == BLANK:
            board[row][column_index] = checker
            return

def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != BLANK for col in range(COLUMNS))

def main():
    clear_screen()
    # Initialize board and variables
    board = create_board()
    players = PLAYERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    winner = None

    print_board(board)

    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")
        
        # Handle player input
        while True:
            column = input().strip()
            if not is_valid_column(column):
                print("Invalid input. Please enter a valid column (A-G).")
            elif is_column_full(board, column):
                print("Column is full. Choose a different column.")
            else:
                break

        # Drop the checker
        drop_checker(board, column, current_player)
        clear_screen()
        print_board(board)

        # Check for a winner or draw
        if check_winner(board, current_player):
            winner = current_player
            break
        if is_draw(board):
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Print result
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
