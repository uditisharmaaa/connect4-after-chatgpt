import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Use 'cls' if on Windows
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" + "---+".join([""] * COLS) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+".join([""] * COLS) + "---+")

def get_valid_column():
    while True:
        col = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        if len(col) == 1 and 'A' <= col <= 'G':
            index = ord(col) - 65
            if any(board[row][index] == ' ' for row in range(ROWS)):
                return index
            else:
                print("Column is full! Choose another column.")
        else:
            print("Invalid input! Please enter a letter from A to G.")

def place_checker(board, column, player):
    for row in reversed(range(ROWS)):
        if board[row][column] == ' ':
            board[row][column] = player
            return

def check_win(board, player):
    # Check horizontal, vertical, and diagonal
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                # Check horizontal
                if col + 3 < COLS and all(board[row][col+i] == player for i in range(4)):
                    return True
                # Check vertical
                if row + 3 < ROWS and all(board[row+i][col] == player for i in range(4)):
                    return True
                # Check diagonal \
                if row + 3 < ROWS and col + 3 < COLS and all(board[row+i][col+i] == player for i in range(4)):
                    return True
                # Check diagonal /
                if row - 3 >= 0 and col + 3 < COLS and all(board[row-i][col+i] == player for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(board[row][col] != ' ' for row in range(ROWS) for col in range(COLS))

# Main game loop
def play_game():
    global current_player
    board = initialize_board()
    current_player = random.choice(PLAYERS)

    print_board(board)
    
    while True:
        column = get_valid_column()
        place_checker(board, column, current_player)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Alternate player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    play_game()
