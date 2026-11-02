import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def print_board(board):
    """Print the current state of the board"""
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| " + " | ".join(row) + " |")
    print("+---+---+---+---+---+---+---+")

def create_board():
    """Create an empty board with the specified dimensions"""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def is_valid_move(board, col):
    """Check if a move is valid (i.e., the column is not full)"""
    return board[0][col] == " "

def get_next_open_row(board, col):
    """Get the next open row in the specified column"""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row

def drop_checker(board, col, checker):
    """Drop a checker into the specified column"""
    row = get_next_open_row(board, col)
    board[row][col] = checker

def winning_move(board, checker):
    """Check if the last move was a winning move"""
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

def game_over(board):
    """Check if the game is over (i.e., the board is full)"""
    return " " not in [cell for row in board for cell in row]

def main():
    # Initialize the board and players
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Print the initial board
    os.system('clear')
    print_board(board)

    # Main game loop
    while True:
        current_player = players[current_player_index]
        print("Player", current_player, "please enter a column (A-G):")
        col = input().upper()

        # Validate the input
        if col not in "ABCDEFG":
            print("Invalid input. Please enter a letter between A and G.")
            continue
        col = ord(col) - ord("A")

        # Check if the move is valid
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue

        # Drop the checker
        drop_checker(board, col, current_player)

        # Clear the screen and print the updated board
        os.system('clear')
        print_board(board)

        # Check for a win
        if winning_move(board, current_player):
            print("Player", current_player, "won!")
            break

        # Check for a draw
        if game_over(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
