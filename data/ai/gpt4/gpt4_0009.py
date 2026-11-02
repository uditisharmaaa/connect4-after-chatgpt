import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Supports up to 5 players

def create_board():
    """Create the game board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Display the board on the console."""
    os.system('clear')  # Clear the console
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    horizontal_border = "+---" * COLUMNS + "+"
    print(column_labels)
    for row in board:
        print(horizontal_border)
        print("| " + " | ".join(row) + " |")
    print(horizontal_border)

def is_valid_column(column, board):
    """Check if the column input is valid."""
    if column < 0 or column >= COLUMNS:
        return False
    if board[0][column] != " ":
        return False
    return True

def drop_checker(column, checker, board):
    """Drop a checker into the selected column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return row, column

def check_win(board, last_row, last_col):
    """Check for a win condition."""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, Vertical, Diagonal /
    for dr, dc in directions:
        count = 1
        for direction in (1, -1):  # Check both directions
            r, c = last_row, last_col
            while True:
                r += dr * direction
                c += dc * direction
                if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == board[last_row][last_col]:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    # Initialize the game
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, it's your turn!")
        while True:
            try:
                column_input = input("Please enter a column (A-G): ").strip().upper()
                if len(column_input) != 1 or not column_input.isalpha():
                    raise ValueError()
                column = ord(column_input) - 65  # Convert column letter to index
                if not is_valid_column(column, board):
                    raise ValueError()
                break
            except ValueError:
                print("Invalid input. Please try again.")

        # Drop the checker
        last_row, last_col = drop_checker(column, current_player, board)
        print_board(board)

        # Check for a win
        if check_win(board, last_row, last_col):
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
