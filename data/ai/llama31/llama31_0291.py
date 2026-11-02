import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
CHECKERS = ["X", "O", "V", "H", "M"][:MAX_PLAYERS]

def create_board():
    """Create a new game board with all elements initialized to whitespace."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| " + " | ".join(row) + " |")
    print("+---+---+---+---+---+---+---+")

def is_valid_input(column):
    """Check if the input is a valid column letter."""
    return column.upper() >= 'A' and column.upper() <= chr(ord('A') + NUM_COLS - 1)

def is_valid_move(board, column):
    """Check if the move is valid (i.e., the column is not full)."""
    return board[0][ord(column.upper()) - ord('A')] == " "

def get_next_open_row(board, column):
    """Get the next open row in the specified column."""
    for row in range(NUM_ROWS-1, -1, -1):
        if board[row][ord(column.upper()) - ord('A')] == " ":
            return row

def drop_checker(board, column, checker):
    """Drop the checker in the specified column."""
    row = get_next_open_row(board, column)
    board[row][ord(column.upper()) - ord('A')] = checker

def check_for_win(board, checker):
    """Check if the current player has won."""
    # Check horizontal locations for win
    for c in range(NUM_COLS-3):
        for r in range(NUM_ROWS):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True

    # Check vertical locations for win
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS-3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(NUM_COLS-3):
        for r in range(NUM_ROWS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(NUM_COLS-3):
        for r in range(3, NUM_ROWS):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True

def check_for_draw(board):
    """Check if the game is a draw (i.e., the board is full)."""
    return all([cell!= " " for row in board for cell in row])

def main():
    num_players = 2
    players = PLAYERS[:num_players]
    current_player_index = random.randint(0, num_players-1)

    board = create_board()
    os.system('clear')
    print_board(board)

    while True:
        current_player = players[current_player_index]
        column = input(f"Player {current_player}, please enter a column: ")
        if not is_valid_input(column):
            print("Invalid input. Please enter a letter from A to G.")
            continue
        if not is_valid_move(board, column):
            print("Column is full. Please choose another column.")
            continue

        drop_checker(board, column, current_player)
        os.system('clear')
        print_board(board)

        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif check_for_draw(board):
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
