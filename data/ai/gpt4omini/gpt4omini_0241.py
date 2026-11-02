import os
import random

# Constants
COLUMNS = 7
ROWS = 6
PLAYERS = ["X", "O"]

# Create and initialize the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column labels A, B, C, ...
    print("+---" + "+---" * (COLUMNS - 1) + "+")
    for row in board:
        print("|".join(" " + cell + " " for cell in row) + "|")
        print("+---" + "+---" * (COLUMNS - 1) + "+")

# Find the next available row in a column
def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1  # Column is full

# Check for wins
def winning_move(board, player):
    # Check horizontal
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    # Check positively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True

    return False

# Check for draw
def is_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

# Main game function
def main():
    board = create_board()
    game_over = False
    turn = random.randint(0, len(PLAYERS) - 1)
    
    print_board(board)

    while not game_over:
        current_player = PLAYERS[turn]
        column_choice = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLUMNS - 1)}): ").upper()

        # Validate input
        if column_choice not in (chr(65 + i) for i in range(COLUMNS)):
            print("Invalid input. Please choose a valid column.")
            continue

        column = ord(column_choice) - 65
        row = get_next_open_row(board, column)

        if row == -1:
            print("Column is full. Try a different column.")
            continue

        # Drop the piece
        board[row][column] = current_player
        print_board(board)

        # Check for a win
        if winning_move(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        elif is_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            turn = (turn + 1) % len(PLAYERS)  # Switch turns

if __name__ == "__main__":
    main()
