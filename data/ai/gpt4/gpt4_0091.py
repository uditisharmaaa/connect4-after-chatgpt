import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for up to 5 players
NUM_PLAYERS = 2  # Number of players (can be adjusted but must be <= MAX_PLAYERS)

def clear_screen():
    os.system('clear')

def initialize_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    header = "  " + "   ".join(chr(65 + col) for col in range(len(board[0])))
    print(header)
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def is_valid_column(column_input, board):
    if len(column_input) != 1 or not column_input.isalpha():
        return False
    column_index = ord(column_input.upper()) - 65
    return 0 <= column_index < len(board[0]) and board[0][column_index] == " "

def drop_checker(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return

def check_winner(board, checker):
    rows, cols = len(board), len(board[0])

    def check_line(start_row, start_col, delta_row, delta_col):
        count = 0
        row, col = start_row, start_col
        while 0 <= row < rows and 0 <= col < cols and board[row][col] == checker:
            count += 1
            row += delta_row
            col += delta_col
        return count

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == checker:
                if check_line(r, c, 0, 1) >= 4:  # Horizontal
                    return True
                if check_line(r, c, 1, 0) >= 4:  # Vertical
                    return True
                if check_line(r, c, 1, 1) >= 4:  # Diagonal /
                    return True
                if check_line(r, c, 1, -1) >= 4:  # Diagonal \
                    return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialize game
    board = initialize_board(ROWS, COLUMNS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print("Welcome to Connect 4!")
    print_board(board)

    while True:
        current_checker = players[current_player_index]
        column_input = ""

        # Get valid move
        while True:
            column_input = input(f"Player {current_checker}, please enter a column: ")
            if is_valid_column(column_input, board):
                break
            print("Invalid input. Please enter a valid column.")

        # Drop checker
        column_index = ord(column_input.upper()) - 65
        drop_checker(board, column_index, current_checker)

        clear_screen()
        print_board(board)

        # Check for win or draw
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        elif is_draw(board):
            print("The game is a draw!")
            break

        # Alternate player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
