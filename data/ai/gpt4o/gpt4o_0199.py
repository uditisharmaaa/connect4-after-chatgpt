import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS_COUNT]
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Initialize board
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Print board
def print_board(board):
    os.system('clear')
    # Print column headers
    print('  ' + '   '.join(LETTERS[:COLS]))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

# Check for a win
def check_for_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all([cell == checker for cell in row[col:col+4]]):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all([board[row+i][col] == checker for i in range(4)]):
                return True

    # Check diagonals (bottom-left to top-right and bottom-right to top-left)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all([board[row+i][col+i] == checker for i in range(4)]):
                return True
        for col in range(3, COLS):
            if all([board[row+i][col-i] == checker for i in range(4)]):
                return True
    
    return False

# Check for a draw
def check_for_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Get valid input
def get_valid_input():
    while True:
        player_input = input("Select a column: ").upper()
        if player_input in LETTERS[:COLS]:
            col = LETTERS.index(player_input)
            if board[0][col] == ' ':
                return col
            else:
                print("Column full! Choose another one.")
        else:
            print("Invalid input! Choose a valid column letter.")

# Place checker
def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            break

# Main function
def main():
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS_COUNT - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, it's your turn.")
        col = get_valid_input()
        place_checker(board, col, CHECKERS[current_player])
        print_board(board)

        if check_for_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_for_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS_COUNT

if __name__ == "__main__":
    main()
