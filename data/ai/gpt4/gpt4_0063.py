import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))
    # Print rows with grid lines
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def get_valid_column():
    while True:
        column = input("Please enter a column: ").strip().upper()
        if len(column) == 1 and 'A' <= column < chr(65 + COLS):
            return ord(column) - 65
        else:
            print("Invalid input. Enter a valid column letter (e.g., A-G).")

def place_checker(board, column, symbol):
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom row
        if board[row][column] == " ":
            board[row][column] = symbol
            return row, column
    return None  # Column is full

def is_winning_move(board, player_symbol, r, c):
    # Check directions: horizontal, vertical, diagonal (both ways)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for step in range(1, 4):  # Check forward
            nr, nc = r + step * dr, c + step * dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == player_symbol:
                count += 1
            else:
                break
        for step in range(1, 4):  # Check backward
            nr, nc = r - step * dr, c - step * dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == player_symbol:
                count += 1
            else:
                break
        if count >= 4:  # If 4 in a row is found
            return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))  # Top row filled?

def game():
    # Initialize game
    board = create_board()
    num_players = 2  # Fixed at 2 players for this assignment
    symbols = PLAYER_SYMBOLS[:num_players]
    current_player = random.randint(0, num_players - 1)  # Randomly select first player

    print_board(board)

    while True:
        print(f"Player {symbols[current_player]}'s turn.")
        col = get_valid_column()

        # Place checker
        result = place_checker(board, col, symbols[current_player])
        if not result:  # Column was full
            print("Column is full. Try again.")
            continue

        r, c = result
        print_board(board)

        # Check for a win
        if is_winning_move(board, symbols[current_player], r, c):
            print(f"Player {symbols[current_player]} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    game()
