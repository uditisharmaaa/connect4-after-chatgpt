import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]  # Checker symbols for up to 5 players
NUM_PLAYERS = 2  # Change this value for more players

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels (A, B, C, ...)
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_move(column, board):
    # Check if column is in range and has empty spaces
    return 0 <= column < COLS and board[0][column] == " "

def get_next_open_row(column, board):
    # Find the lowest available row for the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            return row

def place_checker(column, symbol, board):
    row = get_next_open_row(column, board)
    board[row][column] = symbol

def check_winner(board, symbol):
    # Check horizontal wins
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Check vertical wins
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check diagonal (/) wins
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonal (\) wins
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][column] != " " for column in range(COLS))

def get_player_input(player):
    while True:
        user_input = input(f"Player {player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if len(user_input) == 1 and 'A' <= user_input <= chr(65 + COLS - 1):
            return ord(user_input) - 65
        print("Invalid input. Try again!")

def game_loop():
    clear_screen()
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)  # Random starting player
    print_board(board)

    while True:
        player_symbol = PLAYERS[current_player]
        print(f"Player {player_symbol}'s turn")
        
        column = get_player_input(player_symbol)
        if not is_valid_move(column, board):
            print("Column full or invalid! Try again.")
            continue

        place_checker(column, player_symbol, board)
        clear_screen()
        print_board(board)

        if check_winner(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS  # Switch to next player

if __name__ == "__main__":
    game_loop()
