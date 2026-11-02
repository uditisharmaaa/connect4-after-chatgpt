import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    print("  " + "   ".join(chr(65 + col) for col in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    # Print rows of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_column(column, board):
    if column.isalpha() and len(column) == 1:
        col_idx = ord(column.upper()) - 65
        if 0 <= col_idx < COLUMNS and board[0][col_idx] == " ":
            return True
    return False

def get_empty_row(board, col_idx):
    for row_idx in range(ROWS-1, -1, -1):
        if board[row_idx][col_idx] == " ":
            return row_idx
    return None

def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row+i][col-i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def connect_four():
    # Initialize game variables
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        player_checker = CHECKERS[current_player]
        print(f"Player {player_checker}, please enter a column: ", end="")
        choice = input().strip()

        if is_valid_column(choice, board):
            col_idx = ord(choice.upper()) - 65
            row_idx = get_empty_row(board, col_idx)
            if row_idx is not None:
                board[row_idx][col_idx] = player_checker
                
                clear_screen()
                print_board(board)

                # Check for a win
                if check_winner(board, player_checker):
                    print(f"Player {player_checker} won!")
                    break

                # Check for a draw
                if is_draw(board):
                    print("It's a draw!")
                    break

                # Switch to next player
                current_player = (current_player + 1) % PLAYERS
            else:
                print("Column is full. Choose another column.")
        else:
            print("Invalid input. Please try again.")

# Start the game
if __name__ == "__main__":
    connect_four()
