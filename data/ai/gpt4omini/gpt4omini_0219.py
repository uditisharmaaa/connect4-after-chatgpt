import os
import random

# Constants for the board dimensions and player tokens
ROWS = 6
COLS = 7
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

# Function to initialize the game board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the game board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

# Function to drop a checker into the board
def drop_checker(board, column, token):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = token
            return True
    return False

# Function to check if a player has won
def check_win(board, token):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == token for i in range(4)):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == token for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == token for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == token for i in range(4)):
                return True

    return False

# Function to check if the game ends in a draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main function to run the Connect 4 game
def main():
    board = create_board()
    players_count = min(len(PLAYER_TOKENS), 5)
    current_player = random.randint(0, players_count - 1)

    while True:
        print_board(board)
        current_token = PLAYER_TOKENS[current_player]
        column_input = input(f"Player {current_token}, please enter a column (A-G): ").upper()

        if len(column_input) != 1 or ord(column_input) < ord('A') or ord(column_input) >= ord('A') + COLS:
            print("Invalid input! Please select a valid column.")
            continue

        column = ord(column_input) - ord('A')
        if not drop_checker(board, column, current_token):
            print("Column is full! Please select a different column.")
            continue

        if check_win(board, current_token):
            print_board(board)
            print(f"Player {current_token} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % players_count

if __name__ == "__main__":
    main()
