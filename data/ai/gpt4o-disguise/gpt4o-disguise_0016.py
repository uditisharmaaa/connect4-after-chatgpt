import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYER_COUNT]

# Initialize the game board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the current state of the board
def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

# Check if the move is valid
def is_valid_move(move, board):
    if move.isalpha() and len(move) == 1:
        col = ord(move.upper()) - 65
        if 0 <= col < COLUMNS and board[0][col] == ' ':
            return True
    return False

# Place the checker in the chosen column
def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            break

# Check if a player has won
def check_win(board, checker):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if check_line(board, row, col, checker, 0, 1) or check_line(board, row, col, checker, 1, 0) or check_line(board, row, col, checker, 1, 1) or check_line(board, row, col, checker, 1, -1):
                return True
    return False

# Check a line for a win condition
def check_line(board, row, col, checker, row_dir, col_dir):
    if not (0 <= row + 3 * row_dir < ROWS and 0 <= col + 3 * col_dir < COLUMNS):
        return False
    for i in range(4):
        if board[row + i * row_dir][col + i * col_dir] != checker:
            return False
    return True

# Check if the board is full
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game loop
def main():
    board = create_board()
    current_player = random.choice(range(PLAYER_COUNT))
    print_board(board)

    while True:
        move = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        if is_valid_move(move, board):
            col = ord(move) - 65
            place_checker(board, col, CHECKERS[current_player])
            print_board(board)

            if check_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break

            if check_draw(board):
                print("The game is a draw!")
                break

            current_player = (current_player + 1) % PLAYER_COUNT
        else:
            print("Invalid move. Please try again.")

main()
