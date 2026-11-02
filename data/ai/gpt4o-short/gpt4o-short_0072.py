import os
import random

# Constants for the game
NUM_ROWS = 6
NUM_COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    os.system('clear')  # Clears the console
    print("  A  B  C  D  E  F  G ")
    print("+" + "---+" * NUM_COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * NUM_COLS)

def pick_random_first_player(players):
    return random.choice(players)

def is_valid_move(board, col_index):
    return board[0][col_index] == ' '

def make_move(board, col_index, player_symbol):
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = player_symbol
            break

def check_win(board, player_symbol):
    # Check horizontal, vertical, and diagonal directions for a win
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r][c+i] == player_symbol for i in range(4)):
                return True

    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS):
            if all(board[r+i][c] == player_symbol for i in range(4)):
                return True
    
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS - 3):
            if all(board[r+i][c+i] == player_symbol for i in range(4)):
                return True

    for r in range(3, NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r-i][c+i] == player_symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(NUM_COLS))

def get_column_input():
    while True:
        column = input("Choose column (A-G): ").strip().upper()
        if column in 'ABCDEFG':
            return ord(column) - ord('A')
        print("Invalid input. Enter a letter between A and G.")

def play_game():
    num_players = int(input("Enter number of players (2-5): ").strip())
    players = PLAYER_SYMBOLS[:num_players]

    board = initialize_board()
    current_player = pick_random_first_player(players)

    while True:
        print_board(board)
        print(f"Player {current_player}'s turn.")
        
        col_index = get_column_input()

        if not is_valid_move(board, col_index):
            print("Column full or invalid move, try again.")
            continue

        make_move(board, col_index, current_player)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % num_players]

play_game()
