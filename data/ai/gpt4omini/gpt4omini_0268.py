import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))  # Column labels
    print("+---" + "---+" * COLS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row contents
        print("+---" + "---+" * COLS)  # Bottom border
    print()

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1  # Column is full

def is_valid_location(board, col):
    return board[0][col] == " "  # Check if the top row is empty

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Check horizontal locations
    for c in range(COLS - 3):
        for r in range(ROWS):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # Check vertical locations
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # Check positively sloped diagonals
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    return False

def is_full(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    game_over = False
    turn = random.randint(0, len(PLAYERS) - 1)  # Randomly select the first player

    print_board(board)

    while not game_over:
        # Ask for input
        current_player = PLAYERS[turn]
        valid_input = False

        while not valid_input:
            column_input = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
            if len(column_input) == 1 and column_input.isalpha():
                col = ord(column_input) - 65  # Convert letter to column index
                if 0 <= col < COLS and is_valid_location(board, col):
                    valid_input = True
                else:
                    print("Invalid input. The column is either full or out of bounds.")
            else:
                print("Invalid input. Please enter a single letter.")

        # Place piece
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, current_player)
        print_board(board)

        # Check for win or draw
        if winning_move(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        elif is_full(board):
            print("It's a draw!")
            game_over = True

        # Alternate turns
        turn = (turn + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
