import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

# Initialize board
def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print board
def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLS + '+')

# Place checker
def place_checker(board, col, token):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = token
            return True
    return False

# Check for win
def check_win(board, token):
    # Check horizontal, vertical, diagonal
    def streak(row, col, dr, dc):
        return all(board[row + i * dr][col + i * dc] == token for i in range(4))

    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != token:
                continue
            if c <= COLS - 4 and streak(r, c, 0, 1): return True
            if r <= ROWS - 4:
                if streak(r, c, 1, 0): return True
                if c <= COLS - 4 and streak(r, c, 1, 1): return True
                if c >= 3 and streak(r, c, 1, -1): return True
    return False

# Check for draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game logic
def main():
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        token = PLAYER_TOKENS[current_player]
        print(f"Player {token}, please enter a column:")
        while True:
            col_input = input().strip().upper()
            if len(col_input) == 1 and 'A' <= col_input <= chr(65 + COLS - 1):
                col = ord(col_input) - 65
                if place_checker(board, col, token):
                    break
                else:
                    print("Column is full. Choose another.")
            else:
                print("Invalid input. Try again.")

        print_board(board)

        if check_win(board, token):
            print(f"Player {token} won!")
            break
        if check_draw(board):
            print("Game is a draw!")
            break
        
        # Alternate player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
