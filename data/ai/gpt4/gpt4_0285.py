import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
ASCII_A = ord('A')

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    header = '  '.join([chr(ASCII_A + i) for i in range(COLUMNS)])
    print(f"  {header}")
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Validate the move
def is_valid_move(board, column):
    return 0 <= column < COLUMNS and board[0][column] == ' '

def drop_checker(board, column, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            return

# Check for win condition
def check_win(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

# Check for draw
def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Main Game Loop
def play_game():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {players[current_player]}'s turn!")
        move = input("Enter a column: ").strip().upper()
        if len(move) == 1 and ASCII_A <= ord(move) < ASCII_A + COLUMNS:
            column = ord(move) - ASCII_A
            if is_valid_move(board, column):
                drop_checker(board, column, players[current_player])
                print_board(board)
                if check_win(board, players[current_player]):
                    print(f"Player {players[current_player]} won!")
                    break
                if is_draw(board):
                    print("The game is a draw!")
                    break
                current_player = (current_player + 1) % PLAYERS
            else:
                print("Invalid move! Try again.")
        else:
            print("Invalid input! Enter a valid column.")

if __name__ == "__main__":
    play_game()
