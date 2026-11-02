import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for players

def clear_screen():
    os.system('clear')

def create_board():
    """Create an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board."""
    col_labels = "  ".join(chr(i + ord('A')) for i in range(COLS))
    print(f"  {col_labels}")
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_input(user_input, board):
    """Validate the user's input."""
    if len(user_input) != 1 or not user_input.isalpha():
        return False
    col_index = ord(user_input.upper()) - ord('A')
    if col_index < 0 or col_index >= COLS:
        return False
    return board[0][col_index] == " "

def place_checker(board, col, checker):
    """Place the checker in the chosen column."""
    col_index = ord(col.upper()) - ord('A')
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom of the column
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index  # Return the row and column of the placement

def check_win(board, row, col, checker):
    """Check for a win condition."""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, vertical, diagonal /
    for dr, dc in directions:
        count = 1
        for direction in (1, -1):  # Check both directions
            r, c = row, col
            while True:
                r += dr * direction
                c += dc * direction
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                    count += 1
                else:
                    break
        if count >= 4:  # Check if 4 in a row
            return True
    return False

def check_draw(board):
    """Check if the board is full."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    clear_screen()
    board = create_board()
    players = CHECKERS[:PLAYERS_COUNT]  # Get checkers for the number of players
    current_player = random.choice(players)  # Randomly select the first player

    print("Welcome to Connect 4!")
    print_board(board)

    while True:
        print(f"Player {current_player}, it's your turn!")
        user_input = input("Please enter a column (A-G): ").strip()
        
        if not is_valid_input(user_input, board):
            print("Invalid input. Please try again.")
            continue

        # Place the checker
        row, col = place_checker(board, user_input, current_player)
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Switch to next player
        current_index = players.index(current_player)
        current_player = players[(current_index + 1) % PLAYERS_COUNT]

if __name__ == "__main__":
    main()
