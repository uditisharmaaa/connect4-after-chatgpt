import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with the given dimensions."""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A B C D E F G")
    for row in board:
        print("+---" * BOARD_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_COLS + "+")

def validate_input(column):
    """Check if the input column is valid."""
    if not column.isalpha() or len(column)!= 1:
        return False
    column_index = ord(column.upper()) - ord('A')
    if column_index < 0 or column_index >= BOARD_COLS:
        return False
    return True

def place_checker(board, player, column):
    """Place a checker in the given column."""
    column_index = ord(column.upper()) - ord('A')
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = player
            break
    else:
        print("Column is full. Please choose another column.")
        return False
    return True

def check_win(board, player):
    """Check if the given player has won."""
    # Check horizontal locations for win
    for c in range(BOARD_COLS-3):
        for r in range(BOARD_ROWS):
            if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS-3):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS-3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= " " for row in board for cell in row)

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS-1)
    while True:
        print_board(board)
        print(f"Player {players[current_player_index]}, please enter a column:")
        column = input().strip().upper()
        if not validate_input(column):
            print("Invalid input. Please try again.")
            continue
        if not place_checker(board, players[current_player_index], column):
            continue
        if check_win(board, players[current_player_index]):
            print_board(board)
            print(f"Player {players[current_player_index]} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
