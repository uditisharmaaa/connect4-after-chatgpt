import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    # Print column labels
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(len(board[0]))))
    # Print board
    for row in board:
        print('+---' * len(row) + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * len(board[0]) + '+')

def valid_move(board, column):
    if column < 0 or column >= len(board[0]) or board[0][column] != ' ':
        return False
    return True

def make_move(board, column, checker):
    for i in range(len(board) - 1, -1, -1):
        if board[i][column] == ' ':
            board[i][column] = checker
            break

def check_win(board, checker):
    # Horizontal check
    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Vertical check
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal check (bottom left to top right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Diagonal check (top left to bottom right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def connect_four():
    board = initialize_board(ROWS, COLUMNS)
    current_player = random.choice(range(PLAYERS))
    print_board(board)

    while True:
        player_checker = CHECKERS[current_player]
        move = input(f"Player {player_checker}, please enter a column: ").strip().upper()

        if move.isalpha() and len(move) == 1:
            column = ord(move) - ord('A')
            if valid_move(board, column):
                make_move(board, column, player_checker)
                print_board(board)

                if check_win(board, player_checker):
                    print(f"Player {player_checker} won!")
                    break
                elif check_draw(board):
                    print("The game is a draw.")
                    break

                current_player = (current_player + 1) % PLAYERS
            else:
                print("Invalid move, try again.")
        else:
            print("Invalid input, try again.")

if __name__ == "__main__":
    connect_four()
