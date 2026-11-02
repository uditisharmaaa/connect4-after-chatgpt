import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Adjust this list for more players if needed
WINNING_COUNT = 4

# Initialize the game board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers
    print("+---+" + "---+" * (COLS - 1))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLS - 1))

# Check if the column is full
def is_column_full(board, col):
    return board[0][col] != " "

# Get the next available row in the column
def get_available_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1  # Column is full

# Check for a win condition
def check_win(board, player):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                if check_direction(board, player, r, c, 1, 0) or \
                   check_direction(board, player, r, c, 0, 1) or \
                   check_direction(board, player, r, c, 1, 1) or \
                   check_direction(board, player, r, c, 1, -1):
                    return True
    return False

# Check a specific direction for win condition
def check_direction(board, player, row, col, delta_row, delta_col):
    count = 0
    for i in range(WINNING_COUNT):
        r = row + i * delta_row
        c = col + i * delta_col
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
        else:
            break
    return count == WINNING_COUNT

# Check for a draw condition
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Main game loop
def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    game_over = False

    print_board(board)
    while not game_over:
        col = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        
        if col not in 'ABCDEFG' or len(col) != 1:
            print("Invalid input. Please enter a letter between A and G.")
            continue

        col_index = ord(col) - 65
        
        if col_index < 0 or col_index >= COLS:
            print("Column out of bounds. Please select a column between A and G.")
            continue

        if is_column_full(board, col_index):
            print("Column is full. Please choose another column.")
            continue

        row = get_available_row(board, col_index)
        board[row][col_index] = current_player
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
