import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]  # Checker symbols for up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print the column headers
    print("  " + "   ".join(chr(65 + col) for col in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")

    # Print the board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(row) + "+")

def is_valid_input(input_char, cols):
    return len(input_char) == 1 and 'A' <= input_char < chr(65 + cols)

def get_column_index(input_char):
    return ord(input_char) - 65

def is_column_full(board, col):
    return board[0][col] != " "

def drop_checker(board, col, player_symbol):
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_symbol
            return row

def check_winner(board, player_symbol):
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == player_symbol for i in range(4)):
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == player_symbol for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == player_symbol for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == player_symbol for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(len(board[0])))

def main():
    # Initialize board
    board = create_board(ROWS, COLS)

    # Set number of players
    num_players = 2  # Change this value for more players (up to MAX_PLAYERS)

    # Select first player randomly
    current_player = random.randint(0, num_players - 1)

    # Game loop
    while True:
        print_board(board)
        print(f"Player {PLAYERS[current_player]}'s turn")

        # Get valid input
        while True:
            column_input = input("Please enter a column (A-G): ").strip().upper()
            if is_valid_input(column_input, COLS):
                col = get_column_index(column_input)
                if not is_column_full(board, col):
                    break
                else:
                    print("Column is full. Try again.")
            else:
                print("Invalid input. Try again.")

        # Drop the checker
        drop_checker(board, col, PLAYERS[current_player])

        # Check for a win
        if check_winner(board, PLAYERS[current_player]):
            print_board(board)
            print(f"Player {PLAYERS[current_player]} won!")
            break

        # Check for a draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
