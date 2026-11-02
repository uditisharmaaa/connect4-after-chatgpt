import os
import random

# Constants for board size and number of players
ROWS = 6
COLS = 7
PLAYERS = 2  # Change this to support more players (max 5)
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols for players

def create_board():
    """Creates an empty game board"""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board"""
    os.system('clear')  # Clears the terminal screen
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))  # Column labels: A, B, C...
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")
    print()

def get_valid_column_input():
    """Gets and validates user input for column selection"""
    while True:
        column = input("Enter a column (A-G): ").upper().strip()
        if len(column) == 1 and "A" <= column < chr(65 + COLS):
            return ord(column) - 65
        print("Invalid input. Please enter a valid column (A-G).")

def is_column_full(board, col):
    """Checks if a column is full"""
    return board[0][col] != " "

def place_checker(board, col, checker):
    """Places a checker in the specified column"""
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row

def check_winner(board, row, col, checker):
    """Checks if a player has won after placing a checker"""
    def count_in_direction(delta_row, delta_col):
        count = 0
        r, c = row, col
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += delta_row
            c += delta_col
        return count

    # Check all directions: horizontal, vertical, diagonals
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    for dr, dc in directions[::2]:  # Consider opposite directions in pairs
        count = count_in_direction(dr, dc) + count_in_direction(-dr, -dc) - 1
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Checks if the board is full"""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    """Main function to run the game"""
    board = create_board()
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player = random.randint(0, PLAYERS - 1)  # Randomly select first player

    print_board(board)
    print(f"Player {players[current_player]} goes first!\n")

    while True:
        # Print current player's turn
        print(f"Player {players[current_player]}'s turn!")
        
        # Get a valid column
        column = get_valid_column_input()

        # Check if column is full
        if is_column_full(board, column):
            print("Column is full. You lose your turn.")
            current_player = (current_player + 1) % PLAYERS
            continue

        # Place the checker
        row = place_checker(board, column, players[current_player])
        print_board(board)

        # Check for win
        if check_winner(board, row, column, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
