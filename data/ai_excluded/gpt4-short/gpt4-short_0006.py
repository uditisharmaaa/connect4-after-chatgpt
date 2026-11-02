import os
import random

# Game constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ["A", "B", "C", "D", "E", "F", "G"]
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]  # Supports up to 5 players
NUM_PLAYERS = 3  # Change this value from 2 to 5

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def display_board(board):
    os.system('clear')  # Clear the console
    print(" " + " ".join(COLUMN_LABELS))  # Print column labels
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (2 * COLS + 1))

def valid_column(board, col_index):
    return 0 <= col_index < COLS and board[0][col_index] == " "

def drop_piece(board, col_index, token):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = token
            break

def check_winner(board, token):
    # Check horizontal, vertical, and diagonal matches
    for row in range(ROWS):
        for col in range(COLS):
            if col <= COLS - 4 and all(board[row][col + i] == token for i in range(4)):
                return True
            if row <= ROWS - 4 and all(board[row + i][col] == token for i in range(4)):
                return True
            if row <= ROWS - 4 and col <= COLS - 4 and all(board[row + i][col + i] == token for i in range(4)):
                return True
            if row <= ROWS - 4 and col >= 3 and all(board[row + i][col - i] == token for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def get_player_input(player, board):
    while True:
        col_input = input(f"Player {player} ({PLAYER_TOKENS[player]}), select a column (A-G): ").strip().upper()
        if col_input in COLUMN_LABELS:
            col_index = COLUMN_LABELS.index(col_input)
            if valid_column(board, col_index):
                return col_index
        print("Invalid input. Please try again.")

def main():
    os.system('clear')
    print("Welcome to Connect 4!")

    # Initialize game
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        display_board(board)
        print(f"It's Player {current_player + 1}'s ({PLAYER_TOKENS[current_player]}) turn!")
        
        # Get player input and update board
        col_index = get_player_input(current_player, board)
        drop_piece(board, col_index, PLAYER_TOKENS[current_player])
        
        # Check for a win or draw
        if check_winner(board, PLAYER_TOKENS[current_player]):
            display_board(board)
            print(f"Player {current_player + 1} ({PLAYER_TOKENS[current_player]}) wins!")
            break
        if is_draw(board):
            display_board(board)
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
