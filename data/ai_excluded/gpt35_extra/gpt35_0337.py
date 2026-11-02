import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # up to 5 players
REQUIRED_TO_WIN = 4

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(COLUMNS)]
    print("  " + "   ".join(labels))
    # Print board rows
    line = "+---" * COLUMNS + "+"
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)

def get_valid_column_input(player_checker):
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ")
        if len(col_input) != 1:
            # Invalid length
            print("Invalid input. Please enter exactly one uppercase letter from A to " + chr(ord('A') + COLUMNS - 1) + ".")
            continue
        if not ('A' <= col_input <= chr(ord('A') + COLUMNS - 1)):
            # Not a valid column letter
            print("Invalid input. Column must be a letter from A to " + chr(ord('A') + COLUMNS - 1) + ".")
            continue
        return col_input

def place_checker(board, col, player_checker):
    # col is a zero-based column index
    # place checker in lowest empty row of this column
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    # Column full
    return False

def check_winner(board, player_checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLUMNS - REQUIRED_TO_WIN + 1):
            if (board[r][c] == player_checker and
                board[r][c+1] == player_checker and
                board[r][c+2] == player_checker and
                board[r][c+3] == player_checker):
                return True
    # Vertical check
    for c in range(COLUMNS):
        for r in range(ROWS - REQUIRED_TO_WIN + 1):
            if (board[r][c] == player_checker and
                board[r+1][c] == player_checker and
                board[r+2][c] == player_checker and
                board[r+3][c] == player_checker):
                return True
    # Diagonal "\" check
    for r in range(ROWS - REQUIRED_TO_WIN + 1):
        for c in range(COLUMNS - REQUIRED_TO_WIN + 1):
            if (board[r][c] == player_checker and
                board[r+1][c+1] == player_checker and
                board[r+2][c+2] == player_checker and
                board[r+3][c+3] == player_checker):
                return True
    # Diagonal "/" check
    for r in range(REQUIRED_TO_WIN - 1, ROWS):
        for c in range(COLUMNS - REQUIRED_TO_WIN + 1):
            if (board[r][c] == player_checker and
                board[r-1][c+1] == player_checker and
                board[r-2][c+2] == player_checker and
                board[r-3][c+3] == player_checker):
                return True
    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]

    # Random starting player
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = players_checkers[current_player_index]

        col_input = get_valid_column_input(player_checker)
        col_index = ord(col_input) - ord('A')

        placed = place_checker(board, col_index, player_checker)
        if not placed:
            # Column full, player loses turn
            print(f"Column {col_input} is full. Player {player_checker} loses the turn.")
        else:
            print_board(board)
            # Check for win
            if check_winner(board, player_checker):
                print(f"Player {player_checker} won!")
                break
            # Check for draw
            if board_full(board):
                print("The game is a draw.")
                break

        # Move to next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
