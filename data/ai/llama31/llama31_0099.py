import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a 2D board with whitespaces"""
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    """Print the board with column labels"""
    print('  ' + ' '.join(string.ascii_uppercase[:len(board[0])]))
    print('+' + '+---' * len(board[0]) + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '+---' * len(board[0]) + '+')

def validate_input(input_str, cols):
    """Validate user input"""
    if len(input_str)!= 1 or not input_str.isalpha():
        return False
    if ord(input_str.upper()) - ord('A') < 0 or ord(input_str.upper()) - ord('A') >= cols:
        return False
    return True

def drop_checker(board, col, checker):
    """Drop a checker into a column"""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return

def check_win(board, checker):
    """Check for a win"""
    # Check horizontal locations for win
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

def check_draw(board):
    """Check for a draw"""
    return all(all(cell!= ' ' for cell in row) for row in board)

def main():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {current_player}, please enter a column:")

        while True:
            input_str = input().strip().upper()
            if validate_input(input_str, BOARD_COLS):
                col = ord(input_str) - ord('A')
                if all(cell!= ' ' for cell in [row[col] for row in board]):
                    print("Column is full, please choose another column.")
                else:
                    break
            else:
                print("Invalid input, please enter a letter from A to", string.ascii_uppercase[BOARD_COLS - 1])

        drop_checker(board, col, current_player)

        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
