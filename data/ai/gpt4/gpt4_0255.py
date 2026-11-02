import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    print("  " + "   ".join(chr(65 + col) for col in range(COLS)))
    print("+" + "---+" * COLS)

    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_column(col, board):
    # Check if column is within bounds and not full
    return 0 <= col < COLS and board[0][col] == " "

def get_column_from_input(input_char):
    # Convert column letter (e.g., 'A') to a column index
    return ord(input_char.upper()) - ord('A')

def place_checker(column, symbol, board):
    # Drop the checker to the lowest available row in the chosen column
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = symbol
            break

def check_for_win(board, symbol):
    # Check horizontal, vertical, and diagonal for a win
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Diagonal (down-right) check
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Diagonal (down-left) check
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == symbol for i in range(4)):
                return True
                
    return False

def is_draw(board):
    # Check if the board is full (no empty spaces in the top row)
    return all(cell != " " for cell in board[0])

def main():
    # Set up game variables
    num_players = 2  # Set to 2 for this submission
    symbols = PLAYER_SYMBOLS[:num_players]
    board = create_board()
    current_player = random.randint(0, num_players - 1)

    clear_screen()
    print_board(board)

    # Main game loop
    while True:
        print(f"Player {symbols[current_player]}, please enter a column:")
        user_input = input().strip()

        # Validate input
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a valid column letter.")
            continue

        column = get_column_from_input(user_input)
        if not is_valid_column(column, board):
            print("Invalid column. Please choose a different one.")
            continue

        # Place checker
        place_checker(column, symbols[current_player], board)
        clear_screen()
        print_board(board)

        # Check for win or draw
        if check_for_win(board, symbols[current_player]):
            print(f"Player {symbols[current_player]} won!")
            break
        elif is_draw(board):
            print("The game is a draw!")
            break

        # Alternate turns
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
