import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Supports up to 5 players

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the console
    # Print column labels
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_input(player):
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if len(column) != 1 or not ('A' <= column <= chr(ord('A') + COLS - 1)):
            print("Invalid input. Please enter a column letter (A-G).")
            continue
        col_index = ord(column) - ord('A')
        if board[0][col_index] != ' ':
            print("Column is full. Please choose another column.")
            continue
        return col_index

def place_checker(board, col_index, player):
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = player
            return True
    return False

def check_winner(board, player):
    # Check horizontal, vertical, and diagonal for a winner
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

# Main game logic
board = create_board()
current_player_index = random.randint(0, min(1, len(PLAYERS) - 1))
game_over = False

print_board(board)

while not game_over:
    current_player = PLAYERS[current_player_index]
    col_index = get_valid_input(current_player)
    place_checker(board, col_index, current_player)

    print_board(board)

    if check_winner(board, current_player):
        print(f"Player {current_player} won!")
        game_over = True
    elif check_draw(board):
        print("The game is a draw!")
        game_over = True
    else:
        current_player_index = (current_player_index + 1) % len(PLAYERS)
