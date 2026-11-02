import os
import random

# Constants
ROWS, COLS = 6, 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

# Initialize the game board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))  # Column labels
    print("+" + "---+" * COLS)
    for row in board:
        print("|" + "|".join(row) + "|")
        print("+" + "---+" * COLS)

# Check for win conditions
def check_win(board, symbol):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if (c + 3 < COLS and all(board[r][c+i] == symbol for i in range(4))) or \
               (r + 3 < ROWS and all(board[r+i][c] == symbol for i in range(4))) or \
               (r + 3 < ROWS and c + 3 < COLS and all(board[r+i][c+i] == symbol for i in range(4))) or \
               (r - 3 >= 0 and c + 3 < COLS and all(board[r-i][c+i] == symbol for i in range(4))):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Main game loop
def play_connect4():
    board = create_board()
    current_player = random.choice(PLAYERS)

    while True:
        print_board(board)
        while True:
            column = input(f"Player {current_player}, please enter a column: ").upper()
            if len(column) == 1 and column in [chr(65 + c) for c in range(COLS)]:
                col_index = ord(column) - 65
                for row in reversed(range(ROWS)):
                    if board[row][col_index] == " ":
                        board[row][col_index] = current_player
                        break
                else:
                    print("Column is full. Try another column.")
                    continue
                break
            else:
                print("Invalid input. Please enter a valid column.")

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    play_connect4()
