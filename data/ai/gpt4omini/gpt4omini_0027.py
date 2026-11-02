import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))  # Column labels
    print('+' + '---+' * COLUMNS)  # Top border
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')  # Row contents
        print('+' + '---+' * COLUMNS)  # Bottom border

# Check for a valid column input
def valid_column(col):
    return col in range(COLUMNS)

# Place a checker in the specified column
def place_checker(board, col, checker):
    for row in reversed(board):  # Start from the bottom row
        if row[col] == ' ':
            row[col] = checker
            return True
    return False  # Column is full

# Check for a win condition
def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (bottom left to top right)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (top left to bottom right)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw (board full)
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game loop
def play_game():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}, please enter a column (A-G): ", end='')

        while True:
            col_input = input().strip().upper()
            if col_input in (chr(65 + i) for i in range(COLUMNS)):
                col = ord(col_input) - 65
                if valid_column(col):
                    if place_checker(board, col, current_player):
                        break
                    else:
                        print("Column is full, try again: ", end='')
                else:
                    print("Invalid column, try again: ", end='')
            else:
                print("Invalid input, please enter a letter (A-G): ", end='')

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    play_game()
