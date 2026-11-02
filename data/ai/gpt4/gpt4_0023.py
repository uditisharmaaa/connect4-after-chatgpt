import os
import random

# Constants
ROWS = 6  # Number of rows
COLS = 7  # Number of columns
PLAYERS = 2  # Number of players
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for players
PLAYER_CHECKERS = CHECKERS[:PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def drop_checker(board, col, checker):
    for row in reversed(board):  # Start from bottom row
        if row[col] == " ":
            row[col] = checker
            return True
    return False  # Column is full

def is_valid_column(col, board):
    return 0 <= col < COLS and board[0][col] == " "

def get_column_from_player(player, board):
    while True:
        player_input = input(f"Player {player} ({PLAYER_CHECKERS[player]}), please enter a column: ").strip().upper()
        if len(player_input) == 1 and 'A' <= player_input <= chr(65 + COLS - 1):
            col = ord(player_input) - 65
            if is_valid_column(col, board):
                return col
            else:
                print("Column is full. Try a different column.")
        else:
            print("Invalid input. Please enter a valid column letter.")

def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check diagonals (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check diagonals (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        col = get_column_from_player(current_player, board)
        if drop_checker(board, col, PLAYER_CHECKERS[current_player]):
            print_board(board)

            # Check for win
            if check_win(board, PLAYER_CHECKERS[current_player]):
                print(f"Player {current_player} ({PLAYER_CHECKERS[current_player]}) won!")
                break

            # Check for draw
            if is_draw(board):
                print("The game is a draw!")
                break

            # Switch to next player
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
