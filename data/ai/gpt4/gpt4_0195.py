import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print the column labels (A, B, C, ...)
    col_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(col_labels)
    print("+---" * len(board[0]) + "+")

    # Print the board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(row) + "+")

def validate_column_input(col_input, cols):
    if len(col_input) != 1 or not col_input.isalpha():
        return False
    col = ord(col_input.upper()) - 65
    return 0 <= col < cols

def is_column_full(board, col):
    return board[0][col] != " "

def drop_checker(board, col, symbol):
    for row in range(len(board) - 1, -1, -1):  # Start from the bottom row
        if board[row][col] == " ":
            board[row][col] = symbol
            return row, col

def check_winner(board, symbol, row, col):
    return (check_direction(board, symbol, row, col, 0, 1) or  # Horizontal
            check_direction(board, symbol, row, col, 1, 0) or  # Vertical
            check_direction(board, symbol, row, col, 1, 1) or  # Diagonal /
            check_direction(board, symbol, row, col, 1, -1))   # Diagonal \

def check_direction(board, symbol, row, col, row_dir, col_dir):
    count = 1
    for step in range(1, 4):  # Check forward
        r, c = row + step * row_dir, col + step * col_dir
        if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
            count += 1
        else:
            break
    for step in range(1, 4):  # Check backward
        r, c = row - step * row_dir, col - step * col_dir
        if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
            count += 1
        else:
            break
    return count >= 4

def is_board_full(board):
    return all(cell != " " for cell in board[0])

def main():
    # Initialize game
    board = create_board(ROWS, COLS)
    num_players = 2  # Change for more players
    players = PLAYER_SYMBOLS[:num_players]
    current_player = random.randint(0, num_players - 1)
    winner = None

    print_board(board)
    print(f"Player {players[current_player]} will go first!")

    # Game loop
    while True:
        print_board(board)

        col_input = input(f"Player {players[current_player]}, please enter a column: ").strip().upper()
        if not validate_column_input(col_input, COLS):
            print("Invalid input. Please enter a valid column (A-G).")
            continue

        col = ord(col_input) - 65
        if is_column_full(board, col):
            print("Column is full! Choose a different column.")
            continue

        row, col = drop_checker(board, col, players[current_player])

        # Check for a win
        if check_winner(board, players[current_player], row, col):
            winner = players[current_player]
            break

        # Check for a draw
        if is_board_full(board):
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

    # Game over
    print_board(board)
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
