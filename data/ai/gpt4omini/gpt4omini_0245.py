import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(row) + '|')
        print('+' + '---+' * COLS)

# Check if the move is valid
def is_valid_input(col, board):
    if col < 0 or col >= COLS or board[0][col] != ' ':
        return False
    return True

# Place the checker in the board
def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return

# Check for win
def check_win(board, checker):
    # Check horizontal, vertical and diagonal positions
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                # Check horizontal
                if c + 3 < COLS and all(board[r][c + i] == checker for i in range(4)):
                    return True
                # Check vertical
                if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
                    return True
                # Check diagonal \
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
                # Check diagonal /
                if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == checker for i in range(4)):
                    return True
    return False

# Check for draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Main game function
def connect4():
    board = create_board()
    current_player = random.choice(PLAYERS)
    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        col = input().upper()

        if col in [chr(65 + i) for i in range(COLS)]:
            index = ord(col) - 65
            
            if is_valid_input(index, board):
                place_checker(board, index, current_player)
                
                if check_win(board, current_player):
                    print_board(board)
                    print(f"Player {current_player} won!")
                    game_over = True
                elif check_draw(board):
                    print_board(board)
                    print("It's a draw!")
                    game_over = True
                else:
                    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
            else:
                print("Invalid column. Try again.")
        else:
            print("Invalid input. Enter a letter from A to G.")

if __name__ == "__main__":
    connect4()
