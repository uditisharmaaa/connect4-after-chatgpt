import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(i) for i in range(65, 65 + COLS)))
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

def random_player(players):
    return random.randint(0, players - 1)

def is_valid_input(column):
    return column.isalpha() and 'A' <= column <= chr(65 + COLS - 1)

def place_checker(board, column, checker):
    col_idx = ord(column) - 65
    for row_idx in range(ROWS-1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    return None

def check_win(board, row, col):
    checker = board[row][col]
    
    # check horizontal
    for c in range(max(col - 3, 0), min(col, COLS - 4) + 1):
        if all(board[row][c + i] == checker for i in range(4)):
            return True
    
    # check vertical
    for r in range(max(row - 3, 0), min(row, ROWS - 4) + 1):
        if all(board[r + i][col] == checker for i in range(4)):
            return True
    
    # check diagonal
    for d in range(-3, 1):
        # Check downward diagonal
        if 0 <= row + d < ROWS - 3 and 0 <= col + d < COLS - 3:
            if all(board[row + d + i][col + d + i] == checker for i in range(4)):
                return True
        # Check upward diagonal
        if 3 <= row - d < ROWS and 0 <= col + d < COLS - 3:
            if all(board[row - d - i][col + d + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board(ROWS, COLS)
    player_turn = random_player(PLAYERS)
    print_board(board)

    while True:
        checker = CHECKERS[player_turn]
        column = input(f"Player {checker}, please enter a column: ").upper()

        while not is_valid_input(column) or place_checker(board, column, checker) is None:
            print("Invalid input. Try again.")
            column = input(f"Player {checker}, please enter a column: ").upper()

        row, col = place_checker(board, column, checker)
        print_board(board)

        if check_win(board, row, col):
            print(f"Player {checker} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break

        player_turn = (player_turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
